#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
# Provides functions to generate random numbers and selections
import random
import math
import sys

# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools

#NUM TAB question_text TAB answer TAB [optional]tolerance

color_series_list = [
	('red', 'pink', 'white'),
	('blue', 'green', 'yellow'),
	('black', 'gray', 'white'),
	('red', 'orange', 'yellow'),
	('red', 'violet', 'blue'),
]

organism_list = [
	'flowers',
	'fish',
	'snakes',
	'birds',
	'butterflies',
	'beetles',
	'ducks',
	'frogs',
]

fictional_diseases = [
    'cooties',
    'homework-itis',
    'snackmania',
    'the giggle pox',
    'boardom syndrome',
    'midterm madness',
    'deadline delirium',
    'the freshman five',
    'finals fever',
    'powerpoint poisoning',
    'zoom fatigue',
]

#=========================
def get_values(p=None):
	if p is None:
		p = get_good_p()
	q = round(1-p, 2)
	#hw
	p2 = round(p**2, 4)
	q2 = round(q**2, 4)
	twopq = round(2*p*q,4)
	#print(p, q)
	#print(p2, twopq, q2, sum)
	return p, q, p2, twopq, q2

#=========================
def get_good_p():
	max_p = 0.99
	min_p = 0.4
	r = random.random()
	r *= (max_p-min_p)
	r += min_p
	#alleles
	p = round(r, 2)
	return p

#=========================
def get_good_F(p):
	if p <= 0.5:
		maxF = (1 - p)/p - 0.01
	else:
		maxF = 0.9
	r1 = 2*maxF*random.random() - maxF
	F = round(r1, 1)
	if F < 0.01 and maxF > 0.1:
		F = 0.1 * random.choice([-1, 1])
	return F

#=========================
def add_note():
	numbers = [2, 3, 4, 5, 6, 7, 8]
	random.shuffle(numbers)
	digits = ''.join(map(str, numbers[:3]))
	note_text = ''
	note_text += "<p>Note: "
	note_text += "Do not enter a percentage on the blank. "
	note_text += f"For example, if the answer is {digits[0:2]}.{digits[2]}%, "
	note_text += f"enter 0.{digits} on the blank. "
	note_text += "Your answer will be a decimal value between 0 and 1.</p>"
	return note_text

#=========================
def make_interesting_fraction(n, d=10000):
	#assume out of 10000
	# given numerator, n and denominator, d
	n = int(n)
	gcd = math.gcd(n, d)
	numerator = n // gcd
	denominator = d // gcd
	if denominator <= 100:
		factor = random.choice([7,11,13])
		numerator *= factor
		denominator *= factor
	elif denominator <= 400:
		factor = random.choice([3,7])
		numerator *= factor
		denominator *= factor
	if (numerator*1e4/denominator - n*1e4/d) > 0.1:
		print("something went wrong")
		sys.exit(1)
	return numerator, denominator

#=========================
def makeType1Table(organism, colors, counts):
	table = '<table style="border-collapse: collapse; border: 2px solid black;">'
	table += '<tr>'
	table += '  <th colspan="3" align="center">{0}</th>'.format(organism)
	table += '</tr><tr>'
	table += '  <th align="center">genotype</th>'
	table += '  <th align="center">phenotype</th>'
	table += '  <th align="center">count</th>'
	table += '</tr><tr>'
	table += '  <td align="center">homozygous<br/>dominant</td>'
	table += '  <td align="center">{0}</td>'.format(colors[0])
	table += '  <td align="right">{0:,d}</td>'.format(counts[0])
	table += '</tr><tr>'
	table += '  <td align="center">heterozygous</td>'
	table += '  <td align="center">{0}</td>'.format(colors[1])
	table += '  <td align="right">{0:,d}</td>'.format(counts[1])
	table += '</tr><tr>'
	table += '  <td align="center">homozygous<br/>recessive</td>'
	table += '  <td align="center">{0}</td>'.format(colors[2])
	table += '  <td align="right">{0:,d}</td>'.format(counts[2])
	table += '</tr><tr>'
	table += '  <th colspan="2" align="right">SUM</th>'
	table += '  <th align="right">{0:,d}</th>'.format(sum(counts))
	table += '</tr></table> '
	return table

#=========================
def makeType1Question(p, phenotype=None):
	# not in Hardy-Weinberg equilibrium
	# add a inbreeding factor, F
	# q > F / (F-1)
	# 1/ q < (F-1)/F < 1 - 1/F
	# 1/q + 1/F < 1
	# 1/F < 1 - 1/q < (q - 1)/q
	# F < q / (q - 1) = 1-p / (-p) q/p

	F = get_good_F(p)
	#if you change F from 0, then everything below breaks.
	#used to believe above statement, but it was a bug twopq instead of Ftwopq

	print(phenotype)
	p, q, p2, twopq, q2 = get_values(p)
	if phenotype != 'recessive': # or random.random() < 0.5:
		#get p
		phenotype = 'dominant'
		answer = p
	else:
		#get p
		print(phenotype)
		phenotype = 'recessive'
		answer = q
	Fp2 = round(p2 * (1 - F) + p*F, 8)
	Ftwopq = round(twopq * (1 - F), 8)
	Fq2 = round(q2 * (1 - F) + q * F, 8)

	Fsum = round(Fp2 + Ftwopq + Fq2, 8)
	if abs(Fsum - 1.0) > 0.01:
		print("sum error")
		return None
	#print("p={0:.2f} AND q={1:.2f} AND F={2:.2f}".format(p,q,F))
	#print(" p2={0:.4f},  2pq={1:.4f},  q2={2:.4f},  sum={3:.4f}".format(p2, twopq, q2, sum))
	#print("Fp2={0:.4f}, F2pq={1:.4f}, Fq2={2:.4f}, Fsum={3:.4f}".format(Fp2, Ftwopq, Fq2, Fsum))
	#print("")
	if Fq2 < 0:
		print("negative q2")
		return None

	gcd1 = math.gcd(int(Fp2*1e5), 100000)
	gcd2 = math.gcd(int(Ftwopq*1e5), int(Fq2*1e5))
	gcd = math.gcd(gcd1, gcd2)
	homo_recessive = int(Fq2*1e5) // gcd
	if homo_recessive == 1 and gcd % 2 == 0:
		gcd = gcd // 2

	homo_dominant = int(Fp2*1e5) // gcd
	heterozygote  = int(Ftwopq*1e5) // gcd
	homo_recessive = int(Fq2*1e5) // gcd

	print(homo_dominant, heterozygote, homo_recessive)
	organism = random.choice(organism_list)
	colors = random.choice(color_series_list)
	counts = [homo_dominant, heterozygote, homo_recessive]
	total = homo_dominant + heterozygote + homo_recessive

	table = makeType1Table(organism, colors, counts)

	question_text = ' '
	question_text += '<p>In a field there are {0:,d} {1} {2}, '.format(homo_dominant, colors[0], organism)
	question_text += '{0:,d} {1} {2}, '.format(heterozygote, colors[1], organism)
	question_text += 'and {0:,d} {1} {2} '.format(homo_recessive, colors[2], organism)
	question_text += 'that show incomplete dominance. '
	question_text += 'What is the frequency of the <b>{0}</b> allele?</p>'.format(phenotype)
	question_text += add_note()

	actual_q = (homo_recessive*2 + heterozygote)/(2.0*total)
	actual_p = 1.0 - actual_q
	#print("p={0:.2f}; actual_p={1:.5f}, diff={2:.8f}".format(p, actual_p, abs(p - actual_p)))
	#print("q={0:.2f}; actual_q={1:.5f}, diff={2:.8f}".format(q, actual_q, abs(q - actual_q)))
	if abs(q - actual_q) > 0.001 or abs(p - actual_p) > 0.001:
		print("ERROR VALUES ARE OFF")
		sys.exit(1)
		return None

	blackboard_text = 'NUM\t'
	blackboard_text += table + question_text + '\t'
	blackboard_text += '{0:.2f}\t'.format(answer)
	blackboard_text += '0.0099\n'
	return blackboard_text

#=========================
def makeType2aQuestion(p):
	p, q, p2, twopq, q2 = get_values(p)
	if random.random() < 0.5:
		#get p
		phenotype = 'dominant'
		answer = p
	else:
		#get p
		phenotype = 'recessive'
		answer = q
	numerator, denominator = make_interesting_fraction(q2*1e4, 10000)

	question_text = ''
	question_text += 'Genetic disorder occurs {0:,d} in {1:,d} births. '.format(numerator, denominator)
	question_text += 'What is the expected frequency of the <b>{0}</b> allele '.format(phenotype)
	question_text += 'according to the Hardy-Weinberg model? '
	question_text += add_note()

	blackboard_text = 'NUM\t'
	blackboard_text += question_text+'\t'
	blackboard_text += '{0:.2f}\t'.format(answer)
	blackboard_text += '0.0099\n'
	return blackboard_text

#=========================
def makeType2bQuestion(p):
	p, q, p2, twopq, q2 = get_values(p)
	if random.random() < 0.5:
		#get p
		phenotype = 'dominant'
		answer = p
	else:
		#get p
		phenotype = 'recessive'
		answer = q
	dominant_count = int((1.0 - q2)*1e4)
	numerator, denominator = make_interesting_fraction(dominant_count, 10000)

	question_text = ''
	question_text += 'In a small village, {0:,d} out of {1:,d} people '.format(numerator, denominator)
	question_text += 'have the dominant phenotype '
	question_text += 'and do NOT have a rare recessive disorder. '
	question_text += 'What is the expected frequency of the <b>{0}</b> allele '.format(phenotype)
	question_text += 'according to the Hardy-Weinberg model? '
	question_text += add_note()

	blackboard_text = 'NUM\t'
	blackboard_text += question_text+'\t'
	blackboard_text += '{0:.2f}\t'.format(answer)
	blackboard_text += '0.0099\n'
	return blackboard_text

#=========================
def makeType3aQuestion(p):
	p, q, p2, twopq, q2 = get_values(p)
	answer = p

	girls_count = int((p2 + twopq) * 1e4)
	girls_numerator, denominator = make_interesting_fraction(
		girls_count, 10000
	)
	boys_numerator = int(p * denominator)
	total_kids = denominator * 2

	disease = random.choice(fictional_diseases)

	question_text = (
		f'<p>It was recently discovered that <i>{disease}</i> '
		'is a dominant X-linked disease that displays complete '
		'dominance.</p> '
		'<p>At local high schools, '
		f'{total_kids:,d} students were tested for <i>{disease}</i>. '
		f'It was found that {boys_numerator:,d} of {denominator:,d} boys '
		f'and {girls_numerator:,d} of {denominator:,d} girls had '
		f'<i>{disease}</i>. '
	)

	if disease == 'cooties':
		question_text += (
			'Further supporting the theory that girls have more '
			f'<i>{disease}</i> than boys. '
			'<a href="https://www.pnas.org/content/105/46/17994.full">'
			'[1]</a> '
			'<a href="https://www.collegian.psu.edu/archives/'
			'article_14ddb2bf-895d-5208-bdba-53db8062f01c.html">'
			'[2]</a> '
		)

	question_text += (
		'</p> '
		'<p>Based on the data above, what is the allele frequency '
		f'(p) for the dominant <i>{disease}</i> allele? '
		'Assume the Hardy-Weinberg model applies.</p>'
	)

	question_text += add_note()

	#print(question_text)

	blackboard_text = 'NUM\t'
	blackboard_text += question_text+'\t'
	blackboard_text += '{0:.2f}\t'.format(answer)
	blackboard_text += '0.0099\n'

	#sys.exit(1)
	return blackboard_text


#=========================
def makeQuestion(variant, p):
	if variant == '1a':
		blackboard_text = makeType1Question(p, 'dominant')
	elif variant == '1b':
		blackboard_text = makeType1Question(p, 'recessive')
	elif variant == '2a':
		blackboard_text = makeType2aQuestion(p)
	elif variant == '2b':
		blackboard_text = makeType2bQuestion(p)
	elif variant == '3a':
		blackboard_text = makeType3aQuestion(p)
	return blackboard_text

#===========================================================
#===========================================================
# This function handles the parsing of command-line arguments.
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Returns:
		argparse.Namespace: Parsed arguments with attributes `duplicates`,
		`num_choices`, and `question_type`.
	"""
	parser = bptools.make_arg_parser(description="Generate questions.")
	parser = bptools.add_choice_args(parser, default=5)
	parser = bptools.add_question_format_args(
		parser,
		types_list=['num', 'mc'],
		required=False,
		default='num'
	)
	variant_group = parser.add_mutually_exclusive_group(required=False)

	VARIANT_LONG_HELP = {
		"1a": "From phenotype counts with incomplete dominance, compute dominant allele frequency (p).",
		"1b": "From phenotype counts with incomplete dominance, compute recessive allele frequency (q).",
		"2a": "Given recessive disorder prevalence (q^2), compute p or q as specified.",
		"2b": "Given dominant phenotype proportion (1-q^2), compute p or q as specified.",
		"3a": "Use X-linked dominant model with sex-specific rates to estimate allele frequency p.",
	}

	variant_group.add_argument(
		"-v", "--variant", dest="variant", type=str,
		choices=tuple(VARIANT_LONG_HELP.keys()),
		help="Select question template variant"
	)

	# Optional direct flags
	variant_group.add_argument("--1a", dest="variant", action="store_const", const="1a",
		help=VARIANT_LONG_HELP["1a"])
	variant_group.add_argument("--1b", dest="variant", action="store_const", const="1b",
		help=VARIANT_LONG_HELP["1b"])
	variant_group.add_argument("--2a", dest="variant", action="store_const", const="2a",
		help=VARIANT_LONG_HELP["2a"])
	variant_group.add_argument("--2b", dest="variant", action="store_const", const="2b",
		help=VARIANT_LONG_HELP["2b"])
	variant_group.add_argument("--3a", dest="variant", action="store_const", const="3a",
		help=VARIANT_LONG_HELP["3a"])

	parser.set_defaults(variant="1a")
	args = parser.parse_args()
	return args

#===========================================================
#===========================================================
# This function serves as the entry point for generating and saving questions.
def main():
	"""
	Main function that orchestrates question generation and file output.

	Workflow:
	1. Parse command-line arguments.
	2. Generate the output filename using script name and args.
	3. Generate formatted questions using write_question().
	4. Shuffle and trim the list if exceeding max_questions.
	5. Write all formatted questions to output file.
	6. Print stats and status.
	"""

	# Parse arguments from the command line
	args = parse_arguments()

	outfile = bptools.make_outfile(args.question_type.upper(),
		f"{args.num_choices}_choices"
	)
	bptools.collect_and_write_questions(write_question, args, outfile)

#===========================================================
def write_question(N, args):
	rawp = random.randint(20, 50) * 2
	p = rawp / 100.0
	blackboard_text = makeQuestion(args.variant, p)
	return blackboard_text

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
