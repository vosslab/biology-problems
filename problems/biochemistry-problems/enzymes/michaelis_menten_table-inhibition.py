#!/usr/bin/env python3

"""Generate Michaelis-Menten inhibition type identification questions."""

# Standard Library
import math
import random

# Local repo modules
import bptools
import mm_lib

# Module-level scenario list, initialized in main()
SCENARIOS = None

#============================================
def adjust_mm_values(
	km: float, vmax: float, inhibition: str, substrate_concs: list,
) -> tuple:
	"""Compute inhibited Km and Vmax based on the inhibition type.

	Args:
		km: Original Michaelis constant.
		vmax: Original maximum velocity.
		inhibition: One of 'competitive', 'un-competitive', 'non-competitive'.
		substrate_concs: List of substrate concentrations for picking altered Km.

	Returns:
		Tuple of (inhib_km, inhib_vmax).
	"""
	# working copy of substrate concentrations for picking values
	km_pool = substrate_concs[:-2]
	random.shuffle(km_pool)

	if inhibition == "competitive":
		# competitive: Vmax unchanged, Km increases
		inhib_vmax = vmax
		inhib_km = 0
		while inhib_km <= km:
			inhib_km = km_pool.pop()
	elif inhibition == "un-competitive":
		# un-competitive: both Km and Vmax decrease, slope Km/Vmax stays similar
		if round(math.log10(km / 5.0) % 1, 3) < 0.001:
			# value ends with a 5 (like 0.005, 0.05)
			inhib_km = round(km / 2.5, 5)
		else:
			# value ends with 1 or 2
			inhib_km = round(km / 2, 5)
		# keep slope Km/Vmax approximately unchanged
		raw_vmax = vmax * inhib_km / km
		inhib_vmax = round(raw_vmax / 20.0) * 20
	elif inhibition == "non-competitive":
		# non-competitive: Km unchanged, Vmax decreases
		inhib_km = km
		vmax_pool = [20, 40, 60, 80, 100, 120, 140, 160, 180]
		random.shuffle(vmax_pool)
		inhib_vmax = 300
		while inhib_vmax >= vmax:
			inhib_vmax = vmax_pool.pop(0)
	else:
		raise ValueError(f"Unknown inhibition type: {inhibition}")

	# validate the result
	if abs(km - inhib_km) < 1e-5 and abs(vmax - inhib_vmax) < 0.01:
		raise ValueError(
			f"{inhibition}: inhibited values match originals "
			f"(vmax={vmax}, km={km}, inhib_vmax={inhib_vmax}, inhib_km={inhib_km})"
		)
	if inhibition == "competitive" and (inhib_km - km <= 1e-5 or abs(vmax - inhib_vmax) > 0.01):
		raise ValueError(
			f"competitive: Km did not increase or Vmax changed "
			f"(vmax={vmax}, km={km}, inhib_vmax={inhib_vmax}, inhib_km={inhib_km})"
		)
	if inhibition == "un-competitive" and (km - inhib_km <= 1e-5 or vmax - inhib_vmax <= 0):
		raise ValueError(
			f"un-competitive: Km or Vmax did not decrease "
			f"(vmax={vmax}, km={km}, inhib_vmax={inhib_vmax}, inhib_km={inhib_km})"
		)
	if inhibition == "non-competitive" and (abs(km - inhib_km) > 1e-6 or vmax - inhib_vmax <= 0.01):
		raise ValueError(
			f"non-competitive: Km changed or Vmax did not decrease "
			f"(vmax={vmax}, km={km}, inhib_vmax={inhib_vmax}, inhib_km={inhib_km})"
		)

	return inhib_km, inhib_vmax

#============================================
def make_complete_problem(
	N: int, km: float, vmax: float, inhibition: str,
) -> str:
	"""Build a complete MC question asking students to identify the inhibition type.

	Args:
		N: The question number.
		km: The Michaelis constant.
		vmax: Maximum velocity.
		inhibition: Correct inhibition type.

	Returns:
		A formatted Blackboard question string.
	"""
	substrate_concs = mm_lib.SUBSTRATE_CONCS

	# compute uninhibited velocities
	velocities = []
	for s_val in substrate_concs:
		v0 = mm_lib.michaelis_menten(s_val, km, vmax)
		velocities.append(v0)

	# compute inhibited velocities
	inhib_km, inhib_vmax = adjust_mm_values(km, vmax, inhibition, substrate_concs)
	inhibited_velocities = []
	for s_val in substrate_concs:
		v0 = mm_lib.michaelis_menten(s_val, inhib_km, inhib_vmax)
		inhibited_velocities.append(v0)

	# build the data table
	data_table = mm_lib.make_data_table(
		substrate_concs, velocities, vmax,
		inhibited_velocities=inhibited_velocities,
		inhib_vmax=inhib_vmax,
	)

	# build question text
	header = "<p><u>Michaelis-Menten Kinetics and Inhibition Type Determination</u></p>"
	header += "<p>The table below presents data on enzyme activity measured as initial reaction"
	header += " velocities (V<sub>0</sub>) with and without the presence of an inhibitor at various substrate"
	header += " concentrations ([S]).</p>"

	question = "<p>Based on the data provided, determine the type of inhibition show by"
	question += " the inhibitor. Consider how the addition of the inhibitor affects the initial"
	question += " reaction velocities (V<sub>0</sub>) at various substrate concentrations ([S]).</p>"

	question_text = header + data_table + '<br/>' + question

	# build answer choices: 3 real types + 2 fake prefixed types
	choices = ['competitive', 'un-competitive', 'non-competitive']
	extra_prefixes = [
		'ultra', 'hetero', 'homo', 'anti', 'super', 'dis', 'over', 'self',
		'contra', 'intra', 'omni', 'ortho', 'inter', 'mis', 'semi', 'auto',
		'extra', 'hyper', 'pre', 'post', 'eco', 'hypo', 'iso', 'mega', 'para',
		'poly', 'oligo', 'proto', 'pseudo', 'quasi', 'supra', 'idio', 'epi',
	]
	random.shuffle(extra_prefixes)
	for i in range(2):
		prefix = extra_prefixes[i]
		choices.append(prefix + '-competitive')
	choices.sort()

	# format as MC question
	complete_question = bptools.formatBB_MC_Question(
		N, question_text, choices, inhibition
	)
	return complete_question

#============================================
def _get_scenarios() -> list:
	"""Generate all (inhibition, vmax, km) scenario combinations.

	Returns:
		List of (inhibition_type, vmax, km) tuples.
	"""
	# Vmax choices: 40 to 200 in steps of 20
	vmax_choices = [40, 60, 80, 100, 120, 140, 160, 180, 200]
	inhibition_types = ['competitive', 'un-competitive', 'non-competitive']
	km_choices = mm_lib.SUBSTRATE_CONCS[1:6]

	scenarios = []
	for inhibition in inhibition_types:
		for vmax in vmax_choices:
			for km in km_choices:
				scenarios.append((inhibition, vmax, km))
	return scenarios

#============================================
def write_question(N: int, args) -> str:
	"""Create a formatted MC question for inhibition type identification.

	Args:
		N: The question number.
		args: Parsed command-line arguments.

	Returns:
		A formatted question string.
	"""
	if SCENARIOS is None:
		raise ValueError("Scenarios not initialized; run main().")
	idx = (N - 1) % len(SCENARIOS)
	inhibition, vmax, km = SCENARIOS[idx]
	return make_complete_problem(N, km, vmax, inhibition)

#============================================
def parse_arguments():
	"""Parse command-line arguments.

	Returns:
		argparse.Namespace: Parsed arguments.
	"""
	parser = bptools.make_arg_parser(
		description="Generate Michaelis-Menten inhibition table questions.",
	)
	parser = bptools.add_scenario_args(parser)
	args = parser.parse_args()
	return args

#============================================
def main():
	"""Main function that orchestrates question generation and file output."""
	args = parse_arguments()

	global SCENARIOS
	SCENARIOS = _get_scenarios()
	if len(SCENARIOS) == 0:
		raise ValueError("No scenarios were generated.")
	if args.scenario_order == 'random':
		random.shuffle(SCENARIOS)
	if args.max_questions is None or args.max_questions > len(SCENARIOS):
		args.max_questions = len(SCENARIOS)

	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

#============================================
if __name__ == '__main__':
	main()
