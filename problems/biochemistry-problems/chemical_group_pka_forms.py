#!/usr/bin/env python3

import random

import bptools


HYDROGEN_CHOICES = [
	"<span style='color:#2f855a;font-weight:700;'>no hydrogens (0 H)</span>",
	"<span style='color:#2f855a;font-weight:700;'>one hydrogen (1 H)</span>",
	"<span style='color:#2f855a;font-weight:700;'>two hydrogens (2 H)</span>",
	"<span style='color:#2f855a;font-weight:700;'>three hydrogens (3 H)</span>",
]

CHARGE_CHOICES = [
	"<span style='color:#1f5aa6;font-weight:700;'>positive charge (+)</span>",
	"<span style='color:#111111;font-weight:700;'>neutral charge (0)</span>",
	"<span style='color:#c1121f;font-weight:700;'>negative charge (-)</span>",
]

HYDROGEN_LABELS = {
	0: HYDROGEN_CHOICES[0],
	1: HYDROGEN_CHOICES[1],
	2: HYDROGEN_CHOICES[2],
	3: HYDROGEN_CHOICES[3],
}

CHARGE_LABELS = {
	"positive": CHARGE_CHOICES[0],
	"neutral": CHARGE_CHOICES[1],
	"negative": CHARGE_CHOICES[2],
}


#======================================
#======================================
def build_prompt(group_key: str, position_emph: str) -> str:
	"""Return the question prompt for the chosen scenario."""
	group_labels = {
		"carboxyl": "<span style='color:#c62828;font-weight:700;'>carboxyl group</span>",
		"amine": "<span style='color:#1565c0;font-weight:700;'>amine group</span>",
		"thiol": "<span style='color:#b58900;font-weight:700;'>thiol group</span>",
	}
	group_examples = {
		"carboxyl": "-COOH",
		"amine": "-NH<sub>2</sub>",
		"thiol": "-SH",
	}
	prompt_prefix = "When the pH is more than two (2) pH units"
	prompt_tail = "what form is the chemical group in?"
	group_label = group_labels[group_key]
	group_example = group_examples[group_key]
	both_emph = "<span style='font-weight:700;'>BOTH</span>"
	hydrogen_emph = "<span style='color:#2f855a;font-weight:700;'>number of hydrogens</span>"
	charge_emph = "<span style='color:#6b21a8;font-weight:700;'>its charge</span>"
	check_emph = "<span style='font-weight:700;'>check two boxes</span>"
	return (
		f"<p>{prompt_prefix} {position_emph} the pKa of a {group_label} "
		f"(e.g., {group_example}), {prompt_tail}</p>"
		f"<p>Select {both_emph} the {hydrogen_emph} and {charge_emph}; {check_emph}.</p>"
	)


#======================================
#======================================
def pick_scenario() -> dict:
	"""Return a randomized scenario definition."""
	above_emph = "<span style='color:#d96500;font-weight:700;'>ABOVE</span>"
	below_emph = "<span style='color:#1f7a1f;font-weight:700;'>BELOW</span>"
	scenarios = [
		{"group": "carboxyl", "position": above_emph, "hydrogens": 0, "charge": "negative"},
		{"group": "carboxyl", "position": below_emph, "hydrogens": 1, "charge": "neutral"},
		{"group": "amine", "position": above_emph, "hydrogens": 2, "charge": "neutral"},
		{"group": "amine", "position": below_emph, "hydrogens": 3, "charge": "positive"},
		{"group": "thiol", "position": above_emph, "hydrogens": 0, "charge": "negative"},
		{"group": "thiol", "position": below_emph, "hydrogens": 1, "charge": "neutral"},
	]
	return random.choice(scenarios)


#======================================
#======================================
def generate_answers(scenario: dict) -> list[str]:
	"""Return the list of correct answers for the scenario."""
	hydrogen_text = HYDROGEN_LABELS[scenario["hydrogens"]]
	charge_text = CHARGE_LABELS[scenario["charge"]]
	return [hydrogen_text, charge_text]


#======================================
#======================================
def write_question(question_num: int, args) -> str:
	"""Create a complete formatted question."""
	assert question_num > 0, "Question number must be positive"

	scenario = pick_scenario()
	question_text = build_prompt(scenario["group"], scenario["position"])
	choices_list = HYDROGEN_CHOICES + CHARGE_CHOICES
	answers_list = generate_answers(scenario)
	return bptools.formatBB_MA_Question(
		question_num,
		question_text,
		choices_list,
		answers_list,
		min_answers_required=2,
		allow_all_correct=False,
	)


#======================================
#======================================
def main() -> None:
	parser = bptools.make_arg_parser(
		description="Generate protonation form questions for groups above/below pKa."
	)
	args = parser.parse_args()

	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)


#======================================
#======================================
if __name__ == "__main__":
	main()
