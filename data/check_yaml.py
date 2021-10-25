#!/usr/bin/env python

import sys
import yaml
import pprint

#=======================
def readYamlFile(yaml_file):
	yaml_pointer = open(yaml_file, 'r')
	data = yaml.safe_load(yaml_pointer)
	yaml_pointer.close()
	return data


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage file.py <yaml_file.yml>")
	yaml_file = sys.argv[1]
	data = readYamlFile(yaml_file)
	pprint.pprint(data)
