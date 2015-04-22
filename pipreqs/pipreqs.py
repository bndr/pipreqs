#!/usr/bin/python
# -*- coding: utf-8 -*-
"""pipreqs - Generate pip requirements.txt file based on imports

Usage:
	pipreqs <path>
	pipreqs <path>[options]

Options:
    --debug  prints debug information.
    --savepath path to requirements.txt (Optional)
"""
import os, re, logging
from docopt import docopt
import yarg

REGEXP = [re.compile(r'import ([a-zA-Z123456789]+)'),re.compile(r'from (.*?) import (?:.*)')]

def get_all_imports(start_path):
	imports = []
	packages = []
	for root, dirs, files in os.walk(start_path):
	    path = root.split('/')
	    packages.append(os.path.basename(root))       
	    for file in files:
	    	if file[-3:] != ".py":
	    		continue
	    	for rex in REGEXP:
	    		with open(root + "/" + file, "r") as f:
	    			s = rex.match(f.read())
	    			if s:
	    				for item in s.groups():
	    					if "." in item:
	    						imports.append(item.split(".")[0])
	    					else:
	    						imports.append(item)
	local_packages =  list(set(packages) & set(imports))
	third_party_packages = list(set(imports) - set(local_packages))
	with open(os.path.dirname(__file__)+"/stdlib", "r") as f:
		data = [x.strip() for x in f.readlines()]
		return list(set(third_party_packages) - set(data))

def generate_requirements_file(path, imports):
	with open(path, "w") as ff:
		for item in imports:
			ff.write(item['name'])
			ff.write("==")
			ff.write(item['version'])
			ff.write("\n")

def get_imports_info(imports):
	result = []
	for item in imports:
		data = yarg.get(item)
		if not data or len(data.release_ids) < 1:
			continue
		last_release = data.release_ids[-1]
		result.append({'name':item,'version':last_release})
	return result

def init(args):
	imports = get_all_imports(args['<path>'])
	imports_with_info = get_imports_info(imports)
	path = args["--savepath"] if args["--savepath"] else os.path.join(args['<path>'],"requirements.txt")
	generate_requirements_file(path, imports_with_info)

def main():
    args = docopt(__doc__, version='xstat 0.1')
    log_level = logging.WARNING
    if args['--debug']:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s')

    try:
        init(args)
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    main()