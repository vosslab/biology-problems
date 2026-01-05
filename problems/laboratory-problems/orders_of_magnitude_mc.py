#!/usr/bin/env python3

import random
import locale
import bptools


locale.setlocale(locale.LC_ALL, 'en_US')

units = {
	'M': 'molar',
	'g': 'grams',
	'L': 'liters',
	'mol': 'moles'
}

unit_orders = {
	'M': ['', 'm', '&mu;', 'n'],
	'g': ['k', '', 'm', '&mu;', 'n'],
	'L': ['k', '', 'm', '&mu;', 'n'],
	'mol': ['m', '&mu;', 'n'],
}

orders = ['k', '', 'm', '&mu;', 'n']

up_values = [500, 200, 100, 50, 20, 10, 5, 2, 1]
down_values = [0.1, 0.2, 0.5, 1]

order_names = {
	'k': 'kilo',
	'': '',
	'm': 'milli',
	'&mu;': 'micro',
	'n': 'nano',
}

order_factors = {
	'k': 3,
	'': 0,
	'm': -3,
	'&mu;': -6,
	'n': -9,
}

#==================================================
def build_scenarios():
	scenarios = []
	for unit in units:
		for value in down_values:
			for i in range(2, len(unit_orders[unit])):
				first_prefix = unit_orders[unit][i-1]
				second_prefix = unit_orders[unit][i]
				scenarios.append((value, first_prefix, second_prefix, unit))
		for value in up_values:
			for i in range(2, len(unit_orders[unit])):
				first_prefix = unit_orders[unit][i]
				second_prefix = unit_orders[unit][i-1]
				scenarios.append((value, first_prefix, second_prefix, unit))
	return scenarios

SCENARIOS = build_scenarios()

#==================================================
#==================================================
def question_text(value, first_prefix, unit):
	formed_str = format_value(value, first_prefix, unit)
	question = "<p>Order of Magnitude Units</p>"
	question = "<p>Which one of the following values is equal to: <strong>{0}</strong>?</p>".format(formed_str)
	return question

#==================================================
#==================================================
#==================================================
#==================================================
def format_value(value, prefix, unit):
	if value >= 10:
		formed_str = "{0:,.0f} {1}{2}".format(value, prefix, unit)
	elif value >= 1:
		formed_str = "{0:.0f} {1}{2}".format(value, prefix, unit)
	elif value >= 0.1:
		formed_str = "{0:.1f} {1}{2}".format(value, prefix, unit)
	elif value >= 0.01:
		formed_str = "{0:.2f} {1}{2}".format(value, prefix, unit)
	elif value >= 0.001:
		formed_str = "{0:.3f} {1}{2}".format(value, prefix, unit)
	elif value >= 0.0001:
		formed_str = "{0:.4f} {1}{2}".format(value, prefix, unit)
	elif value >= 1e-5:
		formed_str = "{0:.5f} {1}{2}".format(value, prefix, unit)
	elif value >= 1e-6:
		formed_str = "{0:.6f} {1}{2}".format(value, prefix, unit)
	elif value >= 1e-7:
		formed_str = "{0:.7f} {1}{2}".format(value, prefix, unit)
	return formed_str

#==================================================
#==================================================
def make_choices(value, first_prefix, second_prefix, unit):

	factor = order_factors[first_prefix] - order_factors[second_prefix]
	mult_factor = 10**factor
	answer_value = value*mult_factor
	answer_str = format_value(answer_value, second_prefix, unit)

	inverse_factor = 10**-factor
	inverse_value = value*inverse_factor

	choice_values = [answer_value, inverse_value]
	wrong_values = [
		answer_value*10, answer_value*100,
		answer_value/10.0, answer_value/100.0,
		inverse_value*10, inverse_value*100,
		inverse_value/10.0, inverse_value/100.0,
	]
	wrong_values = list(set(wrong_values))
	random.shuffle(wrong_values)
	choice_values += wrong_values[:3]
	choice_values.sort()

	choices = []
	for choice_value in choice_values:
		choice_str = format_value(choice_value, second_prefix, unit)
		choices.append(choice_str)

	return choices, answer_str

#==================================================
#==================================================
def write_question(N: int, args) -> str:
	value, first_prefix, second_prefix, unit = random.choice(SCENARIOS)
	q = question_text(value, first_prefix, unit)
	choices, answer = make_choices(value, first_prefix, second_prefix, unit)
	bbf = bptools.formatBB_MC_Question(N, q, choices, answer)
	return bbf

def parse_arguments():
	parser = bptools.make_arg_parser(
		description="Generate orders of magnitude questions."
	)
	args = parser.parse_args()
	return args

def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(None)
	bptools.collect_and_write_questions(write_question, args, outfile)

if __name__ == '__main__':
	main()
