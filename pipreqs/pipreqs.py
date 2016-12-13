#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pipreqs - Generate pip requirements.txt file based on imports

Usage:
    pipreqs [options] <path>

Options:
    --use-local           Use ONLY local package info instead of querying PyPI
    --pypi-server <url>   Use custom PyPi server
    --proxy <url>         Use Proxy, parameter will be passed to requests library. You can also just set the
                          environments parameter in your terminal:
                          $ export HTTP_PROXY="http://10.10.1.10:3128"
                          $ export HTTPS_PROXY="https://10.10.1.10:1080"
    --debug               Print debug information
    --ignore <dirs>...    Ignore extra directories, each separated by a comma
    --encoding <charset>  Use encoding parameter for file open
    --savepath <file>     Save the list of requirements in the given file
    --print               Output the list of requirements in the standard output
    --force               Overwrite existing requirements.txt
"""
from __future__ import print_function, absolute_import
import os
import sys
import re
import logging
import codecs
import ast
import traceback
from docopt import docopt
import requests
from yarg import json2package
from yarg.exceptions import HTTPError

from pipreqs import __version__

REGEXP = [
    re.compile(r'^import (.+)$'),
    re.compile(r'^from ((?!\.+).*?) import (?:.*)$')
]

if sys.version_info[0] > 2:
    open_func = open
else:
    open_func = codecs.open


def get_all_imports(path, encoding=None, extra_ignore_dirs=None):
    imports = set()
    raw_imports = set()
    candidates = []
    ignore_errors = False
    ignore_dirs = [".hg", ".svn", ".git", ".tox", "__pycache__", "env", "venv"]

    if extra_ignore_dirs:
        ignore_dirs_parsed = []
        for e in extra_ignore_dirs:
            ignore_dirs_parsed.append(os.path.basename(os.path.realpath(e)))
        ignore_dirs.extend(ignore_dirs_parsed)

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        candidates.append(os.path.basename(root))
        files = [fn for fn in files if os.path.splitext(fn)[1] == ".py"]

        candidates += [os.path.splitext(fn)[0] for fn in files]
        for file_name in files:
            with open_func(os.path.join(root, file_name), "r", encoding=encoding) as f:
                contents = f.read()
                try:
                    tree = ast.parse(contents)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for subnode in node.names:
                                raw_imports.add(subnode.name)
                        elif isinstance(node, ast.ImportFrom):
                            raw_imports.add(node.module)
                except Exception as exc:
                    if ignore_errors:
                        traceback.print_exc(exc)
                        logging.warn("Failed on file: %s" % os.path.join(root, file_name))
                        continue
                    else:
                        logging.error("Failed on file: %s" % os.path.join(root, file_name))
                        raise exc



    # Clean up imports
    for name in [n for n in raw_imports if n]:
        # Sanity check: Name could have been None if the import statement was as from . import X
        # Cleanup: We only want to first part of the import.
        # Ex: from django.conf --> django.conf. But we only want django as an import
        cleaned_name, _, _ = name.partition('.')
        imports.add(cleaned_name)

    packages = set(imports) - set(set(candidates) & set(imports))
    logging.debug('Found packages: {0}'.format(packages))

    with open(join("stdlib"), "r") as f:
        data = [x.strip() for x in f.readlines()]
        return sorted(list(set(packages) - set(data)))


def filter_line(l):
    return len(l) > 0 and l[0] != "#"


def generate_requirements_file(path, imports):
    with open(path, "w") as out_file:
        logging.debug('Writing {num} requirements: {imports} to {file}'.format(
            num=len(imports),
            file=path,
            imports=", ".join([x['name'] for x in imports])
        ))
        fmt = '{name}=={version}'
        out_file.write('\n'.join(fmt.format(**item) if item['version'] else '{name}'.format(**item)
                                 for item in imports) + '\n')

def output_requirements(imports):
    logging.debug('Writing {num} requirements: {imports} to stdout'.format(
        num=len(imports),
        imports=", ".join([x['name'] for x in imports])
    ))
    fmt = '{name}=={version}'
    print('\n'.join(fmt.format(**item) if item['version'] else '{name}'.format(**item)
                             for item in imports))

def get_imports_info(imports, pypi_server="https://pypi.python.org/pypi/", proxy=None):
    result = []

    for item in imports:
        try:
            response = requests.get("{0}{1}/json".format(pypi_server, item), proxies=proxy)
            if response.status_code == 200:
                if hasattr(response.content, 'decode'):
                    data = json2package(response.content.decode())
                else:
                    data = json2package(response.content)
            elif response.status_code >= 300:
                raise HTTPError(status_code=response.status_code,
                                reason=response.reason)
        except HTTPError:
            logging.debug(
                'Package %s does not exist or network problems', item)
            continue
        result.append({'name': item, 'version': data.latest_release_id})
    return result


def get_locally_installed_packages(encoding=None):
    packages = {}
    ignore = ["tests", "_tests", "egg", "EGG", "info"]
    for path in sys.path:
        for root, dirs, files in os.walk(path):
            for item in files:
                if "top_level" in item:
                    with open_func(os.path.join(root, item), "r", encoding=encoding) as f:
                        package = root.split(os.sep)[-1].split("-")
                        try:
                            package_import = f.read().strip().split("\n")
                        except:
                            continue
                        for i_item in package_import:
                            if ((i_item not in ignore) and
                                    (package[0] not in ignore)):
                                version = None
                                if len(package) > 1:
                                    version = package[1].replace(
                                        ".dist", "").replace(".egg", "")

                                packages[i_item] = {
                                    'version': version,
                                    'name': package[0]
                                }
    return packages


def get_import_local(imports, encoding=None):
    local = get_locally_installed_packages()
    result = []
    for item in imports:
        if item.lower() in local:
            result.append(local[item.lower()])
    return result


def get_pkg_names(pkgs):
    result = []
    with open(join("mapping"), "r") as f:
        data = [x.strip().split(":") for x in f.readlines()]
        for pkg in pkgs:
            toappend = pkg
            for item in data:
                if item[0] == pkg:
                    toappend = item[1]
                    break
            if toappend not in result:
                result.append(toappend)
    return result


def get_name_without_alias(name):
    if "import " in name:
        match = REGEXP[0].match(name.strip())
        if match:
            name = match.groups(0)[0]
    return name.partition(' as ')[0].partition('.')[0].strip()


def join(f):
    return os.path.join(os.path.dirname(__file__), f)


def init(args):
    encoding = args.get('--encoding')
    extra_ignore_dirs = args.get('--ignore')

    if extra_ignore_dirs:
        extra_ignore_dirs = extra_ignore_dirs.split(',')

    candidates = get_all_imports(args['<path>'], 
                                 encoding=encoding,
                                 extra_ignore_dirs = extra_ignore_dirs)
    candidates = get_pkg_names(candidates)
    logging.debug("Found imports: " + ", ".join(candidates))
    pypi_server = "https://pypi.python.org/pypi/"
    proxy = None
    if args["--pypi-server"]:
        pypi_server = args["--pypi-server"]

    if args["--proxy"]:
        proxy = {'http': args["--proxy"], 'https': args["--proxy"]}

    if args["--use-local"]:
        logging.debug(
            "Getting package information ONLY from local installation.")
        imports = get_import_local(candidates, encoding=encoding)
    else:
        logging.debug("Getting packages information from Local/PyPI")
        local = get_import_local(candidates, encoding=encoding)
        # Get packages that were not found locally
        difference = [x for x in candidates
                      if x.lower() not in [z['name'].lower() for z in local]]
        imports = local + get_imports_info(difference,
                                           proxy=proxy,
                                           pypi_server=pypi_server)

    path = (args["--savepath"] if args["--savepath"] else
            os.path.join(args['<path>'], "requirements.txt"))

    if not args["--print"] and not args["--savepath"] and not args["--force"] and os.path.exists(path):
        logging.warning("Requirements.txt already exists, "
                        "use --force to overwrite it")
        return
    if args["--print"]:
        output_requirements(imports)
        logging.info("Successfully output requirements")
    else:
        generate_requirements_file(path, imports)
        logging.info("Successfully saved requirements file in " + path)


def main():  # pragma: no cover
    args = docopt(__doc__, version=__version__)
    log_level = logging.DEBUG if args['--debug'] else logging.INFO
    logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s')

    try:
        init(args)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()  # pragma: no cover
