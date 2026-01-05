#!/usr/bin/env python3

import random
import bptools

df_ratios = [
	(2, 1), (3, 1), (4, 1),
	(3, 2), (5, 2), (7, 2),
	(4, 3), (5, 3), (7, 3), (8, 3),
	(5, 4), (7, 4), (9, 4),
	(6, 5), (7, 5), (8, 5), (9, 5),
]


#==================================================
#==================================================
def question_text(volume, df1, df2):
	volume_text = f"<span style='font-family: monospace;'>{volume} &mu;L</span>"
	question = (
		f"<p>Using a previous diluted sample at DF={df1}, "
		f"create a new dilution with a final dilution of DF={df2} and a total volume of {volume_text}.</p>"
		"<p>What volume of aliquot in microliters (&mu;L) do you add to distilled water to make the dilution?</p>"
	)
	return question

#==================================================
#==================================================
def df_ratio_to_values(df_ratio):
	#dfsum = df_ratio[0] + df_ratio[1]
	max_int = 100 // df_ratio[0]
	volume = df_ratio[0] * random.randint(1, max_int) * 10
	multiplier = random.choice((4,5,8,10,20,25,40,50))
	df1 = df_ratio[1]*multiplier
	df2 = df_ratio[0]*multiplier
	return volume, df1, df2

#==================================================
#==================================================
scenario_list = [df_ratio for df_ratio in df_ratios if df_ratio[1] >= 3]

#==================================================
def _select_scenario_index(N: int, count: int, mode: str) -> int:
	if mode == 'cycle':
		return (N - 1) % count
	if mode == 'modmix':
		return (N * 2654435761) % count
	if mode == 'random':
		return random.randrange(count)
	raise ValueError("Unknown scenario selection mode.")

#==================================================
def write_question(N: int, args) -> str:
	idx = _select_scenario_index(N, len(scenario_list), args.scenario_select)
	df_ratio = scenario_list[idx]
	volume, df1, df2 = df_ratio_to_values(df_ratio)
	q = question_text(volume, df1, df2)
	aliquot = volume * df_ratio[1] / df_ratio[0]
	answer = aliquot
	tolerance = 0.9
	complete_question = bptools.formatBB_NUM_Question(N, q, answer, tolerance)
	return complete_question

#==================================================
def parse_arguments():
	parser = bptools.make_arg_parser(
		description="Generate serial dilution aliquot questions."
	)
	parser.add_argument(
		'--scenario-select', dest='scenario_select', type=str,
		choices=('cycle', 'modmix', 'random'),
		default='modmix', help='Scenario selection mode.'
	)
	args = parser.parse_args()
	return args

#==================================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

#==================================================
if __name__ == '__main__':
	main()
