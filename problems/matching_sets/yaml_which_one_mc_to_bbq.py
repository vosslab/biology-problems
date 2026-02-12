#!/usr/bin/env python3

"""
This program creates all permutations of matching pairs

MAT TAB question text TAB answer text TAB matching text TAB answer two text TAB matching two text
"""

import os
import sys
import pprint
import random
import argparse
import re

import bptools
from qti_package_maker.assessment_items import item_bank
from qti_package_maker.engines.bbq_text_upload import read_package as bbq_read_package

CONTENT_ID_RE = re.compile(r"<p>([0-9a-f]{4}_[0-9a-f]{4})</p>")


#=======================
#=======================
#=======================
""""
def makeQuestions(yaml_data, num_choices=None):
	matching_pairs_dict = yaml_data['matching pairs']
	exclude_pairs_list = yaml_data.get('exclude pairs', [])

	list_of_complete_questions = []

	if num_choices is None:
		num_choices = yaml_data.get('items to match per question', 5)

	all_keys = list(matching_pairs_dict.keys())
	print('Shuffling {0} items'.format(len(all_keys)))
	all_combs = list(itertools.combinations(all_keys, num_choices))
	print('Created {0} combinations from {1} items'.format(len(all_combs), len(all_keys)))
	#filter combinations
	if len(exclude_pairs_list) > 0:
		filter_combs = []
		for comb in all_combs:
			excluded_comb = False
			#print(comb)
			for a,b in exclude_pairs_list:
				if a in comb and b in comb:
					excluded_comb = True
			if excluded_comb is False:
				filter_combs.append(comb)
		print('Filtered down to {0} combinations from {1} items'.format(len(filter_combs), len(all_combs)))
		all_combs = filter_combs
	random.shuffle(all_combs)
	N = 0
	for comb in all_combs:
		choices_list = list(comb)
		random.shuffle(choices_list)
		answer = choices_list[0]
		answer_description = matching_pairs_dict[answer]
		if isinstance(answer_description, list):
			answer_description = random.choice(answer_description)
		random.shuffle(choices_list)
		question = ("<p>Which one of the following {0} correspond to the {1} <strong>'{2}'</strong>.</p>".format(
			yaml_data['key description'], yaml_data['value description'], answer_description))
		N += 1
		complete_question = bptools.formatBB_MC_Question(N, question, choices_list, answer)

		list_of_complete_questions.append(complete_question)

	list_of_complete_questions = bptools.applyReplacementRulesToList(list_of_complete_questions, yaml_data.get('replacement_rules'))
	return list_of_complete_questions
"""

#=======================
def makeQuestions2(yaml_data, num_choices=None, flip=False):
	matching_pairs_dict = yaml_data['matching pairs']
	exclude_pairs_list = yaml_data.get('exclude pairs', [])

	list_of_complete_questions = []

	if num_choices is None:
		num_choices = yaml_data.get('items to match per question', 5)
	### Get Keys and Key/Values Pairs
	all_keys = list(matching_pairs_dict.keys())
	key_value_pairs = []
	for key in all_keys:
		for value in matching_pairs_dict[key]:
			pair = (key, value)
			key_value_pairs.append(pair)
	random.shuffle(key_value_pairs)
	print('Preparing scenario pools from {0} items'.format(len(all_keys)))
	if num_choices > len(all_keys):
		print("No questions generated: num_choices exceeds available key count.")
		return list_of_complete_questions

	exclude_pair_set = {tuple(sorted((a, b))) for a, b in exclude_pairs_list}

	def _scenario_is_allowed(scenario_tuple: tuple) -> bool:
		if len(exclude_pair_set) == 0:
			return True
		scenario_key_set = set(scenario_tuple)
		for a, b in exclude_pair_set:
			if a in scenario_key_set and b in scenario_key_set:
				return False
		return True

	def _build_scenarios_for_key(key: str, target_count: int=24) -> list[tuple]:
		other_keys = [k for k in all_keys if k != key]
		pick_count = num_choices - 1
		if pick_count < 0 or pick_count > len(other_keys):
			return []
		if pick_count == 0:
			singleton = (key,)
			return [singleton] if _scenario_is_allowed(singleton) else []

		scenario_set = set()
		max_attempts = max(64, target_count * 20)
		for _ in range(max_attempts):
			distractors = random.sample(other_keys, pick_count)
			scenario_tuple = tuple(sorted([key] + distractors))
			if not _scenario_is_allowed(scenario_tuple):
				continue
			scenario_set.add(scenario_tuple)
			if len(scenario_set) >= target_count:
				break
		return list(scenario_set)

	scenarios_by_key = {}
	scenario_index_by_key = {}
	for key in all_keys:
		key_scenarios = _build_scenarios_for_key(key)
		# Option 2b (random order, no repeats until exhausted): shuffle once, then modulo index.
		random.shuffle(key_scenarios)
		scenarios_by_key[key] = key_scenarios
		scenario_index_by_key[key] = 0

	total_scenarios = sum(len(v) for v in scenarios_by_key.values())
	print('Prepared {0} scenarios across {1} keys'.format(total_scenarios, len(all_keys)))

	N = 0
	for pair in key_value_pairs[:2]:
		key, value = pair
		key_scenarios = scenarios_by_key.get(key, [])
		if len(key_scenarios) == 0:
			continue

		scenario_idx = scenario_index_by_key[key] % len(key_scenarios)
		scenario = key_scenarios[scenario_idx]
		scenario_index_by_key[key] += 1

		if flip is False:
			item_name = value
			plural_choice_description = yaml_data['keys description']
			singular_item_description = yaml_data['value description']
			choices_list = list(scenario)
			choices_list.sort()
			answer = key
		else:
			print("Flipping the question")
			item_name = key
			plural_choice_description = yaml_data['values description']
			singular_item_description =yaml_data['key description']
			choices_list = [value, ]
			for scenario_key in scenario:
				if scenario_key == key:
					continue
				choice = random.choice(matching_pairs_dict[scenario_key])
				choices_list.append(choice)
			choices_list.sort()
			answer = value

		question = (
			f"<p>Which one of the following {plural_choice_description} "
			f"correspond to the {singular_item_description} "
			f"<span style='font-size: 1em;'><strong>'{item_name}'</strong></span>.</p>"
		)
		question = bptools.applyReplacementRulesToText(question, yaml_data.get('replacement_rules'))
		choices_list = bptools.applyReplacementRulesToList(choices_list, yaml_data.get('replacement_rules'))
		answer = bptools.applyReplacementRulesToText(answer, yaml_data.get('replacement_rules'))

		N += 1
		complete_question = bptools.formatBB_MC_Question(N, question, choices_list, answer)
		list_of_complete_questions.append(complete_question)

	#list_of_complete_questions = bptools.applyReplacementRulesToList(list_of_complete_questions, yaml_data.get('replacement_rules'))
	return list_of_complete_questions

#=======================
#=======================
def parse_arguments():
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('-f', '-y', '--file', metavar='<file>', type=str, dest='input_yaml_file',
		help='yaml input file to process')
	parser.add_argument('-x', '--max-questions', metavar='#', type=int, dest='max_questions',
		help='max number of questions', default=199)
	parser.add_argument('-d', '--duplicate-runs', metavar='#', type=int, dest='duplicate_runs',
		help='if more than one value is provided for each choice, run duplicates', default=1)
	parser.add_argument('-c', '--num-choices', metavar='#', type=int, dest='num_choices',
		help='how many choices to have for each question', default=None)
	parser.add_argument('--flip', action='store_true', dest='flip', help='Flip the keys and values from the YAML input')
	parser = bptools.add_anticheat_args(parser)
	args = parser.parse_args()
	return args

#=======================
#=======================
def get_question_content_id(bbformat_question: str) -> str | None:
	match = CONTENT_ID_RE.search(bbformat_question)
	if match is None:
		return None
	return match.group(1)

#=======================
#=======================
def sync_bptools_histogram_to_item_bank(output_item_bank):
	bptools.answer_histogram.clear()
	bptools.question_count = 0

	for crc_key in output_item_bank.items_dict_key_list:
		item_cls = output_item_bank.items_dict[crc_key]
		if item_cls.item_type == "MC":
			letter = bptools.letters[item_cls.answer_index]
			bptools.answer_histogram[letter] += 1
		elif item_cls.item_type == "MA":
			for answer_index in item_cls.answer_index_list:
				letter = bptools.letters[answer_index]
				bptools.answer_histogram[letter] += 1
		bptools.question_count += 1

#=======================
#=======================
def main():
	args = parse_arguments()
	bptools.apply_anticheat_args(args)

	if args.input_yaml_file is None or not os.path.isfile(args.input_yaml_file):
		print("Usage: {0} -y <input_yaml_file>".format(__file__))
		sys.exit(0)

	yaml_data = bptools.readYamlFile(args.input_yaml_file)
	pprint.pprint(yaml_data)

	list_of_complete_questions = []
	for i in range(args.duplicate_runs):
		list_of_complete_questions += makeQuestions2(
			yaml_data,
			args.num_choices,
			args.flip,
		)

	if len(list_of_complete_questions) > args.max_questions:
		print("Too many questions, trimming down to {0} questions".format(args.max_questions))
		random.shuffle(list_of_complete_questions)
		less_questions = list_of_complete_questions[:args.max_questions]
		list_of_complete_questions = less_questions

	outfile = 'bbq-WOMC-' + os.path.splitext(os.path.basename(args.input_yaml_file))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	N = 0
	skipped_dupes = 0
	seen_content_ids = set()
	output_item_bank = item_bank.ItemBank(allow_mixed=False)
	for i, question_output in enumerate(list_of_complete_questions, start=1):
		bbformat_question = bptools.normalize_question_output(question_output, str(i))
		if bbformat_question is None:
			continue
		content_id = get_question_content_id(bbformat_question)
		if content_id is not None:
			if content_id in seen_content_ids:
				skipped_dupes += 1
				continue
			seen_content_ids.add(content_id)

		item_cls = bbq_read_package.make_item_cls_from_line(bbformat_question)
		if item_cls is None:
			continue
		before_count = len(output_item_bank.items_dict_key_list)
		output_item_bank.add_item_cls(item_cls)
		after_count = len(output_item_bank.items_dict_key_list)
		if after_count == before_count:
			skipped_dupes += 1
			continue
		N += 1
		f.write(bbformat_question)
	f.close()
	print("Wrote {0} questions to file.".format(N))
	if skipped_dupes > 0:
		print("Skipped {0} duplicate questions at write time.".format(skipped_dupes))
	sync_bptools_histogram_to_item_bank(output_item_bank)
	print('')
	bptools.print_histogram()

#=======================
#=======================
if __name__ == '__main__':
	main()
