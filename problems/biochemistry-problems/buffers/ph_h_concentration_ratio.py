#!/usr/bin/env python3

import random

import bptools

CONTEXTS = [
	{"name": "battery acid", "pH": 0.8, "color": "#7F1D1D"},
	{"name": "gastric juice", "pH": 1.4, "color": "#B45309"},
	{"name": "lemon juice", "pH": 2.0, "color": "#C2410C"},
	{"name": "vinegar", "pH": 2.4, "color": "#9A3412"},
	{"name": "cola", "pH": 2.5, "color": "#991B1B"},
	{"name": "orange juice", "pH": 3.4, "color": "#EA580C"},
	{"name": "tomato juice", "pH": 4.1, "color": "#B91C1C"},
	{"name": "black coffee", "pH": 5.1, "color": "#3F3F46"},
	{"name": "rainwater", "pH": 5.6, "color": "#2563EB"},
	{"name": "saliva", "pH": 6.8, "color": "#0F766E"},
	{"name": "pure water", "pH": 7.0, "color": "#1D4ED8"},
	{"name": "blood sample", "pH": 7.4, "color": "#7F1D1D"},
	{"name": "seawater", "pH": 8.1, "color": "#0EA5E9"},
	{"name": "baking soda solution", "pH": 8.4, "color": "#0F766E"},
	{"name": "egg white", "pH": 9.0, "color": "#6B7280"},
	{"name": "milk of magnesia", "pH": 10.5, "color": "#64748B"},
	{"name": "household ammonia", "pH": 11.0, "color": "#0B7285"},
	{"name": "bleach", "pH": 12.0, "color": "#7C3AED"},
]

JITTER_VALUES = (-0.1, 0.0, 0.1)


#======================================
#======================================
def power_of_ten_words(exponent: int) -> str:
	"""Return a power-of-ten label with HTML superscripts."""
	words = {
		1: "10 (10<sup>1</sup>)",
		2: "100 (10<sup>2</sup>)",
		3: "1,000 (10<sup>3</sup>)",
		4: "10,000 (10<sup>4</sup>)",
		5: "100,000 (10<sup>5</sup>)",
		6: "1 million (10<sup>6</sup>)",
		7: "10 million (10<sup>7</sup>)",
		8: "100 million (10<sup>8</sup>)",
		9: "1 billion (10<sup>9</sup>)",
	}
	return words.get(exponent, f"10^{exponent}")


#======================================
#======================================
def format_item_name(name: str, color: str) -> str:
	"""Return a bold, colored label for the item name."""
	return f"<span style='color: {color}; font-weight: 700;'>{name}</span>"


#======================================
#======================================
def format_ph_value(ph_text: str) -> str:
	"""Return a monospace pH value string."""
	return f"<span style='font-family: monospace;'>{ph_text}</span>"


#======================================
#======================================
def build_pairs(contexts: list[dict]) -> list[dict]:
	"""Build valid (high, low) pairs whose difference can be nudged to an integer."""
	pairs = []
	for i, hi in enumerate(contexts):
		for j, lo in enumerate(contexts):
			if i == j:
				continue
			if hi["pH"] <= lo["pH"]:
				continue
			diff0 = hi["pH"] - lo["pH"]
			delta_int = int(diff0 + 0.5)
			if abs(diff0 - delta_int) > 0.2 + 1e-9:
				continue
			pairs.append(
				{
					"hi": hi,
					"lo": lo,
					"diff0": diff0,
					"delta_int": delta_int,
				}
			)
	return pairs


#======================================
#======================================
def select_pair_and_jitter(pairs: list[dict]) -> dict:
	"""Pick a valid pair and jitter so the difference stays integer."""
	if not pairs:
		raise ValueError("No valid pH pairs available.")
	pick = random.choice(pairs)
	delta = pick["delta_int"] - pick["diff0"]
	jitter_pairs = []
	for dh in JITTER_VALUES:
		dl = dh - delta
		dl_rounded = round(dl, 1)
		if abs(dl - dl_rounded) > 1e-6:
			continue
		if dl_rounded < -0.1 or dl_rounded > 0.1:
			continue
		jitter_pairs.append((dh, dl_rounded))
	if not jitter_pairs:
		raise ValueError("No valid pH jitters available.")
	dh, dl = random.choice(jitter_pairs)
	high_pH = pick["hi"]["pH"] + dh
	low_pH = pick["lo"]["pH"] + dl
	pick["high_pH_text"] = f"{high_pH:.1f}"
	pick["low_pH_text"] = f"{low_pH:.1f}"
	return pick


#======================================
#======================================
def build_question_text(pick: dict) -> str:
	"""Build the HTML question text for the selected pair."""
	high_name_html = format_item_name(pick["hi"]["name"], pick["hi"]["color"])
	low_name_html = format_item_name(pick["lo"]["name"], pick["lo"]["color"])
	high_ph_html = format_ph_value(pick["high_pH_text"])
	low_ph_html = format_ph_value(pick["low_pH_text"])
	delta_int = pick["delta_int"]
	return (
		f"<p>The pH of the {high_name_html} is {high_ph_html}, while the "
		f"{low_name_html} is pH {low_ph_html}. This is a difference of {delta_int} "
		"pH units.</p>"
		f"<p>The {low_name_html} has:</p>"
	)


#======================================
#======================================
def generate_choices(pick: dict) -> tuple[list[str], str]:
	"""Return shuffled choices and the correct answer text."""
	delta_int = pick["delta_int"]
	high_name_html = format_item_name(pick["hi"]["name"], pick["hi"]["color"])
	factor_text = power_of_ten_words(delta_int)
	correct_text = f"{factor_text} times higher [H+] than the {high_name_html}."
	wrong_high = f"{delta_int} times higher [H+] than the {high_name_html}."
	wrong_low = f"{delta_int} times lower [H+] than the {high_name_html}."
	wrong_factor_low = f"{factor_text} times lower [H+] than the {high_name_html}."
	choices = [wrong_high, correct_text, wrong_low, wrong_factor_low]
	random.shuffle(choices)
	return choices, correct_text


#======================================
#======================================
def write_question(question_num: int, args) -> str:
	"""Create a complete formatted question."""
	assert question_num > 0, "Question number must be positive"

	pairs = build_pairs(CONTEXTS)
	pick = select_pair_and_jitter(pairs)
	question_text = build_question_text(pick)
	choices_list, answer_text = generate_choices(pick)
	return bptools.formatBB_MC_Question(question_num, question_text, choices_list, answer_text)


#======================================
#======================================
def main() -> None:
	parser = bptools.make_arg_parser(description="Generate pH vs [H+] ratio questions.")
	args = parser.parse_args()

	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)


#======================================
#======================================
if __name__ == "__main__":
	main()
