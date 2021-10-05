#!/usr/bin/env python

import os
import copy
import random
import crossinglib


#===================
#===================
def questionContent(gene_id):
	question = ''
	question += '<p>Above are the phenotypic results from a dihybrid cross and double heterozygote test cross. '
	question += 'The phenotypes were '
	ratio = crossinglib.gene_type_ratios[gene_id]
	counts = ratio.split(':')
	for count in counts:
		question += '{0} to '.format(crossinglib.num2word[int(count)])
	question = question[:-4]
	question += ' ({0}).</p>'.format(ratio)
	question += '<p><strong>What type of gene interaction is being shown?</strong></p>'
	print(question)
	return question


#===================
#===================
def makeQuestion(gene_id, color_set, letter1, letter2):
	assigned_colors = crossinglib.dihybridAssignColors(gene_id, color_set)
	dihybrid_table = crossinglib.createDiHybridTable(letter1, letter2, assigned_colors)
	testcross_table = crossinglib.createTestCrossTable(letter1, letter2, assigned_colors)

	# write the question content
	question = questionContent(gene_id)

	complete_question = '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	complete_question += ' <tr><td> '
	complete_question += dihybrid_table
	complete_question += ' </td><td> '
	complete_question += '&nbsp;'
	complete_question += ' </td><td> '
	complete_question += testcross_table
	complete_question += '</td></tr></table> '

	complete_question += " <br/> "
	complete_question += question

	print(complete_question)
	return complete_question


#===================
#===================
def writeQuestion(gene_id, color_set, file_handle):
	# make the question
	letter_pool = copy.copy(crossinglib.gene_letters)
	random.shuffle(letter_pool)
	two_letters = [letter_pool.pop(), letter_pool.pop()]
	two_letters.sort()
	letter1 = two_letters[0]
	letter2 = two_letters[1]
	complete_question = makeQuestion(gene_id, color_set, letter1, letter2)

	# write the question
	choice_letters = "ABCDEFGHI"
	file_handle.write("MC\t{0}".format(complete_question))
	answer = gene_id
	gene_ids = list(crossinglib.gene_interaction_names.keys())
	random.shuffle(gene_ids)
	for k, sub_gene_id in enumerate(gene_ids):
		if sub_gene_id == answer:
			prefix = "*"
			status = "Correct"
		else:
			prefix = ""
			status = "Incorrect"
		name = crossinglib.gene_interaction_names[sub_gene_id]
		description = crossinglib.gene_type_description[sub_gene_id]
		choice_text = "These two genes show <strong>{0}</strong>. {1}.".format(name, description)
		file_handle.write("\t{0}\t{1}".format(choice_text, status))
		print("{0}{1}. {2}".format(prefix, choice_letters[k], choice_text))
	file_handle.write("\n")

#===================
#===================
#===================
#===================
if __name__ == '__main__':
	duplicates = 2
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	file_handle = open(outfile, 'w')
	for i in range(duplicates):
		for gene_id in crossinglib.gene_interaction_names:
			for color_set in crossinglib.get_four_color_sets():
				writeQuestion(gene_id, color_set, file_handle)
			#sys.exit(1)
	file_handle.close()
