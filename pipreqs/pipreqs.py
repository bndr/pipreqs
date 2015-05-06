#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pipreqs - Generate pip requirements.txt file based on imports

Usage:
    pipreqs [options] <path>

Options:
    --use-local         Use ONLY local package information instead of querying PyPI
    --debug             Print debug information
    --savepath <file>   Save the list of requirements in the given file
"""
from __future__ import print_function
import os
import sys
from distutils.sysconfig import get_python_lib
import re
import logging

from docopt import docopt
import yarg
from yarg.exceptions import HTTPError


REGEXP = [
    re.compile(r'^import (.+)$'),
    re.compile(r'^from ((?!\.+).*?) import (?:.*)$')
]


def get_all_imports(start_path):
    imports = []
    packages = []
    logging.debug('Traversing tree, start: {0}'.format(start_path))
    for root, dirs, files in os.walk(start_path):
        packages.append(os.path.basename(root))
        files = [fn for fn in files if os.path.splitext(fn)[1] == ".py"]
        packages += [os.path.splitext(fn)[0] for fn in files]
        for file_name in files:
            with open(os.path.join(root, file_name), "r") as file_object:
                lines = filter(
                    lambda l: len(l) > 0, map(lambda l: l.strip(), file_object))
                for line in lines:
                    if line[0] == "#":
                        continue
                    if "(" in line:
                        break
                    for rex in REGEXP:
                        s = rex.match(line)
                        if not s:
                            continue
                        for item in s.groups():
                            if "," in item:
                                for match in item.split(","):
                                    imports.append(match.strip())
                            else:
                                to_append = item.partition(
                                    ' as ')[0].partition('.')[0]
                                imports.append(to_append.strip())
    third_party_packages = set(imports) - set(set(packages) & set(imports))
    logging.debug(
        'Found third-party packages: {0}'.format(third_party_packages))
    with open(os.path.join(os.path.dirname(__file__), "stdlib"), "r") as f:
        data = [x.strip() for x in f.readlines()]
        return sorted(list(set(third_party_packages) - set(data)))


def generate_requirements_file(path, imports):
    with open(path, "w") as out_file:
        logging.debug('Writing {num} requirements to {file}'.format(
            num=len(imports),
            file=path
        ))
        fmt = '{name} == {version}'
        out_file.write('\n'.join(fmt.format(**item)
                                 for item in imports) + '\n')


def get_imports_info(imports):
    result = []
    for item in imports:
        try:
            data = yarg.get(item)
        except HTTPError:
            logging.debug('Package does not exist or network problems')
            continue
        if not data or not data.release_ids:
            continue
        last_release = data.latest_release_id
        result.append({'name': item, 'version': last_release})
    return result


def get_locally_installed_packages():
    path = get_python_lib()
    packages = {}
    for root, dirs, files in os.walk(path):
        for item in files:
            if "top_level" in item:
                with open(os.path.join(root, item), "r") as f:
                    package = root.split("/")[-1].split("-")
                    package_import = f.read().strip().split("\n")
                    package_import_name = ""
                    for item in package_import:
                        if item not in ["tests", "_tests"]:
                            package_import_name = item
                            break
                    if package_import_name == "":
                        logging.debug(
                            'Could not determine import name for package ' + package_import)
                    else:
                        packages[package_import_name] = {
                            'version': package[1].replace(".dist", ""),
                            'name': package[0]
                        }
    return packages


def get_import_local(imports):
    local = get_locally_installed_packages()
    result = []
    for item in imports:
        if item in local:
            result.append(local[item])
    return result


def init(args):
    print("Looking for imports")
    imports = get_all_imports(args['<path>'])
    print("Found third-party imports: " + ", ".join(imports))
    if args['--use-local']:
        print(
            "Getting package version information ONLY from local installation.")
        imports_with_info = get_import_local(imports)
    else:
        print(
            "Getting latest version information about packages from Local/PyPI")
        imports_local = get_import_local(imports)
        difference = [x for x in imports if x not in [z['name']
                                                      for z in imports_local]]
        imports_pypi = get_imports_info(difference)
        imports_with_info = imports_local + imports_pypi
    print("Imports written to requirements file:", ", ".join(
        [x['name'] for x in imports_with_info]))
    path = args[
        "--savepath"] if args["--savepath"] else os.path.join(args['<path>'], "requirements.txt")
    generate_requirements_file(path, imports_with_info)
    print("Successfully saved requirements file in " + path)


def main():  # pragma: no cover
    args = docopt(__doc__, version='xstat 0.1')
    log_level = logging.DEBUG if args['--debug'] else logging.WARNING
    logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s')

    try:
        init(args)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()  # pragma: no cover
