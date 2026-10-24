#!/usr/bin/env python3
"""Connect N choose r notation to entries in Pascal triangle rows."""

import math
import random

import bptools
import binomiallib


def write_question(N: int, args):
	"""Read the coefficient that counts birth orders with exactly r girls or boys."""
	number = random.randint(5, 9)
	count = random.randint(0, number)
	sex = random.choice(("girls", "boys"))
	groups = []
	for group, size, color, symbol in (
		("boys", count if sex == "boys" else number - count, "#0086b3", "&male;"),
		("girls", count if sex == "girls" else number - count, "#b30086", "&female;"),
	):
		label = group[:-1] if size == 1 else group
		groups.append(f'<span style="color: {color};"><strong>'
			f'{bptools.number_to_cardinal(size)} ({size}) {label} {symbol}</strong></span>')
	row = [math.comb(number, k) for k in range(number + 1)]
	text = ("<p>The old woman who lived in a shoe had so many children she didn't know what to do. "
		f"In this version of the rhyme, she has {bptools.number_to_cardinal(number)} ({number}) children.</p>"
		f"<p>Row {number} of Pascal's triangle is shown below.</p>")
	text += (f'<table role="presentation" style="table-layout: fixed; width: {3 * len(row)}em; '
		'max-width: 100%; border-collapse: collapse; color: #202020; background: #ffffff;"><tr>')
	for value in row:
		text += f'<td style="border: 1px solid #767676; padding: 6px 8px; text-align: center;">{value}</td>'
	text += '</tr></table>'
	text += (f"<div>To count the birth orders with exactly {groups[0]} and {groups[1]}, "
		f"use the binomial coefficient <strong>{number} choose {count}</strong>, ")
	text += binomiallib.binomial_coefficient(number, count)
	text += ".</div>"
	text += "<p>What is the value of this coefficient in the row above?</p>"
	answer = str(row[count])
	# Other entries represent choosing the wrong position; symmetric entries share a value.
	distractors = sorted(set(row) - {row[count]})
	values = [row[count]] + random.sample(distractors, min(3, len(distractors)))
	choices = [str(value) for value in sorted(values)]
	return bptools.formatBB_MC_Question(N, text, choices, answer)


def parse_arguments():
	parser = bptools.make_arg_parser(description="Read N choose r from Pascal's triangle.")
	return parser.parse_args()


def main():
	args = parse_arguments()
	outfile = bptools.make_outfile("MC")
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()
