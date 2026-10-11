#!/usr/bin/env python3

import re
import random
import functools
import itertools
from fractions import Fraction

import bptools
import disorderlib


ALLOWED_ANSWERS = {
	Fraction(0, 1): 'None, 0%',
	Fraction(1, 8): '1/8, 12.5%',
	Fraction(1, 4): '1/4, 25%',
	Fraction(3, 8): '3/8, 37.5%',
	Fraction(1, 2): '1/2, 50%',
	Fraction(3, 4): '3/4, 75%',
}

AD_GENOTYPE_CHOICES = (
	('Aa', 'aa'),
	('aa', 'Aa'),
	('Aa', 'Aa'),
	('aa', 'aa'),
)

XLR_GENOTYPE_CHOICES = (
	('XaY', 'XAXa'),
	('XAY', 'XAXa'),
	('XaY', 'XAXA'),
	('XAY', 'XAXA'),
	('XaY', 'XaXa'),
)

EVENT_TYPES = ('both', 'only_ad', 'only_xlr', 'neither')
GROUP_TYPES = ('sons', 'daughters', 'children')

MALE_COLOR = '#1765ad'
FEMALE_COLOR = '#b32670'
XLR_COLOR = '#886200'
AD_COLOR = '#6f35a5'


#=====================
def color_description_heading(description: str, color: str) -> str:
	"""Color the shared disorder paragraph's opening heading only."""
	heading, body = description.split('</strong>', 1)
	colored_heading = bptools.colorHTMLText(heading + '</strong>', color[1:])
	colored_description = colored_heading + body
	return colored_description


#=====================
def color_question_text(question_text: str, disorder_colors: dict) -> str:
	"""Color gender and trait labels, italicizing wildtype in phenotype labels."""
	word_colors = dict(disorder_colors)
	for word in ('man', 'men', 'father', 'son', 'sons', 'male', 'males'):
		word_colors[word] = MALE_COLOR
	for word in ('woman', 'women', 'mother', 'daughter', 'daughters', 'female', 'females'):
		word_colors[word] = FEMALE_COLOR

	# Match complete names first and include an adjacent gender symbol in its span.
	terms = sorted(word_colors, key=len, reverse=True)
	pattern = r'\b(' + '|'.join(re.escape(term) for term in terms) + r')\b'
	pattern += r'( \(&(?:fe)?male;\))?'

	def color_match(match: re.Match) -> str:
		color = word_colors[match.group(1)]
		label = match.group(0).replace('wildtype', '<em>wildtype</em>')
		label = f'<strong>{label}</strong>'
		colored_label = bptools.colorHTMLText(label, color[1:])
		return colored_label

	colored_text = re.sub(pattern, color_match, question_text)
	return colored_text


#=====================
def prob_autosomal_dominant(father_genotype, mother_genotype):
	if father_genotype == 'Aa' and mother_genotype == 'Aa':
		return Fraction(3, 4)
	if (father_genotype == 'Aa' and mother_genotype == 'aa') or (father_genotype == 'aa' and mother_genotype == 'Aa'):
		return Fraction(1, 2)
	return Fraction(0, 1)


#=====================
def prob_x_linked_recessive(group, father_genotype, mother_genotype):
	if group == 'sons':
		if mother_genotype == 'XAXA':
			return Fraction(0, 1)
		if mother_genotype == 'XAXa':
			return Fraction(1, 2)
		return Fraction(1, 1)
	if group == 'daughters':
		if father_genotype == 'XaY' and mother_genotype == 'XAXa':
			return Fraction(1, 2)
		if father_genotype == 'XaY' and mother_genotype == 'XaXa':
			return Fraction(1, 1)
		return Fraction(0, 1)
	return (prob_x_linked_recessive('sons', father_genotype, mother_genotype)
		+ prob_x_linked_recessive('daughters', father_genotype, mother_genotype)) / 2


#=====================
def probability_for_event(event, group, ad_genotypes, xlr_genotypes):
	p_ad = prob_autosomal_dominant(ad_genotypes[0], ad_genotypes[1])
	p_xlr = prob_x_linked_recessive(group, xlr_genotypes[0], xlr_genotypes[1])
	if event == 'both':
		return p_ad * p_xlr
	if event == 'only_ad':
		return p_ad * (1 - p_xlr)
	if event == 'only_xlr':
		return (1 - p_ad) * p_xlr
	return (1 - p_ad) * (1 - p_xlr)


#=====================
def ad_person_sentence(role, genotype, disorder_short_name, unaffected_phenotype):
	if genotype == 'Aa':
		parent = random.choice(('father (&male;)', 'mother (&female;)'))
		sentence = (
			f'The {role} has {disorder_short_name}. '
			f'The {parent} of the {role} has {unaffected_phenotype}.'
		)
	else:
		sentence = f'The {role} has {unaffected_phenotype}.'
	return sentence


#=====================
def ad_story(ad_genotypes, disorder_short_name, unaffected_phenotype):
	man_genotype, woman_genotype = ad_genotypes
	story = ' '.join([
		ad_person_sentence('man (&male;)', man_genotype, disorder_short_name, unaffected_phenotype),
		ad_person_sentence('woman (&female;)', woman_genotype, disorder_short_name, unaffected_phenotype),
	])
	return story


#=====================
def xlr_story(xlr_genotypes, disorder_short_name, unaffected_phenotype):
	man_genotype, woman_genotype = xlr_genotypes
	lines = []
	if man_genotype == 'XaY':
		lines.append(f'The man (&male;) has {disorder_short_name}.')
	else:
		lines.append(f'The man (&male;) has {unaffected_phenotype}.')
	if woman_genotype == 'XAXa':
		# Her phenotype and affected father let students infer her carrier genotype.
		lines.append(
			f'The woman (&female;) has {unaffected_phenotype}. '
			f'The father (&male;) of the woman (&female;) has {disorder_short_name}.'
		)
	elif woman_genotype == 'XaXa':
		lines.append(
			f'The woman (&female;) has {disorder_short_name}; her father has {disorder_short_name} as well.'
		)
	else:
		# Phenotype alone cannot distinguish a carrier from a non-carrier.
		lines.append(
			f'The woman (&female;) has {unaffected_phenotype}. '
			f'Genetic testing shows she is not a carrier for {disorder_short_name}.'
		)
	story = ' '.join(lines)
	return story


#=====================
def event_phrase(event, xlr_short_name, ad_short_name, xlr_unaffected, ad_unaffected):
	if event == 'both':
		phrase = f'both {xlr_short_name} and {ad_short_name}'
	elif event == 'only_ad':
		phrase = f'{ad_short_name} and {xlr_unaffected}'
	elif event == 'only_xlr':
		phrase = f'{xlr_short_name} and {ad_unaffected}'
	else:
		phrase = f'{xlr_unaffected} and {ad_unaffected}'
	return phrase


#=====================
def group_phrase(group):
	if group == 'sons':
		return 'sons (&male;)'
	if group == 'daughters':
		return 'daughters (&female;)'
	return 'children (sons and daughters equally likely)'


#=====================
@functools.cache
def scenarios_by_answer() -> dict:
	"""Group supported scenarios in which both traits vary in the requested group."""
	scenarios = {}
	for ad_genotypes, xlr_genotypes, event, group in itertools.product(
		AD_GENOTYPE_CHOICES, XLR_GENOTYPE_CHOICES, EVENT_TYPES, GROUP_TYPES,
	):
		p_ad = prob_autosomal_dominant(*ad_genotypes)
		p_xlr = prob_x_linked_recessive(group, *xlr_genotypes)
		# A fixed trait turns the joint question into a one-trait calculation.
		if not (0 < p_ad < 1 and 0 < p_xlr < 1):
			continue
		prob = probability_for_event(event, group, ad_genotypes, xlr_genotypes)
		if prob in ALLOWED_ANSWERS:
			scenarios.setdefault(prob, []).append((ad_genotypes, xlr_genotypes, event, group, prob))
	return scenarios


#=====================
def generate_scenario() -> tuple:
	# Give each attainable answer equal weight, then choose a compatible scenario.
	scenarios = scenarios_by_answer()
	prob = random.choice(tuple(scenarios))
	scenario = random.choice(scenarios[prob])
	return scenario


#=====================
def write_question(N, args):
	md = disorderlib.MultiDisorderClass()

	XLR_disorder_dict = md.randomDisorderDict('X-linked recessive')
	AD_disorder_dict = md.randomDisorderDict('autosomal dominant')
	XLR_description = md.getDisorderParagraph(XLR_disorder_dict)
	AD_description = md.getDisorderParagraph(AD_disorder_dict)
	XLR_short_name = md.getDisorderShortName(XLR_disorder_dict)
	AD_short_name = md.getDisorderShortName(AD_disorder_dict)
	XLR_unaffected = XLR_disorder_dict['unaffected phenotype']
	AD_unaffected = AD_disorder_dict['unaffected phenotype']

	ad_genotypes, xlr_genotypes, event, group, prob = generate_scenario()

	# Keep background details neutral, with a small gap before the family scenario.
	background_text = '<p style="margin: 0;">'
	background_text += color_description_heading(XLR_description, XLR_COLOR) + '</p>'
	background_text += '<p style="margin: 0 0 0.75em;">'
	background_text += color_description_heading(AD_description, AD_COLOR) + '</p>'

	# Group the family facts by disease and give the final question its own paragraph.
	paragraph_start = '<p style="margin: 0 0 0.75em;">'
	question_text = paragraph_start
	question_text += 'A man (&male;) and a woman (&female;) are planning a family. '
	question_text += xlr_story(xlr_genotypes, XLR_short_name, XLR_unaffected) + '</p>'
	question_text += paragraph_start + ad_story(ad_genotypes, AD_short_name, AD_unaffected) + '</p>'
	question_text += (
		f'<p style="margin: 0;"><em>Reminder: {XLR_short_name} is {XLR_disorder_dict["type"]} '
		f'and {AD_short_name} is {AD_disorder_dict["type"]}.</em></p>'
	)
	question_text += (
		f'<p style="margin: 0.75em 0 0;">What fraction of their {group_phrase(group)} will have '
		f'{event_phrase(event, XLR_short_name, AD_short_name, XLR_unaffected, AD_unaffected)}?</p>'
	)
	disorder_colors = {
		XLR_short_name: XLR_COLOR,
		AD_short_name: AD_COLOR,
		XLR_unaffected: XLR_COLOR,
		AD_unaffected: AD_COLOR,
	}
	question_text = background_text + color_question_text(question_text, disorder_colors)

	# Both five-choice ladders contain every attainable answer. Choose independently
	# of the key, varying the 0% versus 75% distractor without changing numeric order.
	choice_start = random.randrange(2)
	choices_list = list(ALLOWED_ANSWERS.values())[choice_start:choice_start + 5]
	answer_text = ALLOWED_ANSWERS[prob]
	bb_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
	return bb_question


#===========================================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate questions.")
	args = parser.parse_args()
	return args


#===========================================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)


#=====================
if __name__ == '__main__':
	main()
