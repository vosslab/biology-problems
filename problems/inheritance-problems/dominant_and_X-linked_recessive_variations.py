#!/usr/bin/env python3

import random
from fractions import Fraction

import bptools
import disorderlib


ALLOWED_ANSWERS = {
	Fraction(0, 1): 'None, 0%',
	Fraction(1, 4): '1/4, 25%',
	Fraction(1, 2): '1/2, 50%',
	Fraction(3, 4): '3/4, 75%',
	Fraction(1, 1): 'All, 100%',
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
def ad_person_sentence(role, genotype, disorder_short_name):
	if genotype == 'Aa':
		parent = random.choice(('father (&male;)', 'mother (&female;)'))
		return f'The {role} has {disorder_short_name}. The {parent} of the {role} does not have {disorder_short_name}.'
	return f'The {role} does not have {disorder_short_name}.'


#=====================
def ad_story(ad_genotypes, disorder_short_name):
	man_genotype, woman_genotype = ad_genotypes
	return ' '.join([
		ad_person_sentence('man (&male;)', man_genotype, disorder_short_name),
		ad_person_sentence('woman (&female;)', woman_genotype, disorder_short_name),
	])


#=====================
def xlr_story(xlr_genotypes, disorder_short_name):
	man_genotype, woman_genotype = xlr_genotypes
	lines = []
	if man_genotype == 'XaY':
		lines.append(f'The man (&male;) has {disorder_short_name}.')
	else:
		lines.append(f'The man (&male;) does not have {disorder_short_name}.')
	if woman_genotype == 'XAXa':
		lines.append(
			f'The woman (&female;) is a carrier for {disorder_short_name}; her father has {disorder_short_name}, but her mother does not.'
		)
	elif woman_genotype == 'XaXa':
		lines.append(
			f'The woman (&female;) has {disorder_short_name}; her father has {disorder_short_name} as well.'
		)
	else:
		lines.append(f'Genetic testing shows the woman (&female;) is not a carrier for {disorder_short_name}.')
	return ' '.join(lines)


#=====================
def event_phrase(event, xlr_short_name, ad_short_name):
	if event == 'both':
		return f'both {xlr_short_name} and {ad_short_name}'
	if event == 'only_ad':
		return f'{ad_short_name} but not {xlr_short_name}'
	if event == 'only_xlr':
		return f'{xlr_short_name} but not {ad_short_name}'
	return f'neither {xlr_short_name} nor {ad_short_name}'


#=====================
def group_phrase(group):
	if group == 'sons':
		return 'sons (&male;)' 
	if group == 'daughters':
		return 'daughters (&female;)' 
	return 'children (sons and daughters equally likely)'


#=====================
def generate_scenario():
	for _ in range(200):
		ad_genotypes = random.choice(AD_GENOTYPE_CHOICES)
		xlr_genotypes = random.choice(XLR_GENOTYPE_CHOICES)
		event = random.choice(EVENT_TYPES)
		group = random.choice(GROUP_TYPES)
		prob = probability_for_event(event, group, ad_genotypes, xlr_genotypes)
		if prob in ALLOWED_ANSWERS:
			return ad_genotypes, xlr_genotypes, event, group, prob
	return ('Aa', 'aa'), ('XaY', 'XAXa'), 'both', 'sons', Fraction(1, 4)


#=====================
def write_question(N, args):
	md = disorderlib.MultiDisorderClass()

	XLR_disorder_dict = md.randomDisorderDict('X-linked recessive')
	AD_disorder_dict = md.randomDisorderDict('autosomal dominant')
	XLR_description = md.getDisorderParagraph(XLR_disorder_dict)
	AD_description = md.getDisorderParagraph(AD_disorder_dict)
	XLR_short_name = md.getDisorderShortName(XLR_disorder_dict)
	AD_short_name = md.getDisorderShortName(AD_disorder_dict)

	ad_genotypes, xlr_genotypes, event, group, prob = generate_scenario()

	question_text = ''
	question_text += f'<p>{XLR_description}</p>'
	question_text += f'<p>{AD_description}</p>'
	question_text += '<p>A man (&male;) and a woman (&female;) are planning a family. '
	question_text += xlr_story(xlr_genotypes, XLR_short_name) + ' '
	question_text += ad_story(ad_genotypes, AD_short_name) + '</p>'
	question_text += (
		f'<p>Reminder: {XLR_short_name} is {XLR_disorder_dict["type"]} '
		f'and {AD_short_name} is {AD_disorder_dict["type"]}.</p>'
	)
	question_text += (
		f'<p>What fraction of their {group_phrase(group)} will have '
		f'{event_phrase(event, XLR_short_name, AD_short_name)}?</p>'
	)

	choices_list = md.getStandardChoicesList()
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
