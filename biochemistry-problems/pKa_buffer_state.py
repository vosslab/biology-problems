#!/usr/bin/env python3

import sys
import random

import bptools
import bufferslib

bptools.number_to_cardinal(3)

question_text = ("Carbonic acid is diprotic, with pKa's of 6.35 and 10.33, "
+"and has three possible protonation states below. "
+"The protonated form that is most abundant at pH 11 is:")

"Citric acid is triprotic, with pKa's of 3.13, 4.76, and 6.39, "
"and has four possible protonation states below."
"The protonated form that is most abundant at pH 8.0 is:"

"Phosphoric acid is tribasic, with pKa's of 2.14, 6.86, and 12.4,"
"and has four possible protonation states below."
"The protonated form that is most abundant at pH 4 is:"

"is tribasic, with pKa values of 2.14, 6.86, and 12.4,"
"and has four possible protonation states below. The protonated form that is most abundant at pH 4 is:"

#============================
#============================
#============================
def pKa_list_to_words(pKa_list):
	prefix = 'pK<sub>a</sub> value'
	if len(pKa_list) == 1:
		txt1 = '<strong>{0:.2f}</strong>'.format(pKa_list[0])
		return prefix+' of '+txt1
	elif len(pKa_list) == 2:
		txt1 = '<strong>{0:.2f}</strong>'.format(pKa_list[0])
		txt2 = '<strong>{0:.2f}</strong>'.format(pKa_list[1])
		return prefix+'s of '+txt1+' and '+txt2
	elif len(pKa_list) == 3:
		txt1 = '<strong>{0:.2f}</strong>'.format(pKa_list[0])
		txt2 = '<strong>{0:.2f}</strong>'.format(pKa_list[1])
		txt3 = '<strong>{0:.2f}</strong>'.format(pKa_list[2])
		return prefix+'s of '+txt1+', '+txt2+', and '+txt3
	elif len(pKa_list) == 4:
		txt1 = '<strong>{0:.2f}</strong>'.format(pKa_list[0])
		txt2 = '<strong>{0:.2f}</strong>'.format(pKa_list[1])
		txt3 = '<strong>{0:.2f}</strong>'.format(pKa_list[2])
		txt4 = '<strong>{0:.2f}</strong>'.format(pKa_list[3])
		return prefix+'s of '+txt1+', '+txt2+', '+txt3+', and '+txt4
	sys.exit(1)


#============================
#============================
#============================
def get_pH_values(pKa_list, pH_diff_cutoff=0.7):
	all_pH_list = [
		0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0,
		5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0,
		10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0,
	]
	pH_list = []

	for pH in all_pH_list:
		good_value = True
		for pKa in pKa_list:
			if abs(pKa-pH) < pH_diff_cutoff:
				good_value = False
		if good_value is True:
			pH_list.append(pH)
	return pH_list


#============================
#============================
#============================
def write_question(buffer_dict, pH_value):
	question_text = ''
	question_text += ('<p><strong>' + buffer_dict['acid_name'].capitalize()
		+ '</strong> and it\'s conjugate base, ' + buffer_dict['base_name']
		+ ', ' + buffer_dict['description'] + '.</p> ')
	question_text += ('<p>' + buffer_dict['acid_name'].capitalize() + ' is ' + buffer_dict['protic_name']
		+ ' with '+pKa_list_to_words(buffer_dict['pKa_list'])+'.</p> ')
	num_states = len(buffer_dict['state_list'])
	question_text += ('<p>' + buffer_dict['acid_name'].capitalize() + ' has ' + bptools.number_to_cardinal(num_states)
		+' possible protonation states in the choices below.</p> ')
	question_text += ('<p>Which one of the following protonation states is the most abundant at <strong>pH '
		+('{0:.1f}'.format(pH_value)) + '</strong>?</p> ')
	return question_text


#============================
#============================
#============================
N = 1
buffer_dict = bufferslib.get_random_buffer()
pH_list = get_pH_values(buffer_dict['pKa_list'])
#print(pH_list)
pH_value = random.choice(pH_list)
question_text = write_question(buffer_dict, pH_value)
choices_list = bufferslib.format_list_of_chemical_formula_html(buffer_dict['state_list'])
if random.random() < 0.5:
	choices_list.reverse()
answer_state = bufferslib.get_protonation_state(buffer_dict, pH_value)
answer_formula = bufferslib.format_chemical_formula_html(answer_state)
bptools.formatBB_MC_Question(N, question_text, choices_list, answer_formula)
