#!/usr/bin/env python3

import sys
import random
import argparse

import bptools
import restrictlib

#=====================
#=====================
def explore_object(obj, depth=1, max_depth=5):
	if depth > max_depth:
		return "Max depth reached"

	for attr_name in dir(obj):
		if attr_name.startswith('_'):
			continue
		# Exclude dunder methods
		if not attr_name.startswith('__'):
			attr_value = getattr(obj, attr_name, 'N/A')
			print(f"{'  ' * depth}{attr_name} = {attr_value}")

			# Check if this is a bound method
			if callable(attr_value):
				try:
					# Invoke the bound method and explore it
					method_result = attr_value()
					print(f"{'  ' * (depth + 1)}Result of invoking method = {method_result}")
					explore_object(method_result, depth + 1)
				except Exception as e:
					print(f"{'  ' * (depth + 1)}Exception while invoking: {e}")

			# If it's a class, explore its attributes recursively
			elif not isinstance(attr_value, (int, float, str, list, tuple, dict)):
				explore_object(attr_value, depth + 1)

#=====================
#=====================
def writeQuestion(N, enzyme_class, use_overhang_type):
	name = restrictlib.html_monospace(enzyme_class.__name__)
	cut_description = restrictlib.html_monospace(restrictlib.format_enzyme(enzyme_class))
	web_data = restrictlib.get_web_data(enzyme_class)
	organism = web_data.get('Organism')

	# Constructing the quiz question
	opening =  '<p>Restriction enzymes are proteins that cut DNA at specific sequences to produce fragments for further study.'
	source = "These enzymes are obtained from various types of bacteria and "
	source += "have the ability to recognize short nucleotide sequences within a larger DNA molecule.</p>"
	setup = f"<p>The restriction enzyme we are focusing on is <strong><i>{name}</i></strong> and is obtained from the bacteria {organism}.</p>"
	cut_info = f"<p><strong><i>{name}</i></strong> cuts the DNA sequence as follows: {cut_description} where the '|' indicates the cut location.</p>"
	prompt = "<p>Based on this info, can you identify the type of cut this enzyme makes?</p>"

	question = " ".join([opening, source, setup, cut_info, prompt])
	#print(question)
	#sys.exit(0)

	overhang = enzyme_class.overhang()

	answer = None
	choices_list = []
	if use_overhang_type is True:
		answer = overhang
		choices_list = ["5' overhang", "3' overhang", "blunt"]
	else:
		if overhang.endswith("overhang"):
			answer = "sticky end"
		elif overhang == "blunt":
			answer = "blunt end"
		# actual choices
		choices_list = ["sticky end", "blunt end"]
		# wrong choices
		choices_list.extend(["hanger end", "straight edge", "overhang end", ])
	
	if answer is None:
		print("ERROR")
		sys.exit(1)

	#print(question)
	
	random.shuffle(choices_list)
	bbquestion = bptools.formatBB_MC_Question(N, question, choices_list, answer)
	return bbquestion

#=====================
#=====================
def main():
	parser = argparse.ArgumentParser(description="Generate restriction enzyme questions.")
	parser.add_argument("-o", "--overhang_type", default=True, dest='use_overhang_type',
		action="store_true", help="Whether to use overhang type or use end type.")
	parser.add_argument("-e", "--end_type", default=True, dest='use_end_type',
		action="store_false", help="Whether to use overhang type or use end type.")

	args = parser.parse_args()

	enzyme_names = restrictlib.get_enzyme_list()
	N = 0
	random.shuffle(enzyme_names)
	for enzyme_name in enzyme_names:
		N += 1
		enzyme_class = restrictlib.enzyme_name_to_class(enzyme_name)
		writeQuestion(N, enzyme_class, args.use_overhang_type)
		break

#=====================
#=====================
if __name__ == '__main__':
	main()



	#A. 5'-TGCA-3' B. 5'-CTGCA-3' C. 5'-TGCAG-3' D. 5'-ACGT-3'
