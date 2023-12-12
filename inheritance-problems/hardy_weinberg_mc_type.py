#!/usr/bin/env python3

# built-in modules
import os
import sys
import math
import random
import string
import argparse

# pip modules
import yaml

# local modules
import bptools
import disorderlib


yaml_file = "organism_data.yml"
with open(yaml_file, 'r') as file:
	organism_data = yaml.safe_load(file)
#import pprint
#pprint.pprint(organism_data)

choices_dict = {
	"p":	"<strong>p</strong> &mdash; Frequency of the dominant allele",
	"q":	"<strong>q</strong> &mdash; Frequency of the recessive allele",
	"p2":	"<strong>p&sup2;</strong> &mdash; Frequency of homozygous dominant individuals",
	"2pq":	"<strong>2pq</strong> &mdash; Frequency of heterozygous individuals",
	"q2":	"<strong>q&sup2;</strong> &mdash; Frequency of homozygous recessive individuals",
	"p2 + 2pq":	"<strong>p&sup2; + 2pq</strong> &mdash; Frequency of individuals with the dominant phenotype",
	"2pq + q2":	"<strong>2pq + q&sup2;</strong> &mdash; Frequency of individuals that are NOT homozygous dominant"
}

x_linked_organism_list = ['humans', 'fruit flies']

color_series_list = [
	('red', 'pink', 'white'),
	('blue', 'green', 'yellow'),
	('black', 'gray', 'white'),
	('red', 'orange', 'yellow'),
	('red', 'violet', 'blue'),
]
colorful_organism_dict = {
	'butterflies': 'wings',
	'flowers': 'petals',
	'fish': 'scales',
	'birds': 'feathers',
}

general_organism_dict = {
	'butterflies': 'wing pattern',
	'beetles': 'color pattern',
	'flowers': 'petal color',
	'rabbits': 'coat color',
	'deer': 'antler shape',
	'snakes': 'scale pattern',
	'lizards': 'scale pattern',
	'fish': 'fin shape',
	'birds': 'beak length',
}

#=========================
def make_html_fraction_line(numerator, denominator):
	html_txt = '<span style="display: inline-block; vertical-align: middle; text-align: center;">'
	html_txt += f'  <span style="display: block; font-size: 14px; vertical-align: top;">{numerator}</span>'
	html_txt += '  <hr style="margin: 2px 0; border: none; height: 1px; color: black; background-color: black;" />'
	html_txt += f'  <span style="display: block; font-size: 14px; vertical-align: bottom;">{denominator}</span>'
	html_txt += '</span>'
	return html_txt

def make_html_fraction_table(numerator, denominator):
	font_size = "90%"
	html_txt = '&nbsp;<table style="display: inline-table; border-collapse: collapse; line-height: 1; vertical-align: middle;">'
	html_txt += '  <tr>'
	if isinstance(numerator, int):
		html_txt += f'    <td style="border: none; font-size: {font_size}; padding: 2px; text-align: center;">&nbsp;{numerator:,d}&nbsp;</td>'
	else:
		html_txt += f'    <td style="border: none; font-size: {font_size}; padding: 2px; text-align: center;">&nbsp;{numerator}&nbsp;</td>'
	html_txt += '  </tr>'
	html_txt += '  <tr>'
	html_txt += '    <td style="border: none; padding: 0; height: 2px; background-color: black;"></td>'
	html_txt += '  </tr>'
	html_txt += '  <tr>'
	if isinstance(denominator, int):
		html_txt += f'    <td style="border: none; font-size: {font_size}; padding: 2px; text-align: center;">&nbsp;{denominator:,d}&nbsp;</td>'
	else:
		html_txt += f'    <td style="border: none; font-size: {font_size}; padding: 2px; text-align: center;">&nbsp;{denominator}&nbsp;</td>'
	html_txt += '  </tr>'
	html_txt += '</table>&nbsp;'
	return html_txt

def make_html_fraction_slash(numerator, denominator):
	html_txt = ""
	html_txt += '<span style="display: inline-block; vertical-align: middle; line-height: normal;">'
	html_txt += f'  <span style="font-size: 14px; vertical-align: top;">{numerator:,d}</span>'
	html_txt += '  <span style="font-size: 12px; vertical-align: middle; margin: 4 0px;">&#x2215;</span>'
	html_txt += f'  <span style="font-size: 14px; vertical-align: bottom;">&nbsp;{denominator:,d}&nbsp;</span>'
	html_txt += '</span>'
	return html_txt

def make_html_fraction(numerator, denominator):
	return make_html_fraction_table(numerator, denominator)


#=========================
def make_interesting_fraction(p, d=10000):
	#assume out of 10000
	# given numerator, n and denominator, d
	n = int(round(p*10000))
	gcd = math.gcd(n , d)
	numerator = n // gcd
	denominator = d // gcd
	if denominator <= 100:
		factor = random.choice([7, 11, 13, 17])
		numerator *= factor
		denominator *= factor
	elif denominator <= 400:
		factor = random.choice([3, 7])
		numerator *= factor
		denominator *= factor
	frac = numerator/denominator
	if abs(frac - p) > 0.01:
		print(f'numerator = {numerator} and denominator = {denominator};')
		print(f'frac = {frac:.4f}; n = {p:.4f}')
		print("something went wrong")
		sys.exit(1)
	return numerator, denominator

#=========================
def get_values(p=None):
	if p is None:
		p = get_good_p()
	q = round(1-p, 2)
	#hw
	p2 = round(p**2, 4)
	q2 = round(q**2, 4)
	twopq = round(2*p*q, 4)
	total_sum = p2 + twopq + q2
	if abs(total_sum - 1) > 1e-6:
		raise ValueError
	return p, q, p2, twopq, q2

#=========================
def get_good_p():
	max_p = 0.99
	min_p = 0.40
	r = random.random()
	r *= (max_p-min_p)
	r += min_p
	#alleles
	p = round(r, 2)
	return p

#====================================
def generate_p_q_allele_calc_question(given_var, p):
	""" sample question
	A species of butterflies exhibits incomplete dominance in its wing color. Those with two copies of the R allele have red wings, and heterozygotes have orange wings and recessive individuals have yellow wings. In a field, a researcher counted 3,125 butterflies. There were 3,038 red butterflies, 49 orange butterflies, and 38 yellow butterflies. The researcher calculates a fraction of (49 + 38*2)/6250 = 0.02.
	Which Hardy-Weinberg variable below is represented by the value 0.02?
	"""
	#organism_data
	organism_name, organism_dict = random.choice(list(organism_data['organisms'].items()))
	character_dict = random.choice(organism_dict['characters'])
	character_name = character_dict['name']
	habitat_name = random.choice(organism_dict['habitats'])
	if character_dict['colorful'] is True:
		traits_list = random.choice(color_series_list)
	else:
		traits_list = random.choice(character_dict['trait_sets'])

	p, q, p2, twopq, q2 = get_values(p)
	p2_num, denominator = make_interesting_fraction(p2)
	q2_num = int(round(q2*denominator))
	twopq_num = int(round(twopq*denominator))
	total_alleles = denominator * 2

	question = f"<p>In the {habitat_name} population of {denominator} {organism_name}, " \
		f"there were {p2_num} with {traits_list[0]} {character_name}, " \
		f"{twopq_num} with {traits_list[1]} {character_name}, and {q2_num} with {traits_list[2]} {character_name}.</p> "

	if given_var == 'q':
		numerator = f"1 &times; {twopq_num:,d} &nbsp;+&nbsp; 2 &times; {q2_num:,d}"
		question +=( "<p>The researcher calculates a fraction of "
			+ make_html_fraction(numerator, total_alleles)
			+ f" = {q:.2f}.</p>"
			f"<p>Which Hardy-Weinberg variable below is represented by the value {q:.2f}?</p>")
	else: # given_var == 'p'
		numerator = f"2 &times; {p2_num:,d} &nbsp;+&nbsp; 1 &times; {twopq_num:,d}"
		question += ( "<p>The researcher calculates a fraction of "
			+ make_html_fraction(numerator, total_alleles)
			+ f" = {p:.2f}.</p>"
			+ f"<p>Which Hardy-Weinberg variable below is represented by the value {p:.2f}?</p>"
			)
	return question

#====================================
def generate_p_q_allele_x_linked_question(given_var, p):
	""" sample question
	In a study of an X-linked recessive disorder in a certain species of fruit flies, male phenotypes are directly indicative of the allele frequencies due to their single X chromosome. In a laboratory population of 1,000 male fruit flies, 800 do not show the disorder (implying they have the dominant allele).
	Which Hardy-Weinberg variable is represented by the fraction 800/1000 of male fruit flies without the disorder?
	"""
	organism_name = 'humans'
	mdc = disorderlib.MultiDisorderClass()
	disorder_dict = mdc.randomDisorderDict('X-linked recessive')
	disorder_paragraph = '<p>' + mdc.getDisorderParagraph(disorder_dict) + '</p><br/>'
	disorder_name = mdc.getDisorderShortName(disorder_dict)

	p, q, p2, twopq, q2 = get_values(p)
	print(f'p = {p}')
	p_num, denominator = make_interesting_fraction(p)
	q_num = denominator - p_num
	print(f'p_num = {p_num} and q_num = {q_num}; out of {denominator}')

	if given_var == 'q':
		question = f"<p>In a study of {disorder_name}, an X-linked recessive disorder, " \
			f"in a population of {denominator} male {organism_name}, {q_num} were found to have the disorder.</p> " \
			f"<p>Which Hardy-Weinberg variable is represented by the fraction " \
			f"{make_html_fraction(q_num,denominator)}?</p> "
	else: # given_var == 'p'
		question = f"<p>In a study of {disorder_name}, an X-linked recessive disorder, " \
			f"in a population of {denominator} male {organism_name}, {p_num} did NOT have the disorder.</p> " \
			f"<p>Which Hardy-Weinberg variable is represented by the fraction " \
			f"{make_html_fraction(p_num,denominator)}?</p> "
	return disorder_paragraph + question

#====================================
def generate_2pq_q2_calc_question(p):
	""" sample question
	In a garden, a certain flower shows incomplete dominance in flower color: red (R), pink (RW), and white (W). In practice, pink and white color flowers can be hard to distinguish, so they are counted together. Observations of 200 flowers reveal that 160 were either white or pink and not red.
	Which Hardy-Weinberg variable is represented by the fraction 160/200 of flowers that are not red?
	"""
	organism_name, organism_dict = random.choice(list(organism_data['organisms'].items()))
	character_dict = random.choice(organism_dict['characters'])
	character_name = character_dict['name']
	habitat_name = random.choice(organism_dict['habitats'])
	if character_dict['colorful'] is True:
		traits_list = random.choice(color_series_list)
	else:
		traits_list = random.choice(character_dict['trait_sets'])
	#typical_behavior = organism_dict['typical_behavior'] # Define typical behavior

	# Choose a random uppercase letter to represent the allele
	dom_allele = random.choice(string.ascii_uppercase)
	rec_allele = dom_allele.lower()

	p, q, p2, twopq, q2 = get_values(p)
	p2_num, denominator = make_interesting_fraction(p2)
	twopq_q2_num = denominator - p2_num

	question = f"<p>In the {habitat_name} population of {organism_name}, " \
		f"there is a display of incomplete dominance in {character_name}. " \
		f"Individuals with two {dom_allele} alleles exhibit {traits_list[0]}, " \
		f"those with one {dom_allele} allele and one {rec_allele} allele exhibit {traits_list[1]}, " \
		f"and those with two {rec_allele} alleles exhibit {traits_list[2]}.</p> "

	question += f"<p>A group of {denominator} {organism_name} were observed. " \
		f"{twopq_q2_num:,d} had either <strong>{traits_list[1]} or {traits_list[2]}</strong> {character_name}, " \
		f"and did NOT have {traits_list[0]} {character_name}.</p> "
	question += ( "<p>Which Hardy-Weinberg variable is represented by the fraction"
		+ f"{make_html_fraction(twopq_q2_num, denominator)}? </p>")

	#ChatGPT please finish
	return question

#====================================
def generate_complete_dom_question(given_var, p):
	organism_name, organism_dict = random.choice(list(organism_data['organisms'].items()))
	character_dict = random.choice(organism_dict['characters'])
	character_name = character_dict['name']
	habitat_name = random.choice(organism_dict['habitats'])
	if character_dict['colorful'] is True:
		traits_list = random.choice(color_series_list)
	else:
		traits_list = random.choice(character_dict['trait_sets'])
	#typical_behavior = organism_dict['typical_behavior'] # Define typical behavior

	p, q, p2, twopq, q2 = get_values(p)

	# Choose a random uppercase letter to represent the allele
	dom_allele = random.choice(string.ascii_uppercase)

	# Assuming a scenario of dominant/recessive trait
	p2_num, denominator = make_interesting_fraction(p2)
	twopq_num = int(round(twopq*denominator))
	dominant_num = p2_num + twopq_num
	q2_num = denominator - p2_num - twopq_num

	# Opening sentence for complete dominance
	question = f"<p>In the {habitat_name} population of {organism_name}, " \
		f"there is a display of complete dominance in {character_name}. " \
		f"Individuals with at least one {dom_allele} allele show the {traits_list[0]} {character_name}, " \
		f"while those no {dom_allele} alleles show the {traits_list[2]} {character_name}.</p> "
	#f"{typical_behavior}</p> "


	# given_var in q2 or p2 + 2pq

	question += f"<p>A group of {denominator} {organism_name} were observed. " \
		f"{dominant_num} exhibited the {traits_list[0]} {character_name}, " \
		f"while {q2_num} showed the recessive form of {traits_list[2]} {character_name}.</p> "

	if given_var == 'q2':
		question += ( "<p>Which Hardy-Weinberg variable is represented by the fraction"
			+ f"{make_html_fraction(q2_num, denominator)}? </p>")
	elif given_var == 'p2 + 2pq':
		question += ( "<p>Which Hardy-Weinberg variable is represented by the fraction"
			+ f"{make_html_fraction(dominant_num, denominator)}? </p>")
	return question

#====================================
def generate_incomplete_dom_question(given_var, p):
	""" sample question
	In a botanical garden, a certain species of flower exhibits incomplete dominance in its petal colors: red (homozygous dominant), pink (heterozygous), and white (homozygous recessive). Genetic studies have shown that out of 300 flowers, 60 are red, 180 are pink, and 60 are white.
	Which of the following values is represented by the fraction of pink flowers in the population (180/300)?
	"""
	organism_name, organism_dict = random.choice(list(organism_data['organisms'].items()))
	character_dict = random.choice(organism_dict['characters'])
	character_name = character_dict['name']
	habitat_name = random.choice(organism_dict['habitats'])
	if character_dict['colorful'] is True:
		traits_list = random.choice(color_series_list)
	else:
		traits_list = random.choice(character_dict['trait_sets'])
	#typical_behavior = organism_dict['typical_behavior']  # Define typical behavior

	# Choose a random uppercase letter to represent the allele
	dom_allele = random.choice(string.ascii_uppercase)
	rec_allele = dom_allele.lower()

	p, q, p2, twopq, q2 = get_values(p)

	# Assuming a scenario of dominant/recessive trait
	p2_num, denominator = make_interesting_fraction(p2)
	twopq_num = int(round(twopq*denominator))
	q2_num = denominator - p2_num - twopq_num

	# given_var in p2 or 2pq

	question = f"<p>In the {habitat_name} population of {organism_name}, " \
		f"there is a display of incomplete dominance in {character_name}. " \
		f"Individuals with two {dom_allele} alleles exhibit {traits_list[0]}, " \
		f"those with one {dom_allele} allele and one {rec_allele} allele exhibit {traits_list[1]}, " \
		f"and those with two {rec_allele} alleles exhibit {traits_list[2]}.</p> "

	#f"{typical_behavior}</p> "

	question += f"<p>A group of {denominator} {organism_name} were observed. " \
		f"{p2_num} exhibited the {traits_list[0]} {character_name}, " \
		f"{twopq_num} had the {traits_list[1]} {character_name}, " \
		f"and {q2_num} showed the recessive form of {traits_list[2]} {character_name}.</p> "

	if given_var == 'p2':
		question += ( "<p>Which Hardy-Weinberg variable is represented by the fraction"
			+ f"{make_html_fraction(p2_num, denominator)}? </p>")
		question += f"<p>Which Hardy-Weinberg variable is represented by the fraction {p2_num}/{denominator}?</p>"
	elif given_var == '2pq':
		question += ( "<p>Which Hardy-Weinberg variable is represented by the fraction"
			+ f"{make_html_fraction(twopq_num, denominator)}? </p>")
	return question

#====================================
def generate_hw_problem():
	variables = list(choices_dict.keys())
	given_var = random.choice(variables)
	#given_var = random.choice(('p', 'q'))
	answer_string = choices_dict[given_var]
	p = get_good_p() # value btw 0.40 and 0.99 two decimal places
	#p, q, p2, twopq, q2 = get_values(p)

	if given_var in ('p', 'q'):
		if random.random() < 0.5:
			question_string = generate_p_q_allele_x_linked_question(given_var, p)
		else:
			question_string = generate_p_q_allele_calc_question(given_var, p)
	elif given_var == '2pq + q2':
		question_string = generate_2pq_q2_calc_question(p)
	elif given_var in ('p2 + 2pq','q2'):
		# given_var in q2 or p2+2pq
		question_string = generate_complete_dom_question(given_var, p)
	else:
		# given_var in p2 or 2pq
		question_string = generate_incomplete_dom_question(given_var, p)
	return question_string, answer_string

#====================================
#====================================
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	# Add question type argument with choices
	parser.add_argument('-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='number of duplicate runs to do', default=1)
	args = parser.parse_args()

	choices_list = list(choices_dict.values())
	#print(choices_list)

	outfile = ('bbq-' + os.path.splitext(os.path.basename(__file__))[0]
		+ '-questions.txt')
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	N = 0
	for i in range(args.duplicates):
		N += 1

		question_string, answer_string = generate_hw_problem()
		if len(question_string) < 5:
			continue

		final_question = bptools.formatBB_MC_Question(N, question_string, choices_list, answer_string)

		f.write(final_question)
	f.close()
	bptools.print_histogram()

#THE END
