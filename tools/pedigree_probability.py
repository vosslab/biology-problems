#!/usr/bin/env python3
"""Read a pedigree with original genotypes and print a Monte Carlo diagnostic."""

import argparse
import json
import pathlib
import sys

import numpy

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]
	/ 'problems' / 'inheritance-problems' / 'pedigrees'))
import pedigree_lib.family as family_model
import pedigree_lib.offspring_probability as offspring_probability


#============================================
def parse_args():
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-i', '--input', dest='input_file', required=True,
		help='JSON containing mode, people (id, sex, genotype), and unions')
	parser.add_argument('-s', '--seed', dest='seed', type=int, default=0,
		help='Reproducible Monte Carlo seed (default: 0)')
	parser.add_argument('-n', '--simulations', dest='simulations', type=int, default=9999,
		help='Monte Carlo draws (default: 9999)')
	args = parser.parse_args()
	return args


#============================================
def main():
	args = parse_args()
	# ASVS 1.5.2: deserialize plain JSON data, never executable objects.
	with open(args.input_file, encoding='utf-8') as stream:
		record = json.load(stream)
	people = tuple(family_model.Person(row['id'], row['sex']) for row in record['people'])
	unions = tuple(family_model.Union(row['father'], row['mother'], tuple(row['children']))
		for row in record['unions'])
	genotypes = {row['id']: tuple(row['genotype']) for row in record['people']}
	report = offspring_probability.diagnose(family_model.Family(people, unions),
		record['mode'], genotypes, numpy.random.default_rng(args.seed), args.simulations)
	print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == '__main__':
	main()
