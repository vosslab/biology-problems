#!/usr/bin/env python3

import random

import bptools

SINGLE_BOND_GROUPS = [
	"hydroxyl",
	"sulfhydryl",
	"amino",
	"methyl",
]

DOUBLE_BOND_GROUPS = [
	"carbonyl",
	"carboxyl",
	"phosphate",
]

GROUP_COLORS = {
	"carboxyl": "#e60000",
	"sulfhydryl": "#b3b300",
	"amino": "#00b38f",
	"methyl": "#59b300",
	"phosphate": "#e65400",
	"carbonyl": "#00b3b3",
	"hydroxyl": "#0a9bf5",
}


#======================================
#======================================
def shuffle_list(items: list[str]) -> list[str]:
	"""Return a shuffled copy of the input list."""
	shuffled = list(items)
	random.shuffle(shuffled)
	return shuffled


#======================================
#======================================
def trio_key(groups: list[str]) -> str:
	"""Return a canonical key for a trio of functional groups."""
	return "|".join(sorted(groups))


#======================================
#======================================
def format_group_name(group_name: str) -> str:
	"""Return a colored HTML span for a functional group name."""
	color = GROUP_COLORS.get(group_name)
	if color:
		return f"<span style='color: {color}; font-weight: 700;'>{group_name}</span>"
	return group_name


#======================================
#======================================
def format_trio(groups: list[str]) -> str:
	"""Return a comma-separated trio string with randomized order."""
	return ", ".join(format_group_name(group) for group in shuffle_list(groups))


#======================================
#======================================
def build_correct_trio(requires_double: bool) -> list[str]:
	"""Build the correct trio for the prompt type."""
	if requires_double:
		return list(DOUBLE_BOND_GROUPS)
	omit_index = random.randrange(len(SINGLE_BOND_GROUPS))
	return [group for i, group in enumerate(SINGLE_BOND_GROUPS) if i != omit_index]


#======================================
#======================================
def build_mixed_trio() -> list[str]:
	"""Build a mixed-category trio with 2+1 or 1+2 pattern."""
	pattern = random.choice((0, 1))
	if pattern == 0:
		singles = random.sample(SINGLE_BOND_GROUPS, 2)
		doubles = random.sample(DOUBLE_BOND_GROUPS, 1)
	else:
		singles = random.sample(SINGLE_BOND_GROUPS, 1)
		doubles = random.sample(DOUBLE_BOND_GROUPS, 2)
	return singles + doubles


#======================================
#======================================
def generate_choices(num_choices: int) -> tuple[list[str], str, bool]:
	"""Generate choices for a functional-group bond question."""
	requires_double = random.choice((True, False))
	correct_groups = build_correct_trio(requires_double)
	correct_text = format_trio(correct_groups)
	choices = [correct_text]
	seen_keys = {trio_key(correct_groups)}

	max_attempts = 200
	attempts = 0
	while len(choices) < num_choices:
		attempts += 1
		if attempts > max_attempts:
			raise RuntimeError("Could not generate unique distractors.")
		candidate_groups = build_mixed_trio()
		key = trio_key(candidate_groups)
		if key in seen_keys:
			continue
		seen_keys.add(key)
		choices.append(format_trio(candidate_groups))

	random.shuffle(choices)
	return choices, correct_text, requires_double


#======================================
#======================================
def get_question_text(requires_double: bool) -> str:
	"""Return the question text with emphasized bond type."""
	double_emph = "<span style='color: #B45309; font-size: 1.15em; font-weight: 700;'>double bond</span>"
	single_emph = "<span style='color: #00008B; font-size: 1.15em; font-weight: 700;'>only single bonds</span>"
	if requires_double:
		return (
			"<p>Which one of the following sets of three (3) functional groups all contain a "
			f"{double_emph}?</p>"
		)
	return (
		"<p>Which one of the following sets of three (3) functional groups have "
		f"{single_emph}?</p>"
	)


#======================================
#======================================
def write_question(question_num: int, args) -> str:
	"""Create a complete formatted question."""
	assert question_num > 0, "Question number must be positive"
	assert args.num_choices >= 4, "Number of choices must be at least 4"

	choices_list, answer_text, requires_double = generate_choices(args.num_choices)
	question_text = get_question_text(requires_double)

	return bptools.formatBB_MC_Question(question_num, question_text, choices_list, answer_text)


#======================================
#======================================
def main() -> None:
	parser = bptools.make_arg_parser(description="Generate functional group bond questions.")
	parser = bptools.add_choice_args(parser, default=4)
	args = parser.parse_args()

	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)


#======================================
#======================================
if __name__ == "__main__":
	main()
