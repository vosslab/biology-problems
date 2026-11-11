#!/usr/bin/env python3
"""Generate Dr. Caffeine quadratic regression spreadsheet assignments."""

import bptools
import regressionlib


# Authoring contract: apply the completed tutorial to 25 fresh paired observations.
# One NUM answer reports the fitted quadratic model coefficient of determination.
# Common errors: reporting r, a p-value, a percentage, or stale tutorial results.
def write_question(N: int, args):
	"""Return one numeric item, or reject an unsuitable random draw."""
	pairs = regressionlib.generate_data(2)
	if any(not 0 <= score <= 100 for _, score in pairs):
		return None
	r_squared = regressionlib.r_squared(pairs, 2)
	tolerance = 0.001
	question = bptools.formatBB_NUM_Question(
		N, regressionlib.question_text(pairs, 2), r_squared, tolerance, tol_message=False
	)
	return question


def parse_arguments():
	"""Use the shared bank-size and export options."""
	parser = bptools.make_arg_parser(description=__doc__)
	args = parser.parse_args()
	return args


def main():
	"""Write a Blackboard numeric question bank."""
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()
