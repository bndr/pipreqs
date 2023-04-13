#!/usr/bin/env python
"""pipreqs - Generate pip requirements.txt file based on imports

Usage:
    pipreqs [options] [<path>]

Arguments:
    <path>                The path to the directory containing the application
                          files for which a requirements file should be
                          generated (defaults to the current working
                          directory).

Options:
    --use-local           Use ONLY local package info instead of querying PyPI.
    --pypi-server <url>   Use custom PyPi server.
    --proxy <url>         Use Proxy, parameter will be passed to requests
                          library. You can also just set the environments
                          parameter in your terminal:
                          $ export HTTP_PROXY="http://10.10.1.10:3128"
                          $ export HTTPS_PROXY="https://10.10.1.10:1080"
    --debug               Print debug information
    --ignore <dirs>...    Ignore extra directories, each separated by a comma
    --no-follow-links     Do not follow symbolic links in the project
    --encoding <charset>  Use encoding parameter for file open
    --savepath <file>     Save the list of requirements in the given file
    --print               Output the list of requirements in the standard
                          output
    --force               Overwrite existing requirements.txt
    --diff <file>         Compare modules in requirements.txt to project
                          imports
    --clean <file>        Clean up requirements.txt by removing modules
                          that are not imported in project
    --mode <scheme>       Enables dynamic versioning with <compat>,
                          <gt> or <non-pin> schemes.
                          <compat> | e.g. Flask~=1.1.2
                          <gt>     | e.g. Flask>=1.1.2
                          <no-pin> | e.g. Flask
"""
from contextlib import contextmanager
import os
import sys
import re
import logging
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


@contextmanager
def _open(filename=None, mode='r'):
    """Open a file or ``sys.stdout`` depending on the provided filename.

    Args:
        filename (str): The path to the file that should be opened. If
            ``None`` or ``'-'``, ``sys.stdout`` or ``sys.stdin`` is
            returned depending on the desired mode. Defaults to ``None``.
        mode (str): The mode that should be used to open the file.

    Yields:
        A file handle.

    """
    if not filename or filename == '-':
        if not mode or 'r' in mode:
            file = sys.stdin
        elif 'w' in mode:
            file = sys.stdout
        else:
            raise ValueError('Invalid mode for file: {}'.format(mode))
    else:
        file = open(filename, mode)

    try:
        yield file
    finally:
        if file not in (sys.stdin, sys.stdout):
            file.close()


def get_all_imports(
        path, encoding=None, extra_ignore_dirs=None, follow_links=True):
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

    walk = os.walk(path, followlinks=follow_links)
    for root, dirs, files in walk:
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        candidates.append(os.path.basename(root))
        files = [fn for fn in files if os.path.splitext(fn)[1] == ".py"]

        candidates += [os.path.splitext(fn)[0] for fn in files]
        for file_name in files:
            file_name = os.path.join(root, file_name)
            with open(file_name, "r", encoding=encoding) as f:
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
                    logging.warn("Failed on file: %s" % file_name)
                    continue
                else:
                    logging.error("Failed on file: %s" % file_name)
                    raise exc

    # Clean up imports
    for name in [n for n in raw_imports if n]:
        # Sanity check: Name could have been None if the import
        # statement was as ``from . import X``
        # Cleanup: We only want to first part of the import.
        # Ex: from django.conf --> django.conf. But we only want django
        # as an import.
        cleaned_name, _, _ = name.partition('.')
        imports.add(cleaned_name)

    packages = imports - (set(candidates) & imports)
    logging.debug('Found packages: {0}'.format(packages))

    with open(join("stdlib"), "r") as f:
        data = {x.strip() for x in f}

    return list(packages - data)


def filter_line(line):
    return len(line) > 0 and line[0] != "#"


def generate_requirements_file(path, imports, symbol):
    with _open(path, "w") as out_file:
        logging.debug('Writing {num} requirements: {imports} to {file}'.format(
            num=len(imports),
            file=path,
            imports=", ".join([x['name'] for x in imports])
        ))
        fmt = '{name}' + symbol + '{version}'
        out_file.write('\n'.join(
            fmt.format(**item) if item['version'] else '{name}'.format(**item)
            for item in imports) + '\n')


def output_requirements(imports, symbol):
    generate_requirements_file('-', imports, symbol)


def get_imports_info(
        imports, pypi_server="https://pypi.python.org/pypi/", proxy=None):
    result = []

    for item in imports:
        try:
            logging.warning(
                'Import named "%s" not found locally. '
                'Trying to resolve it at the PyPI server.',
                item
            )
            response = requests.get(
                "{0}{1}/json".format(pypi_server, item), proxies=proxy)
            if response.status_code == 200:
                if hasattr(response.content, 'decode'):
                    data = json2package(response.content.decode())
                else:
                    data = json2package(response.content)
            elif response.status_code >= 300:
                raise HTTPError(status_code=response.status_code,
                                reason=response.reason)
        except HTTPError:
            logging.warning(
                'Package "%s" does not exist or network problems', item)
            continue
        logging.warning(
            'Import named "%s" was resolved to "%s:%s" package (%s).\n'
            'Please, verify manually the final list of requirements.txt '
            'to avoid possible dependency confusions.',
            item,
            data.name,
            data.latest_release_id,
            data.pypi_url
        )
        result.append({'name': item, 'version': data.latest_release_id})
    return result


def get_locally_installed_packages(encoding=None):
    packages = []
    ignore = ["tests", "_tests", "egg", "EGG", "info"]
    for path in sys.path:
        for root, dirs, files in os.walk(path):
            for item in files:
                if "top_level" in item:
                    item = os.path.join(root, item)
                    with open(item, "r", encoding=encoding) as f:
                        package = root.split(os.sep)[-1].split("-")
                        try:
                            top_level_modules = f.read().strip().split("\n")
                        except:  # NOQA
                            # TODO: What errors do we intend to suppress here?
                            continue

                        # filter off explicitly ignored top-level modules
                        # such as test, egg, etc.
                        filtered_top_level_modules = list()

                        for module in top_level_modules:
                            if (
                                (module not in ignore) and
                                (package[0] not in ignore)
                            ):
                                # append exported top level modules to the list
                                filtered_top_level_modules.append(module)

                        version = None
                        if len(package) > 1:
                            version = package[1].replace(
                                ".dist", "").replace(".egg", "")

                        # append package: top_level_modules pairs
                        # instead of top_level_module: package pairs
                        packages.append({
                            'name': package[0],
                            'version': version,
                            'exports': filtered_top_level_modules
                        })
    return packages


def get_import_local(imports, encoding=None):
    local = get_locally_installed_packages()
    result = []
    for item in imports:
        # search through local packages
        for package in local:
            # if candidate import name matches export name
            # or candidate import name equals to the package name
            # append it to the result
            if item in package['exports'] or item == package['name']:
                result.append(package)

    # removing duplicates of package/version
    # had to use second method instead of the previous one,
    # because we have a list in the 'exports' field
    # https://stackoverflow.com/questions/9427163/remove-duplicate-dict-in-list-in-python
    result_unique = [i for n, i in enumerate(result) if i not in result[n+1:]]

    return result_unique


def get_pkg_names(pkgs):
    """Get PyPI package names from a list of imports.

    Args:
        pkgs (List[str]): List of import names.

    Returns:
        List[str]: The corresponding PyPI package names.

    """
    result = set()
    with open(join("mapping"), "r") as f:
        data = dict(x.strip().split(":") for x in f)
    for pkg in pkgs:
        # Look up the mapped requirement. If a mapping isn't found,
        # simply use the package name.
        result.add(data.get(pkg, pkg))
    # Return a sorted list for backward compatibility.
    return sorted(result, key=lambda s: s.lower())


def get_name_without_alias(name):
    if "import " in name:
        match = REGEXP[0].match(name.strip())
        if match:
            name = match.groups(0)[0]
    return name.partition(' as ')[0].partition('.')[0].strip()


def join(f):
    return os.path.join(os.path.dirname(__file__), f)


def parse_requirements(file_):
    """Parse a requirements formatted file.

    Traverse a string until a delimiter is detected, then split at said
    delimiter, get module name by element index, create a dict consisting of
    module:version, and add dict to list of parsed modules.

    Args:
        file_: File to parse.

    Raises:
        OSerror: If there's any issues accessing the file.

    Returns:
        tuple: The contents of the file, excluding comments.
    """
    modules = []
    # For the dependency identifier specification, see
    # https://www.python.org/dev/peps/pep-0508/#complete-grammar
    delim = ["<", ">", "=", "!", "~"]

    try:
        f = open(file_, "r")
    except OSError:
        logging.error("Failed on file: {}".format(file_))
        raise
    else:
        try:
            data = [x.strip() for x in f.readlines() if x != "\n"]
        finally:
            f.close()

    data = [x for x in data if x[0].isalpha()]

    for x in data:
        # Check for modules w/o a specifier.
        if not any([y in x for y in delim]):
            modules.append({"name": x, "version": None})
        for y in x:
            if y in delim:
                module = x.split(y)
                module_name = module[0]
                module_version = module[-1].replace("=", "")
                module = {"name": module_name, "version": module_version}

                if module not in modules:
                    modules.append(module)

                break

    return modules


def compare_modules(file_, imports):
    """Compare modules in a file to imported modules in a project.

    Args:
        file_ (str): File to parse for modules to be compared.
        imports (tuple): Modules being imported in the project.

    Returns:
        tuple: The modules not imported in the project, but do exist in the
               specified file.
    """
    modules = parse_requirements(file_)

    imports = [imports[i]["name"] for i in range(len(imports))]
    modules = [modules[i]["name"] for i in range(len(modules))]
    modules_not_imported = set(modules) - set(imports)

    return modules_not_imported


def diff(file_, imports):
    """Display the difference between modules in a file and imported modules."""  # NOQA
    modules_not_imported = compare_modules(file_, imports)

    logging.info(
        "The following modules are in {} but do not seem to be imported: "
        "{}".format(file_, ", ".join(x for x in modules_not_imported)))


def clean(file_, imports):
    """Remove modules that aren't imported in project from file."""
    modules_not_imported = compare_modules(file_, imports)

    if len(modules_not_imported) == 0:
        logging.info("Nothing to clean in " + file_)
        return

    re_remove = re.compile("|".join(modules_not_imported))
    to_write = []

    try:
        f = open(file_, "r+")
    except OSError:
        logging.error("Failed on file: {}".format(file_))
        raise
    else:
        try:
            for i in f.readlines():
                if re_remove.match(i) is None:
                    to_write.append(i)
            f.seek(0)
            f.truncate()

            for i in to_write:
                f.write(i)
        finally:
            f.close()

    logging.info("Successfully cleaned up requirements in " + file_)


def dynamic_versioning(scheme, imports):
    """Enables dynamic versioning with <compat>, <gt> or <non-pin> schemes."""
    if scheme == "no-pin":
        imports = [{"name": item["name"], "version": ""} for item in imports]
        symbol = ""
    elif scheme == "gt":
        symbol = ">="
    elif scheme == "compat":
        symbol = "~="
    return imports, symbol


def init(args):
    encoding = args.get('--encoding')
    extra_ignore_dirs = args.get('--ignore')
    follow_links = not args.get('--no-follow-links')
    input_path = args['<path>']
    if input_path is None:
        input_path = os.path.abspath(os.curdir)

    if extra_ignore_dirs:
        extra_ignore_dirs = extra_ignore_dirs.split(',')

    path = (args["--savepath"] if args["--savepath"] else
            os.path.join(input_path, "requirements.txt"))
    if (not args["--print"]
            and not args["--savepath"]
            and not args["--force"]
            and os.path.exists(path)):
        logging.warning("requirements.txt already exists, "
                        "use --force to overwrite it")
        return

    candidates = get_all_imports(input_path,
                                 encoding=encoding,
                                 extra_ignore_dirs=extra_ignore_dirs,
                                 follow_links=follow_links)
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

        # check if candidate name is found in
        # the list of exported modules, installed locally
        # and the package name is not in the list of local module names
        # it add to difference
        difference = [x for x in candidates if
                      # aggregate all export lists into one
                      # flatten the list
                      # check if candidate is in exports
                      x.lower() not in [y for x in local for y in x['exports']]
                      and
                      # check if candidate is package names
                      x.lower() not in [x['name'] for x in local]]

        imports = local + get_imports_info(difference,
                                           proxy=proxy,
                                           pypi_server=pypi_server)
    # sort imports based on lowercase name of package, similar to `pip freeze`.
    imports = sorted(imports, key=lambda x: x['name'].lower())

    if args["--diff"]:
        diff(args["--diff"], imports)
        return

    if args["--clean"]:
        clean(args["--clean"], imports)
        return

    if args["--mode"]:
        scheme = args.get("--mode")
        if scheme in ["compat", "gt", "no-pin"]:
            imports, symbol = dynamic_versioning(scheme, imports)
        else:
            raise ValueError("Invalid argument for mode flag, "
                             "use 'compat', 'gt' or 'no-pin' instead")
    else:
        symbol = "=="

    if args["--print"]:
        output_requirements(imports, symbol)
        logging.info("Successfully output requirements")
    else:
        generate_requirements_file(path, imports, symbol)
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
