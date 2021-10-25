#!/usr/bin/env python

import os
import re
import sys
import copy
import yaml
import random

#sample question:
#  A man (&male;) with both hemophilia and Huntington's disease marries
#    a normal phenotype woman (&female;) without either disease.
#  The man's (&male;) father also had Huntington's disease, but not his mother.
#  The woman's (&female;) father suffered from hemophilia, but her mother did not.
#  Huntington's disease is autosomal dominant, and hemophilia is X-linked recessive.

# step 1: pick a dominant disease
# step 2: pick a X-linked disease; mother is a carrier

#easy, ask the genotype of one of the individuals
#hard, ask a compounded question: What fraction of their sons (&male;) will suffer from Huntington's disease AND hemophilia?
#hard, ask a compounded question: What fraction of their daughters (&female;) will suffer from Huntington's disease AND hemophilia?

#A. None, 0%
#B. 1/4, 25%
#C. 1/2, 50%
#D. 3/4, 75%
#E. All, 100%

#=====================
#=====================
#=====================
class MultiDisorderClass(object):
	#=====================
	def __init__(self):
		yaml_data_file = '../data/genetic_disorders.yml'
		raw_disorder_data = self.readYaml(yaml_data_file)
		self.disorder_data = self.filterDisorderData(raw_disorder_data)
		pass

	#=====================
	def readYaml(self, yaml_file):
		yaml_pointer = open(yaml_file, 'r')
		data = yaml.safe_load(yaml_pointer)
		yaml_pointer.close()
		return data

	#=====================
	def filterDisorderData(self, raw_disorder_data_dict):
		# goal is to remove disorders that are NOT complete
		disorder_data = {}
		complete_disorder_count = 0
		all_disorder_count = 0
		#print(raw_disorder_data_dict.keys())
		for disorder_type_name in raw_disorder_data_dict.keys():
			disorder_type_dict = raw_disorder_data_dict[disorder_type_name]
			disorder_data[disorder_type_name] = {}
			#print(disorder_type_dict.keys())
			for disorder_name in disorder_type_dict.keys():
				all_disorder_count += 1
				disorder_dict = disorder_type_dict[disorder_name]
				if disorder_dict['complete'] is True:
					complete_disorder_count += 1
					print('{0:02d}. {1} - {2}'.format(complete_disorder_count, disorder_name.title(), disorder_type_name.title()))
					disorder_data[disorder_type_name][disorder_name] = disorder_dict
					disorder_data[disorder_type_name][disorder_name]['name'] = disorder_name
					disorder_data[disorder_type_name][disorder_name]['type'] = disorder_type_name
		#import pprint
		#pprint.pprint(disorder_data)
		print("Processed {0} of {1} disorders that were complete".format(complete_disorder_count, all_disorder_count))
		return disorder_data

	#=====================
	def capitalFirstLetterOnly(self, string):
		# python str.capitalize() make all other characters lowercase, and is not desired
		new_string = string[0].upper() + string[1:]
		return new_string

	#=====================
	def breakUpGeneLocus(self, locus):
		locus_dict = {}
		if 'p' in locus:
			locus_dict['arm'] = 'short'
			split_list = locus.split('p')
		elif 'q' in locus:
			locus_dict['arm'] = 'long'
			split_list = locus.split('q')
		locus_dict['chromosome'] = split_list[0]
		band = split_list[1]
		band = re.sub('\-.*$', '', band)
		locus_dict['band'] = band
		return locus_dict

	#=====================
	def getDisorderShortName(self, disorder_dict):
		if disorder_dict.get('abbreviation') is not None:
			shortest_name = disorder_dict['abbreviation']
		elif disorder_dict.get('short name') is not None:
			shortest_name = disorder_dict['short name']
		else:
			shortest_name = disorder_dict['name']
		return shortest_name

	#=====================
	def getDisorderParagraph(self, disorder_dict):
		description = ''
		shortest_name = None
		description += '<strong>' + self.capitalFirstLetterOnly(disorder_dict['name']) + " "
		if disorder_dict.get('abbreviation') is not None:
			description += "(" + disorder_dict['abbreviation'] + ") "
		shortest_name = self.getDisorderShortName(disorder_dict)


		description += '</strong> is an ' + disorder_dict['type'] + " genetic disorder "

		description += 'that is caused by ' + disorder_dict['caused by'] + ". "

		description += 'This results in ' + disorder_dict['mechanism'] + ". "
		
		description += 'The disorder affects ' + disorder_dict['frequency'] + '. ' 
		
		description += 'Individuals affected with ' + shortest_name + ' have ' + disorder_dict['symptoms'] + ". "

		locus_dict = self.breakUpGeneLocus(disorder_dict['locus'])
		description += 'The defective gene for ' + shortest_name + ' is located on the ' + locus_dict['arm'] + ' arm of '
		description += 'chromosome ' + locus_dict['chromosome'] + ' at position ' + locus_dict['band']  + ". "

		
		return description
	#=====================
	def randomDisorderDict(self, disorder_type=None):
		while disorder_type is None:
			disorder_type = random.choice(list(self.disorder_data.keys()))
			if len(self.disorder_data[disorder_type].keys()) == 0:
				disorder_type = None
		disorder_name = random.choice(list(self.disorder_data[disorder_type].keys()))
		disorder_dict = md.disorder_data[disorder_type][disorder_name]
		return disorder_dict

	#=====================
	def getStandardChoicesList(self):
		choices_list = ['None, 0%', '1/4, 25%', '1/2, 50%', '3/4, 75%', 'All, 100%']
		return choices_list

	#=====================
	def makeQuestionPretty(self, question):
		pretty_question = copy.copy(question)
		pretty_question = re.sub('\<\/p\>\s*\<p\>', '\n\n', pretty_question)
		return pretty_question


	#=====================
	def formatBB_Question(self, N, question, choices_list, answer):
		bb_question = ''

		number = "{0}. ".format(N)
		bb_question += 'MC\t<p>{0}. {1}'.format(N, question)
		pretty_question = self.makeQuestionPretty(question)
		print('{0}. {1}'.format(N, pretty_question))

		letters = 'ABCDEFGH'
		for i, choice in enumerate(choices_list):
			bb_question += '\t{0}'.format(choice)
			if choice == answer:
				prefix = 'x'
				bb_question += '\tCorrect'
			else:
				prefix = ' '
				bb_question += '\tIncorrect'
			print("- [{0}] {1}. {2}".format(prefix, letters[i], choice))
		print("")
		return bb_question

#=====================
#=====================
#=====================
if __name__ == '__main__':
	md = MultiDisorderClass()
	for i in range(2):
		disorder_dict = md.randomDisorderDict('X-linked recessive')
		description = md.getDisorderParagraph(disorder_dict)
		print(description)
		print("")
		disorder_dict = md.randomDisorderDict('autosomal dominant')
		description = md.getDisorderParagraph(disorder_dict)
		print(description)
		print("")
