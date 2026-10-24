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
	label = sex[:-1] if count == 1 else sex
	row = [math.comb(number, k) for k in range(number + 1)]
	text = ("<p>The old woman who lived in a shoe had so many children she didn't know what to do. "
		f"In this version of the rhyme, she has {number} children.</p>"
		f"<p>Row {number} of Pascal's triangle is shown below.</p>")
	text += '<table role="presentation" style="border-collapse: collapse; color: #202020; background: #ffffff;"><tr>'
	for value in row:
		text += f'<td style="border: 1px solid #767676; padding: 6px 8px; text-align: center;">{value}</td>'
	text += '</tr></table>'
	text += (f"<p>To count the birth orders with exactly {count} {label}, "
		f"use the binomial coefficient <strong>{number} choose {count}</strong>:</p>")
	text += binomiallib.binomial_coefficient(number, count)
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
