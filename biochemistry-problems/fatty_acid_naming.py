#!/usr/bin/env python3

import os
import sys
import random

x = 'margin:0; padding:0; letter-spacing:0px; '
double_low_line = '&#8215;'
double_high_line = '<sup>&#9552;</sup>'
COOH_low = '</span><sub>COOH</sub>'
COOH_high = '</span><sup><sup><sup>COOH</sup></sup></sup>'

pre_chain_span = '<span style="font-size: x-large; font-family: courier;">'
debug = True

def add_carbon_to_omega(fatty_acid, omega):
	C2H4 = '/\\'
	chain = ''
	num_carbon_pairs = omega // 2
	for i in range(num_carbon_pairs):
		chain += C2H4
	return chain

def flip_status(status):
	if status == 'low':
		return 'high'
	return 'low'


def make_unsaturated_fatty_acid(chain_length, omega_list):
	# lowest omega is 1
	omegas = list(omega_list)
	omegas.sort()
	C2H4 = '/\\'

	fatty_acid = ''
	fatty_acid += pre_chain_span

	#first_omega = omegas.pop(0)
	#if first_omega % 2 == 0:
	#	#even
	#	fatty_acid += '\\'
	#	first_omega -= 1
	#fatty_acid += add_carbon_to_omega(fatty_acid, first_omega)
	#fatty_acid += double_low_line
	#last_omega = 0
	#status = 'low'

	if (chain_length - len(omegas)) % 2 == 0:
		status = 'low'
		fatty_acid += '\\'
		last_omega = 1
	else:
		status = 'low'
		last_omega = 0

	while len(omegas) > 0:
		this_omega = omegas.pop(0)
		diff_omega = this_omega - last_omega
		#print(this_omega, last_omega, diff_omega)
		last_omega = this_omega
		if diff_omega % 2 == 0:
			status = flip_status(status)
			diff_omega -= 1
			last_omega += 1
		fatty_acid += add_carbon_to_omega(fatty_acid, diff_omega)
		if status == 'high':
			fatty_acid += '/'+double_high_line+'\\'
			status = 'low'
		else:
			fatty_acid += double_low_line
			status = 'low'
	carbons_remain = (chain_length - last_omega)
	carbon_pairs_remain = (carbons_remain - 1) // 2
	print(chain_length, last_omega, carbons_remain, carbon_pairs_remain)
	for i in range(carbon_pairs_remain):
		fatty_acid += C2H4
	if carbons_remain % 2 == 0:
		fatty_acid += '/'+COOH_high
	else:
		fatty_acid += COOH_low
	return fatty_acid

def omegas2deltas(chain_length, omegas):
	deltas = []
	for omega in omegas:
		delta = chain_length - omega
		deltas.append(delta)
	deltas.sort()
	return deltas

def makeOmegaQuestion():
	return makeQuestion('omega')

def makeDeltaQuestion():
	return makeQuestion('delta')

def list2string(items, type):
	string = '<h5>&{0};&ndash;'.format(type) + ','.join(map(str, items)) + '</h5>'
	return string

def makeQuestion(type):
	chain_length = random.randint(14,22)
	#chain_length = random.randint(7,11)*2
	#chain_length = 10
	fatty_acid, omegas = randomFattyAcid(chain_length)
	deltas = omegas2deltas(chain_length, omegas)

	question = "<h4>What is the correct &{1}; ({1}) notation for the {0} carbon fatty acid pictured above?</h4>".format(chain_length, type)
	#question = "<h4>What is the correct &{0}; ({0}) notation for the fatty acid pictured above?</h4>".format(type)
	choices = []
	if type == 'omega':
		answer = list2string(omegas, type)
		wrong = list2string(deltas, type)
	elif type == 'Delta':
		wrong = list2string(omegas, type)
		answer = list2string(deltas, type)
	else:
		print("unknown type:", type)
		sys.exit(1)
	choices.append(answer)
	choices.append(wrong)

	badomegas = []
	baddeltas = []
	justcount = []
	itemslessone = len(omegas) - 1
	for i in range(len(omegas)):
		badomegas.append(omegas[i] + itemslessone - i)
		baddeltas.append(deltas[i] + itemslessone - i)
		justcount.append(i+1)
	choices.append(list2string(badomegas, type))
	choices.append(list2string(baddeltas, type))
	choices.append(list2string(justcount, type))

	random.shuffle(choices)
	random.shuffle(choices)

	no_dups = list(set(choices))
	if len(no_dups) < 5:
		print('duplicate choices error', len(no_dups), '\n')
		return None

	complete = 'MC\t'
	complete += '<p>' + fatty_acid + '</p>'
	complete += question
	for c in choices:
		complete += '\t'+c
		if c == answer:
			complete += "\tCorrect"
		else:
			complete += "\tIncorrect"
	complete += '\n'
	print(complete)
	return complete

def randomFattyAcid(chain_length=None):
	if chain_length is None:
		chain_length = random.randint(16,22)
	omegas = []
	this_omega = random.randint(2,5)
	while this_omega < chain_length-1:
		omegas.append(this_omega)
		this_omega += random.randint(2,5)

	fatty_acid = make_unsaturated_fatty_acid(chain_length, omegas)
	deltas = omegas2deltas(chain_length, omegas)
	if debug is True:
		print("chain_length", chain_length)
		print("omegas", omegas)
		print("deltas", deltas)
		print(fatty_acid)
	return fatty_acid, omegas


if __name__ == '__main__':
	type = 'omega'
	if len(sys.argv) > 1:
		type = sys.argv[1].strip()
	if type.lower().startswith('delta'):
		type = 'Delta' #capital is key
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	duplicates = 92
	for i in range(duplicates):
		complete = makeQuestion(type)
		if complete is not None:
			f.write(complete)
	f.close()
