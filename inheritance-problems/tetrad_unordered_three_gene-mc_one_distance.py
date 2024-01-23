#!/usr/bin/env python3

import os
import sys
import random
import argparse

import bptools
import genemaplib as gml
import genemapclass as gmc
import pointtestcrosslib as ptcl

debug = True

#=====================
#=====================
def questionText(basetype):
	question_string = '<h6>Unordered Tetrad Three Gene Mapping</h6>'
	question_string += '<p>The yeast <i>Saccharomyces cerevisiae</i> has unordered tetrads. '
	question_string += 'A cross is made to study the linkage relationships among three genes. '
	question_string += '<p>Using the table, determine the order of the genes and the distances between them. '
	question_string += 'Once calculated, fill in the following four blanks: </p><ul>'
	question_string += '<li>The distance between genes {0} and {1} is [{0}{1}] cM ({0}{1})</li>'.format(basetype[0].upper(),basetype[1].upper())
	question_string += '<li>The distance between genes {0} and {1} is [{0}{1}] cM ({0}{1})</li>'.format(basetype[0].upper(),basetype[2].upper())
	question_string += '<li>The distance between genes {0} and {1} is [{0}{1}] cM ({0}{1})</li>'.format(basetype[1].upper(),basetype[2].upper())
	question_string += '<li>From this the correct order of the genes is [geneorder] (gene order).</li></ul>'
	question_string += '<p><i>Hint 1:</i> ALL gene distances will be whole numbers, '
	question_string += ' do NOT enter a decimal; if you have a decimal your calculations are wrong.</p>'
	question_string += '<p><i>Hint 2:</i> enter your answer in the blank using only letters or numbers '
	question_string += ' with no spaces or commas. Also, do NOT add units, e.g. cM or m.u.</p>'
	question_string += '<ul>'
	question_string += '<li>Step 1: Find the Row for the Parental Type for all three genes.</li>'
	question_string += '<li>Step 2: Pick any two genes and assign PD, NPD, TT</li>'
	question_string += '<li>Step 3: Determine if the two genes are linked.</li>'
	question_string += '<ul><li>PD >> NPD &rarr; linked; PD &approx; NPD &rarr; unlinked</li></ul>'
	question_string += '<li>Step 4: Determine the map distance between the two genes</li>'
	question_string += '<ul><li>D = &half; (TT + 6 NPD)/total = (3 NPD + &half;TT)/total</li></ul>'
	question_string += '<li>Step 5: Go to Step 2 and pick a new pair of genes until all pairs are complete.</li>'
	question_string += '</ul>'

	return question_string

#=====================
#=====================
def tetradSetToString(tetradSet):
	mystr = ("%s\t%s\t%s\t%s\t"
		%(tetradSet[0],tetradSet[1],tetradSet[2],tetradSet[3],))
	return mystr

#=====================
#=====================
def makeProgenyHtmlTable(typemap, progeny_size):
	alltypes = list(typemap.keys())
	alltypes.sort()
	td_extra = 'align="center" style="border: 1px solid black;"'
	span = '<span style="font-size: medium;">'
	table = '<table style="border-collapse: collapse; border: 2px solid black; width: 400px; height: 220px;">'
	table += '<tr>'
	table += '  <th {0}>Set #</th>'.format(td_extra)
	table += '  <th colspan="4" {0}>Tetrad Genotypes</th>'.format(td_extra)
	table += '  <th {0}>Progeny<br/>Count</th>'.format(td_extra)
	table += '</tr>'
	for i,type in enumerate(alltypes):
		interheader = '</span></td><td {0}>{1}'.format(td_extra, span)
		html_type = type.strip().replace('\t', interheader)
		table += '<tr>'
		table += ' <td {0}>{1}{2}</span></td>'.format(td_extra, span, i+1)
		table += ' <td {0}>{1}{2}</span></td>'.format(td_extra, span, html_type)
		table += ' <td {0}>{1}{2:d}</span></td>'.format(td_extra.replace('center', 'right'), span, typemap[type])
		table += '</tr>'
	table += '<tr>'
	table += '  <th colspan="5" {0}">TOTAL =</th>'.format(td_extra.replace('center', 'right'))
	table += '  <td {0}>{1:d}</td>'.format(td_extra.replace('center', 'right'), progeny_size)
	table += '</tr>'
	table += '</table>'
	return table


#=====================
#=====================
def makeProgenyAsciiTable(typemap, progeny_size):
	alltypes = list(typemap.keys())
	alltypes.sort()
	table = ''
	for type in alltypes:
		table += ("{0}\t".format(type))
		table += ("{0:d}\t".format(typemap[type]))
		table += "\n"
	table +=  "\t\t\t-----\n"
	table +=  "\t\tTOTAL\t%d\n\n"%(progeny_size)
	return table

#=====================
#=====================
def generateTypeCounts(parental, geneorder, distances, progeny_size, basetype, interference_tuple):
	doublecount = calculate_double_crossovers(distances, progeny_size, interference_tuple)

	firstcount = 2*(int(round(distances[0]*progeny_size/100.)) - 3*(dcount1 + dcount3))
	secondcount = 2*(int(round(distances[1]*progeny_size/100.)) - 3*(dcount2 + dcount3))
	parentcount = progeny_size - doublecount - firstcount - secondcount

	# dcount3 controls the third distance
	# for progeny_size of 1000, each dcount3 = 0.6 distance
	distance3 = distances[-1]

	if not distance3.is_integer():
		return None
	if firstcount <= 0 or secondcount <= 0:
		print("two many double cross-overs")
		return None
	if firstcount >= parentcount:
		print("Tetratype larger than Parental Type")
		return None
	if secondcount >= parentcount:
		print("Tetratype larger than Parental Type")
		return None

	# Create Six Genotypes
	tetradCount = {}

	tetradSet = [parental, parental, ptcl.invert_genotype(parental, basetype), ptcl.invert_genotype(parental, basetype),]
	tetradSet.sort()
	if debug is True: print(" parental ", tetradSet)

	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = parentcount

	#first flip
	firsttype = ptcl.flip_gene_by_letter(parental, geneorder[0], basetype)

	#usually TT
	tetradSet = [firsttype, ptcl.invert_genotype(firsttype, basetype), parental, ptcl.invert_genotype(parental, basetype),]
	tetradSet.sort()
	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = firstcount

	#usually NPD
	tetradSet = [firsttype, ptcl.invert_genotype(firsttype, basetype), firsttype, ptcl.invert_genotype(firsttype, basetype), ]
	tetradSet.sort()
	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = dcount1

	#second flip
	secondtype = ptcl.flip_gene_by_letter(parental, geneorder[2], basetype)

	#usually TT
	tetradSet = [secondtype, ptcl.invert_genotype(secondtype, basetype), parental, ptcl.invert_genotype(parental, basetype),]
	tetradSet.sort()
	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = secondcount

	#usually NPD
	tetradSet = [secondtype, ptcl.invert_genotype(secondtype, basetype), secondtype, ptcl.invert_genotype(secondtype, basetype),]
	tetradSet.sort()
	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = dcount2

	#both flips
	thirdtype = ptcl.flip_gene_by_letter(ptcl.flip_gene_by_letter(parental, geneorder[2], basetype), geneorder[0], basetype)

	#usually NPD
	tetradSet = [thirdtype, ptcl.invert_genotype(thirdtype, basetype), thirdtype, ptcl.invert_genotype(thirdtype, basetype),]
	tetradSet.sort()
	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = dcount3

	return tetradCount

#=====================
#=====================
def getVariables(basetype):
	variable_list = []
	if basetype[0] < basetype[1]:
		variable = '{0}{1}'.format(basetype[0].upper(),basetype[1].upper())
	else:
		variable = '{0}{1}'.format(basetype[1].upper(),basetype[0].upper())
	variable_list.append(variable)
	if basetype[1] < basetype[2]:
		variable = '{0}{1}'.format(basetype[1].upper(),basetype[2].upper())
	else:
		variable = '{0}{1}'.format(basetype[2].upper(),basetype[1].upper())
	variable_list.append(variable)
	if basetype[0] < basetype[2]:
		variable = '{0}{1}'.format(basetype[0].upper(),basetype[2].upper())
	else:
		variable = '{0}{1}'.format(basetype[2].upper(),basetype[0].upper())
	variable_list.append(variable)
	variable = 'geneorder'
	variable_list.append(variable)
	return variable_list

#=====================
#=====================
def blackboardFormat(question_string, html_table, variable_list, geneorder, distances):
	#FIB_PLUS TAB question text TAB variable1 TAB answer1 TAB answer2 TAB TAB variable2 TAB answer3
	blackboard = 'FIB_PLUS\t'
	blackboard += html_table
	blackboard += question_string
	variable_to_distance = {}
	for i in range(len(variable_list)-1):
		variable_to_distance[variable_list[i]] = distances[i]
	variable_list.sort()
	for i in range(len(variable_list)-1):
		variable = variable_list[i]
		blackboard += '\t{0}\t{1}\t'.format(variable, variable_to_distance[variable])
	blackboard += '\tgeneorder\t{0}\t{1}\n'.format(geneorder, geneorder[::-1])
	return blackboard

#=====================
#=====================
def formatBB_FIB_PLUS_Question(N, question, variable_list, geneorder, distances):
	crc16 = bptools.getCrc16_FromString(question)

	#FIB_PLUS TAB question text TAB variable1 TAB answer1 TAB answer2 TAB TAB variable2 TAB answer3
	bb_question = 'FIB_PLUS\t<p>{0}. {1}</p> {2}'.format(N, crc16, question)
	pretty_question = bptools.makeQuestionPretty(question)
	print('{0}. {1} -- {2}'.format(N, crc16, pretty_question))

	variable_to_distance = {}
	for i in range(len(variable_list)-1):
		variable_to_distance[variable_list[i]] = distances[i]
	variable_list.sort()
	for i in range(len(variable_list)-1):
		variable = variable_list[i]
		bb_question += '\t{0}\t{1}\t'.format(variable, variable_to_distance[variable])
	bb_question += '\tgeneorder\t{0}\t{1}'.format(geneorder, geneorder[::-1])
	bb_question += '\n'
	return bb_question

#=====================
#=====================
def makeQuestion(basetype, geneorder, distances, progeny_size, interference_tuple):
	if debug is True: print("------------")
	answerString = ("%s - %d - %s - %d - %s"
		%(geneorder[0], distances[0], geneorder[1], distances[1], geneorder[2]))
	print(answerString)
	if debug is True: print("------------")

	if debug is True: print("determine double crossovers")
	doublecross = distances[0]*distances[1]/100.
	if debug is True: print("doublecross", doublecross*10, 'per 1000')

	if debug is True: print("determine parental type")
	types = ['+++', '++'+basetype[2], '+'+basetype[1]+'+', '+'+basetype[1]+basetype[2]]
	parental = random.choice(types)

	tetradCount = generateTypeCounts(parental, geneorder, distances, progeny_size, basetype, interference_tuple)
	return tetradCount

#=====================
#=====================
def translate_genotype_counts_to_tetrads(GMC):
	print(GMC.progeny_groups_count_dict)
	print(GMC.genotype_counts)
	GMC.gene_letters_str

	# Create Six Genotypes
	tetradCount = {}

	tetradSet = list(GMC.parental_genotypes_tuple) + list(GMC.parental_genotypes_tuple)
	tetradSet.sort()
	if debug is True: print(" parental ", tetradSet)

	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = GMC.progeny_groups_count_dict['parental']

	print(tetradCount)

	#first flip
	firsttype1 = gml.flip_gene_by_letter(GMC.parental_genotypes_tuple[0], GMC.gene_order_str[0], GMC.gene_letters_str)
	firsttype2 = gml.invert_genotype(firsttype1, GMC.gene_letters_str)

	#usually TT
	tetradSet = list(GMC.parental_genotypes_tuple) + [firsttype1, firsttype2]
	tetradSet.sort()
	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = firstcount

	#usually NPD for gene 1
	tetradSet = [firsttype1, firsttype2, firsttype1, firsttype2]
	tetradSet.sort()
	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = dcount1

	#second flip
	secondtype = ptcl.flip_gene_by_letter(parental, geneorder[2], basetype)

	#usually TT
	tetradSet = [secondtype, ptcl.invert_genotype(secondtype, basetype), parental, ptcl.invert_genotype(parental, basetype),]
	tetradSet.sort()
	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = secondcount

	#usually NPD
	tetradSet = [secondtype, ptcl.invert_genotype(secondtype, basetype), secondtype, ptcl.invert_genotype(secondtype, basetype),]
	tetradSet.sort()
	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = dcount2

	#both flips
	thirdtype = ptcl.flip_gene_by_letter(ptcl.flip_gene_by_letter(parental, geneorder[2], basetype), geneorder[0], basetype)

	#usually NPD
	tetradSet = [thirdtype, ptcl.invert_genotype(thirdtype, basetype), thirdtype, ptcl.invert_genotype(thirdtype, basetype),]
	tetradSet.sort()
	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = dcount3

	return tetradCount

#=====================
#=====================
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='number of duplicate runs to do', default=1)
	args = parser.parse_args()
	outfile = ('bbq-' + os.path.splitext(os.path.basename(__file__))[0]
		+ '-questions.txt')
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	N = 0
	print(N)
	for i in range(args.duplicates):
		N += 1
		GMC = gmc.GeneMappingClass(3, N)
		GMC.setup_question()
		print(GMC.get_progeny_ascii_table())
		header = GMC.get_question_header()
		html_table = GMC.get_progeny_html_table()
		phenotype_info_text = GMC.get_phenotype_info()

		translate_genotype_counts_to_tetrads(GMC)
		sys.exit(1)

		genotype_counts_dict = makeQuestion(gene_letters, gene_order, distances, progeny_size, interference_tuple)
		if genotype_counts_dict is None:
			continue
		print(f'genotype_counts_dict={genotype_counts_dict}')

		ascii_table = makeProgenyAsciiTable(genotype_counts_dict, progeny_size)
		print(ascii_table)
		html_table = makeProgenyHtmlTable(genotype_counts_dict, progeny_size)
		#print(html_table)
		question_string = questionText(gene_letters)
		variable_list = getVariables(gene_order)
		complete_question = html_table + question_string
		#final_question = blackboardFormat(question_string, html_table, variable_list, gene_order, distances)
		final_question = formatBB_FIB_PLUS_Question(N, complete_question, variable_list, gene_order, distances)
		#print(final_question)

		f.write(final_question)
	f.close()
