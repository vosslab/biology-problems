#!/usr/bin/env python3

# Standard Library
import os
import sys
import math
import numpy
import random
import argparse

# Local repo modules
import bptools
import genemaplib as gml
import tetradmapclass as tetmapcls

debug = True

def tetradSetToString(tetradSet):
	mylist = sorted(tetradSet)
	mystr = ''
	for item in mylist:
		mystr += f'{item}\t'
	return mystr

#====================================
def getDistance():
	#integers
	return random.randint(2,45)

#====================================
def getProgenySize(distance):
	if debug is True: print("determine progeny size")
	gcdfinal = math.gcd(distance, 100)
	if debug is True: print("Final GCD", gcdfinal)
	progenybase = 100/gcdfinal
	minprogeny =  900/progenybase
	maxprogeny = 6000/progenybase
	progs = numpy.arange(minprogeny, maxprogeny+1, 1, dtype=numpy.float64)*progenybase
	#print(progs)
	numpy.random.shuffle(progs)
	#print(progs)
	bases = progs * distance * distance / 1e4
	#print(bases)
	devs = (bases - numpy.around(bases, 0))**2
	#print(devs)
	argmin = numpy.argmin(devs)
	progeny_size = int(progs[argmin])
	if debug is True: print(("total progeny: %d\n"%(progeny_size)))
	return progeny_size

#====================================
def lcm(a, b):
	return abs(a*b) // math.gcd(a, b)

#====================================
def lcm4(a, b, c, d):
	gcd1 = math.gcd(a, b)
	gcd2 = math.gcd(c, d)
	gcdfinal = math.gcd(gcd1, gcd2)
	return abs(a*b*c*d) // gcdfinal

#====================================
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

#====================================
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

#====================================
def makeQuestion(basetype, distance, progeny_size):
	if debug is True: print("------------")
	answerString = ("%s - %d - %s"
		%(basetype[0], distance, basetype[1]))
	print(answerString)
	if debug is True: print("------------")

	types = ['++', '+'+basetype[1], basetype[0]+'+', basetype[0]+basetype[1]]
	if debug is True: print("types=", types)

	if debug is True: print("determine parental type")
	parental = random.choice(types)
	if debug is True: print("parental=", parental, gml.invert_genotype(parental, basetype))

	tetradCount = generateTypeCounts(parental, basetype, progeny_size, distance)
	if debug is True: print("tetradCount=", tetradCount)

	return tetradCount

#====================================
def generateTypeCountsX2(parental_type, basetype, progeny_size, distance):
	type_counts = {}
	recombinant_type_1 = gml.flip_gene_by_letter(parental_type, geneorder[0], basetype)
	if debug is True: print("recombinant type 1=", recombinant_type_1)
	recombinant_type_2 = gml.invert_genotype(recombinant_type_1, basetype)
	if debug is True: print("recombinant type 2=", recombinant_type_2)

	if debug is True: print("determine recombinant type counts")
	total_recombinant_count = int(round(distance*progeny_size/100.))
	recombinant_count_1 = 0
	recombinant_count_2 = 0
	for i in range(total_recombinant_count):
		if random.random() < 0.5:
			recombinant_count_1 += 1
		else:
			recombinant_count_2 += 1
	if recombinant_count_1 == recombinant_count_2:
		shift = random.randint(1,4)
		recombinant_count_1 += shift
		recombinant_count_2 -= shift
	
	type_counts[recombinant_type_1] = recombinant_count_1
	if debug is True: print("recombinant count_1=", recombinant_count_1)
	type_counts[recombinant_type_2] = recombinant_count_2
	if debug is True: print("recombinant count_2=", recombinant_count_2)

	if debug is True: print("determine parental type count")
	total_parent_count = progeny_size - total_recombinant_count
	if debug is True: print("  ", parental_type, gml.invert_genotype(parental_type, basetype), total_parent_count)
	parent_count_1 = 0
	parent_count_2 = 0
	for i in range(total_parent_count):
		if random.random() < 0.5:
			parent_count_1 += 1
		else:
			parent_count_2 += 1
	if parent_count_1 == parent_count_2:
		shift = random.randint(1,4)
		parent_count_1 += shift
		parent_count_2 -= shift
	
	type_counts[parental_type] = parent_count_1
	if debug is True: print("parental count_1=", parent_count_1)
	type_counts[gml.invert_genotype(parental_type, basetype)] = parent_count_2
	if debug is True: print("parental count_2=", parent_count_2)


	return type_counts

#====================================
def generateTypeCounts(parental, basetype, progeny_size, distance):
	
	#distance = (3*NPD + TT/2) / progeny_size * 100%
	#NPD = double cross // 4
	#double cross = 2 * progeny_size * distance/100
	nonparent_ditype_count = progeny_size * distance**2 // 40000 + 1
	tetra_type_count = 2 * (distance*progeny_size//100 - 3 * nonparent_ditype_count)
	parent_ditype_count = progeny_size - tetra_type_count - nonparent_ditype_count

	if parent_ditype_count <= 0 or tetra_type_count <= 0:
		return None
	if tetra_type_count > parent_ditype_count:
		return None

	print("[3*{0} + {1}/2 ]//{2} = {3}".format(
		nonparent_ditype_count, tetra_type_count, progeny_size, distance))

	# Create Four Genotypes
	tetradCount = {}
	parental_type_1 = parental
	parental_type_2 = gml.invert_genotype(parental, basetype)
	recombinant_type_1 = gml.flip_gene_by_letter(parental, basetype[0], basetype)
	recombinant_type_2 = gml.flip_gene_by_letter(parental, basetype[1], basetype)

	#parental ditype (PD)
	tetradSet = [parental_type_1, parental_type_1, parental_type_2, parental_type_2,]
	tetradSet.sort()
	if debug is True: print(" parental ", tetradSet)
	if debug is True: print(" parent_ditype_count ", parent_ditype_count)


	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = parent_ditype_count

	#tetra-type (TT)
	tetradSet = [parental_type_1, parental_type_2, recombinant_type_1, recombinant_type_2, ]
	tetradSet.sort()
	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = tetra_type_count
	if debug is True: print(" tetra-type (TT) ", tetradSet)
	if debug is True: print(" tetra_type_count ", tetra_type_count)

	#non-parental ditype (NPD)
	tetradSet = [recombinant_type_1, recombinant_type_1, recombinant_type_2, recombinant_type_2,]
	tetradSet.sort()
	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = nonparent_ditype_count
	if debug is True: print(" non-parental ditype (NPD) ", tetradSet)
	if debug is True: print(" nonparent_ditype_count ", nonparent_ditype_count)

	return tetradCount


#===========================
#===========================
def get_question_text(question_type: str) -> str:
	"""
	Generates the question text based on the question type.

	Args:
		question_type (str): Type of question ('num' or 'mc').

	Returns:
		str: The formatted question text for either a standard two-gene problem or a complex tetrad problem.
	"""
	# Background information for both types of questions
	question_string = '<h6>Unordered Tetrad Two Gene Distance</h6>'
	question_string += '<p>The yeast <i>Saccharomyces cerevisiae</i> has unordered tetrads. '
	question_string += 'A cross is made to study the linkage relationships among two genes. '
	question_string += '<p>Using the table above, determine the distance between the two genes.</p> '
	question_string += '<p>Dr. Voss guide to unordered tetrads:</p><ul>'
	question_string += '<li>Step 1: Find the Row for the Parental Ditype (PD).</li>'
	question_string += '<li>Step 2: Assign PD, NPD, TT for each row</li>'
	question_string += '<li>Step 3: Determine if the two genes are linked.</li>'
	question_string += '<ul><li>PD >> NPD &rarr; linked; PD &approx; NPD &rarr; unlinked</li></ul>'
	question_string += '<li>Step 4: If unlinked, determine the map distance between the two genes</li>'
	question_string += '<ul><li>D = &half; (TT + 6 NPD)/total = (3 NPD + &half;TT)/total</li></ul>'
	question_string += '</ul>'

	# Additional instructions based on question type
	if question_type == 'num':
		# Numeric question instructions
		question_string += '<p><strong>Calculate the genetic distance between the two genes,</strong> '
		question_string += 'expressing your answer in centimorgans (cM).</p> '
		question_string += '<ul> '
		question_string += '<li><i>Important Tip 1:</i> '
		question_string +=   'Your calculated distance between the genes should be a whole number. '
		question_string +=   'Finding a decimal in your answer, such as 5.5, indicates a mistake was made. '
		question_string +=   'Please provide your answer as a complete number without fractions or decimals.</li>'
		question_string += '<li><i>Important Tip 2:</i> '
		question_string +=   'Your answer should be written as a numerical value only, '
		question_string +=   'no spaces, commas, or units such as "cM" or "map units". '
		question_string +=   'For example, if the distance is fifty one centimorgans, simply write "51". </li> '
		question_string += '</ul> '

	elif question_type == 'mc':
		# Multiple-choice question instructions
		question_string += '<p><strong>Select the correct genetic distance from the choices below.</strong></p>'

	return question_string

#=====================
#=====================
def translate_genotype_counts_to_tetrads(TetradMapCls):
	print(TetradMapCls.progeny_groups_count_dict)
	print(TetradMapCls.genotype_counts)

	#shorter variable names
	gene_letters = TetradMapCls.gene_letters_str
	gene_order = TetradMapCls.gene_order_str
	parent_tuple = TetradMapCls.parental_genotypes_tuple

	# Create Six Genotypes
	tetradCount = {}

	#(A) No crossing over (NCO), parental ditype (PD)
	tetradSet = list(parent_tuple) + list(parent_tuple)
	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = TetradMapCls.progeny_groups_count_dict['parental']
	print(tetradCount)

	#def crossover_after_index(genotype: str, gene_index: str, gene_order: str) -> str:

	#(B) Single crossing over on the one of the chrosomes, tetratype (TT)
	recomb1 = gml.crossover_after_index(parent_tuple[0], 1, gene_order)
	recomb2 = gml.invert_genotype(recomb1, gene_letters)
	tetradSet = list(parent_tuple) + [recomb1, recomb2]
	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = 0
	print(tetradCount)

	#(C) 2-strand double crossing over, parental ditype (PD)
	tetradSet = list(parent_tuple) + list(parent_tuple)
	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = 0
	print(tetradCount)

	#(D) 3-strand double crossing over, tetratype (TT)

	#(E) 3-strand double crossing over, tetratype (TT)

	#(F) 4-strand double crossing over, non-parental ditype (NPD)

	return tetradCount

#===========================
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Returns:
		Namespace: Parsed arguments with attributes `question_type` and `duplicates`.
	"""
	parser = argparse.ArgumentParser(description='Generate genetic mapping questions.')

	question_group = parser.add_mutually_exclusive_group(required=True)
	question_group.add_argument(
		'-t', '--type', dest='question_type', type=str, choices=('num', 'mc'),
		help="Set the question type: 'num' for numeric or 'mc' for multiple choice"
	)
	question_group.add_argument(
		'-m', '--mc', dest='question_type', action='store_const', const='mc',
		help="Set question type to multiple choice"
	)
	question_group.add_argument(
		'-n', '--num', dest='question_type', action='store_const', const='num',
		help="Set question type to numeric"
	)

	parser.add_argument(
		'-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='Number of duplicate runs to generate', default=1
	)

	return parser.parse_args()

#===========================
def generate_question(N: int, question_type: str) -> str:
	"""
	Generates a formatted question string based on the type.

	Args:
		N (int): Question number.
		question_type (str): Type of question ('num' or 'mc').

	Returns:
		str: The formatted question string ready to be written to the file.
	"""
	# Initialize Gene Mapping Class instance
	TetradMapCls = tetmapcls.TetradMappingClass(2, N)
	TetradMapCls.debug = debug
	TetradMapCls.question_type = question_type
	TetradMapCls.setup_question()
	print(TetradMapCls.get_progeny_ascii_table())

	# Retrieve question data
	header = TetradMapCls.get_question_header()
	phenotype_info_text = TetradMapCls.get_phenotype_info()
	html_table = TetradMapCls.get_progeny_html_table()
	question_string = get_question_text(question_type)

	# Assemble full question content

	translate_genotype_counts_to_tetrads(TetradMapCls)

	full_question = header + phenotype_info_text + html_table + question_string
	# Format question based on type
	if question_type == 'num':
		distance = TetradMapCls.distances_dict[(1, 2)]
		return bptools.formatBB_NUM_Question(N, full_question, distance, 0.1, tol_message=False)
	elif question_type == 'mc':
		choices_list, answer_text = TetradMapCls.make_choices()
		return bptools.formatBB_MC_Question(N, full_question, choices_list, answer_text)
	print("Error: Invalid question type in generate_question.")
	sys.exit(1)

#===========================
def main():
	"""
	Main function that handles generating questions and writing them to an output file.
	"""
	args = parse_arguments()

	# Generate output filename based on script name and question type
	script_name = os.path.splitext(os.path.basename(__file__))[0]
	outfile = f'bbq-{script_name}-{args.question_type.upper()}-questions.txt'
	print(f'Writing to file: {outfile}')

	# Open file and write questions
	with open(outfile, 'w') as f:
		for i in range(args.duplicates):
			N = i + 1  # Question number
			final_question = generate_question(N, args.question_type)
			f.write(final_question)

if __name__ == "__main__":
	main()
