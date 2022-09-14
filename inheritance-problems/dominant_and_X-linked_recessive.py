#!/usr/bin/env python3

import os
import re
import sys
import yaml
import random
import disorderlib

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
if __name__ == '__main__':
	N = 0
	md = disorderlib.MultiDisorderClass()
	choices_list = md.getStandardChoicesList()
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	file_handle = open(outfile, 'w')
	for XLR_disorder_name, XLR_disorder_dict in md.disorder_data['X-linked recessive'].items():
		XLR_description = md.getDisorderParagraph(XLR_disorder_dict)
		XLR_short_name = md.getDisorderShortName(XLR_disorder_dict)
		#print("============")
		#print(XLR_description)
		#print("")
		
		for AD_disorder_name, AD_disorder_dict in md.disorder_data['autosomal dominant'].items():
			AD_description = md.getDisorderParagraph(AD_disorder_dict)
			AD_short_name = md.getDisorderShortName(AD_disorder_dict)
			#print(AD_description)
			#print("")

			base_question = ''
			base_question += '<p>' + XLR_description + '</p>'
			base_question += '<p>' + AD_description + '</p>'
			base_question += '<p>A man (&male;) with both {0} and {1} genetic disorders marries '.format(XLR_short_name, AD_short_name)
			base_question += 'a wild-type phenotype woman (&female;) with neither disorder. '
			base_question += 'The father (&male;) of the woman has the {0} genetic disorder, but mother (&female;) of the woman does not. '.format(XLR_short_name)
			parent = random.choice(('father (&male;)', 'mother (&female;)'))
			base_question += 'The {0} of the man is wild-type phenotype and does not have the {1} genetic disorder.</p> '.format(parent, AD_short_name)

			base_question += '<p>Reminder: {0} is {1} and {2} is {3}.</p>'.format(
				XLR_short_name, XLR_disorder_dict['type'],
				AD_short_name, AD_disorder_dict['type'])
			
			N += 1
			question = base_question + '<p>What fraction of their daughters (&female;) will have both {0} and {1} genetic disorders?</p>'.format(XLR_short_name, AD_short_name)
			answer = '1/4, 25%'
			bb_question = md.formatBB_Question(N, question, choices_list, answer)
			file_handle.write(bb_question)
			file_handle.write('\n')

			N += 1
			question = base_question + '<p>What fraction of their sons (&male;) will have both {0} and {1} genetic disorders?</p>'.format(XLR_short_name, AD_short_name)
			answer = '1/4, 25%'
			bb_question = md.formatBB_Question(N, question, choices_list, answer)
			file_handle.write(bb_question)
			file_handle.write('\n')

	file_handle.close()
	print('wrote {0} questions to file {1}'.format(N, outfile))
