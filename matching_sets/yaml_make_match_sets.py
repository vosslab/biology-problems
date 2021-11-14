#!/usr/bin/env python

"""
This program creates all permutations of matching pairs

MAT TAB question text TAB answer text TAB matching text TAB answer two text TAB matching two text
"""

import os
import sys
import copy
import math
import time
import yaml
import pprint
import random
import argparse
import itertools
import crcmod.predefined

answer_histogram = {}

#=======================
# special loader with duplicate key checking
class UniqueKeyLoader(yaml.SafeLoader):
	def construct_mapping(self, node, deep=False):
		mapping = []
		for key_node, value_node in node.value:
			key = self.construct_object(key_node, deep=deep)
			if key in mapping:
				print("DUPLICATE KEY: ", key)
				raise AssertionError("DUPLICATE KEY: ", key)
			mapping.append(key)
		return super().construct_mapping(node, deep)

#=======================
def getCrc16_FromString(mystr):
	crc16 = crcmod.predefined.Crc('xmodem')
	crc16.update(mystr.encode('ascii'))
	return crc16.hexdigest().lower()

#=======================
def readYamlFile(yaml_file):
	print("Processing file: ", yaml_file)
	yaml.allow_duplicate_keys = False
	yaml_pointer = open(yaml_file, 'r')
	#data = UniqueKeyLoader(yaml_pointer)
	#help(data)
	yaml_text = yaml_pointer.read()
	data = yaml.load(yaml_text, Loader=UniqueKeyLoader)
	#data = yaml.safe_load(yaml_pointer)
	yaml_pointer.close()
	return data

#=======================
#=======================
def printAnswerHistogram():
	keys = list(answer_histogram.keys())
	keys.sort()
	for key in keys:
		print("{0}: {1}".format(key, answer_histogram[key]))


#=======================
def permuteMatchingPairs(yaml_data):
	matching_pairs_dict = yaml_data['matching pairs']

	list_of_complete_questions = []

	#MAT TAB question text TAB answer text TAB matching text TAB answer two text TAB matching two text
	#"Match the each of the following <keys> with their corresponding <values>"
	question = ("<p>Match the each of the following {0} with their corresponding {1}.</p>".format(
		yaml_data['key description'], yaml_data['value description']))
	question += '<p><i>Note:</i> all choices will be used exacly once</p>'

	all_keys = list(matching_pairs_dict.keys())
	all_combs = list(itertools.combinations(all_keys, yaml_data['items to match per question']))
	random.shuffle(all_combs)
	print('Created {0} combinations from {1} items'.format(len(all_combs), len(all_keys)))
	for comb in all_combs:
		key_list = list(comb)
		random.shuffle(key_list)
		complete_question = question
		for key in key_list:
			complete_question += '\t' + key
			complete_question += '\t' + matching_pairs_dict[key]
		list_of_complete_questions.append(complete_question)

	return list_of_complete_questions


#=======================
#=======================
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('-f', '-y', '--file', metavar='<file>', type=str, dest='input_yaml_file',
		help='yaml input file to process')
	parser.add_argument('-x', '--max-questions', metavar='<file>', type=int, dest='max_questions',
		help='yaml input file to process', default=199)
	args = parser.parse_args()

	if args.input_yaml_file is None or not os.path.isfile(args.input_yaml_file):
		print("Usage: {0} -y <input_yaml_file>".format(__file__))
		sys.exit(0)

	yaml_data = readYamlFile(args.input_yaml_file)
	pprint.pprint(yaml_data)

	list_of_complete_questions = permuteMatchingPairs(yaml_data)
	if len(list_of_complete_questions) > args.max_questions:
		print("Too many questions, trimming down to {0} questions".format(args.max_questions))
		random.shuffle(list_of_complete_questions)
		less_questions = list_of_complete_questions[:args.max_questions]
		less_questions.sort()
		list_of_complete_questions = less_questions

	outfile = 'bbq-' + os.path.splitext(os.path.basename(args.input_yaml_file))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	N = 0
	for bbformat_question in list_of_complete_questions:
		N += 1
		crc16_value = getCrc16_FromString(bbformat_question)
		#MAT TAB question text TAB answer text TAB matching text TAB answer two text TAB matching two text
		output_format = "MAT\t<p>{0:03d}. {1}</p> {2}\n".format(N, crc16_value, bbformat_question)
		f.write(output_format)
	f.close()
	printAnswerHistogram()
	print("Wrote {0} questions to file.".format(N))
