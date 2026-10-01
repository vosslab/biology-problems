#!/usr/bin/env python3

import random

import bptools


SCENARIOS = [
	{
		"id": "one_sample_baby_weights",
		"title": "One-sample mean test (baby weights)",
		"family": "one_mean",
		"param_html": "&mu;<sub>hospital</sub>",
		"param_text": "mu_hospital",
		"measure_text": "birth weight",
		"subject_text": "hospital",
		"null_value_html": "7.5",
		"unit_html": "lbs",
		"context_html": (
			"<p>Joe's Hospital of Fried Foods claims their newborns are heavier than "
			"the national average.</p>"
			"<p>The national average birth weight is "
			"<span style='font-family: monospace;'>7.5 lbs</span>.</p>"
		),
	},
	{
		"id": "two_sample_diversity_2014_2024",
		"title": "Two-sample mean test (Shannon diversity 2014 vs 2024)",
		"family": "two_mean",
		"param1_html": "&mu;<sub>2014</sub>",
		"param2_html": "&mu;<sub>2024</sub>",
		"param1_text": "mu_2014",
		"param2_text": "mu_2024",
		"measure_text": "Shannon Diversity Index",
		"context_html": (
			"<p>Ecologists compare Shannon Diversity Index measurements taken at the same "
			"set of sites in 2014 and 2024.</p>"
		),
	},
	{
		"id": "two_sample_variance_2014_2024",
		"title": "Two-sample variance test (F test)",
		"family": "two_variance",
		"param1_html": "&sigma;<sub>2014</sub><sup>2</sup>",
		"param2_html": "&sigma;<sub>2024</sub><sup>2</sup>",
		"param1_text": "sigma^2_2014",
		"param2_text": "sigma^2_2024",
		"measure_text": "Shannon Diversity Index",
		"context_html": (
			"<p>Ecologists want to know whether the <b>variability</b> of Shannon Diversity "
			"Index measurements changed between 2014 and 2024.</p>"
		),
	},
	{
		"id": "anova_shannon_by_year",
		"title": "ANOVA (five years of Shannon diversity)",
		"family": "anova",
		"group_names": ["1994", "2004", "2009", "2014", "2024"],
		"measure_text": "Shannon Diversity Index",
		"context_html": (
			"<p>Ecologists measure Shannon Diversity Index at the same set of sites across "
			"five years (1994, 2004, 2009, 2014, 2024).</p>"
		),
	},
]


ERROR_CHOICES = [
	"They swapped the null and alternative hypotheses.",
	"They wrote the null hypothesis as an inequality (the null should include equality).",
	"They used sample statistics (like x&#772; or s<sup>2</sup>) instead of population parameters.",
	"Nothing is wrong; the hypotheses are stated correctly.",
]


#===========================
def _mk_param(param_html: str, param_text: str | None) -> str:
	if param_text is None:
		return param_html
	param_text_html = bptools.html_monospace(param_text, use_nbsp=False)
	return f"{param_html} ({param_text_html})"


#===========================
def _split_relation(expr: str) -> tuple[str, str, str] | None:
	for op in ("&ne;", "&ge;", "&le;", "&gt;", "&lt;", "="):
		sep = f" {op} " if op != "=" else " = "
		if sep not in expr:
			continue
		left, right = expr.split(sep, 1)
		return left.strip(), op, right.strip()
	return None


#===========================
def _find_year(text: str) -> str | None:
	for year in ("1994", "2004", "2009", "2014", "2024"):
		if year in text:
			return year
	return None


#===========================
def _hypothesis_in_words(scenario: dict, hypothesis_html: str) -> str:
	family = scenario["family"]
	measure = scenario.get("measure_text", "value")
	parts = _split_relation(hypothesis_html)
	if parts is None:
		return hypothesis_html
	left, op, right = parts

	rel_map = {
		"=": "equals",
		"&ne;": "is different from",
		"&gt;": "is greater than",
		"&lt;": "is less than",
		"&ge;": "is greater than or equal to",
		"&le;": "is less than or equal to",
	}
	rel = rel_map.get(op)
	if rel is None:
		return hypothesis_html

	if family == "one_mean":
		unit = scenario.get("unit_html", "")
		subject = scenario.get("subject_text", "population")
		value = right
		if len(unit) > 0:
			value_html = bptools.html_monospace(f"{value} {unit}", use_nbsp=False)
		else:
			value_html = bptools.html_monospace(value, use_nbsp=False)
		return f"The {subject} mean {measure} {rel} {value_html}."

	if family in ("two_mean", "two_variance"):
		stat_text = "mean" if family == "two_mean" else "variance"
		year_left = _find_year(left)
		year_right = _find_year(right)

		if op in ("=", "&ne;"):
			year_set = {y for y in (year_left, year_right) if y is not None}
			if len(year_set) == 2:
				year_text = " and ".join(sorted(year_set))
			else:
				year_text = "the two groups"
			result_text = "equal" if op == "=" else "different"
			return f"The {stat_text} {measure} values in {year_text} are {result_text}."

		if year_left is None:
			year_left = "the first group"
		if year_right is None:
			year_right = "the second group"
		return f"The {stat_text} {measure} value in {year_left} {rel} the value in {year_right}."

	return hypothesis_html


#===========================
def _pick_tail(family: str) -> str:
	if family == "anova":
		return "two"
	return random.choice(("greater", "less", "two"))


#===========================
def _hypotheses_for_scenario(scenario: dict, tail: str) -> tuple[str, str]:
	family = scenario["family"]
	if family == "one_mean":
		param = _mk_param(scenario["param_html"], scenario.get("param_text"))
		v0 = scenario["null_value_html"]
		h0 = f"{param} = {v0}"
		if tail == "greater":
			ha = f"{param} &gt; {v0}"
		elif tail == "less":
			ha = f"{param} &lt; {v0}"
		else:
			ha = f"{param} &ne; {v0}"
		return h0, ha

	if family in ("two_mean", "two_variance"):
		p1 = _mk_param(scenario["param1_html"], scenario.get("param1_text"))
		p2 = _mk_param(scenario["param2_html"], scenario.get("param2_text"))
		h0 = f"{p1} = {p2}"
		if tail == "greater":
			ha = f"{p2} &gt; {p1}"
		elif tail == "less":
			ha = f"{p2} &lt; {p1}"
		else:
			ha = f"{p1} &ne; {p2}"
		return h0, ha

	if family == "anova":
		h0 = "All group means are equal."
		ha = "At least one group mean is different."
		return h0, ha

	raise ValueError(f"Unknown family: {family}")


#===========================
def _apply_error_type(
	scenario: dict,
	tail: str,
	error_type: str
) -> tuple[str, str, int]:
	h0, ha = _hypotheses_for_scenario(scenario, tail)
	family = scenario["family"]

	if error_type == "swap":
		return ha, h0, 0

	if error_type == "null_inequality":
		if family == "anova":
			return "At least one group mean is different.", "All group means are equal.", 1

		if family == "one_mean":
			param = _mk_param(scenario["param_html"], scenario.get("param_text"))
			v0 = scenario["null_value_html"]
			if tail == "greater":
				return f"{param} &gt; {v0}", f"{param} &le; {v0}", 1
			if tail == "less":
				return f"{param} &lt; {v0}", f"{param} &ge; {v0}", 1
			return f"{param} &ne; {v0}", f"{param} = {v0}", 1

		p1 = _mk_param(scenario["param1_html"], scenario.get("param1_text"))
		p2 = _mk_param(scenario["param2_html"], scenario.get("param2_text"))
		if tail == "greater":
			return f"{p2} &gt; {p1}", f"{p2} &le; {p1}", 1
		if tail == "less":
			return f"{p2} &lt; {p1}", f"{p2} &ge; {p1}", 1
		return f"{p1} &ne; {p2}", f"{p1} = {p2}", 1

	if error_type == "sample_stats":
		if family == "anova":
			return "All sample means are equal.", "At least one sample mean is different.", 2

		if family == "one_mean":
			v0 = scenario["null_value_html"]
			h0s = f"x&#772;<sub>hospital</sub> ({bptools.html_monospace('xbar_hospital', use_nbsp=False)}) = {v0}"
			if tail == "greater":
				has = f"x&#772;<sub>hospital</sub> ({bptools.html_monospace('xbar_hospital', use_nbsp=False)}) &gt; {v0}"
			elif tail == "less":
				has = f"x&#772;<sub>hospital</sub> ({bptools.html_monospace('xbar_hospital', use_nbsp=False)}) &lt; {v0}"
			else:
				has = f"x&#772;<sub>hospital</sub> ({bptools.html_monospace('xbar_hospital', use_nbsp=False)}) &ne; {v0}"
			return h0s, has, 2

		if family == "two_mean":
			xbar_2014 = bptools.html_monospace("xbar_2014", use_nbsp=False)
			xbar_2024 = bptools.html_monospace("xbar_2024", use_nbsp=False)
			h0s = f"x&#772;<sub>2014</sub> ({xbar_2014}) = x&#772;<sub>2024</sub> ({xbar_2024})"
			if tail == "greater":
				has = f"x&#772;<sub>2024</sub> ({xbar_2024}) &gt; x&#772;<sub>2014</sub> ({xbar_2014})"
			elif tail == "less":
				has = f"x&#772;<sub>2024</sub> ({xbar_2024}) &lt; x&#772;<sub>2014</sub> ({xbar_2014})"
			else:
				has = f"x&#772;<sub>2014</sub> ({xbar_2014}) &ne; x&#772;<sub>2024</sub> ({xbar_2024})"
			return h0s, has, 2

		s2_2014 = bptools.html_monospace("s2_2014", use_nbsp=False)
		s2_2024 = bptools.html_monospace("s2_2024", use_nbsp=False)
		h0s = f"s<sub>2014</sub><sup>2</sup> ({s2_2014}) = s<sub>2024</sub><sup>2</sup> ({s2_2024})"
		if tail == "greater":
			has = f"s<sub>2024</sub><sup>2</sup> ({s2_2024}) &gt; s<sub>2014</sub><sup>2</sup> ({s2_2014})"
		elif tail == "less":
			has = f"s<sub>2024</sub><sup>2</sup> ({s2_2024}) &lt; s<sub>2014</sub><sup>2</sup> ({s2_2014})"
		else:
			has = f"s<sub>2014</sub><sup>2</sup> ({s2_2014}) &ne; s<sub>2024</sub><sup>2</sup> ({s2_2024})"
		return h0s, has, 2

	if error_type == "correct":
		return h0, ha, 3

	raise ValueError(f"Unknown error_type: {error_type}")


#===========================
def make_question(error_type: str, scenario_id: str | None = None) -> tuple[str, list[str], str]:
	if scenario_id is None:
		scenario = random.choice(SCENARIOS)
	else:
		matches = [s for s in SCENARIOS if s["id"] == scenario_id]
		if len(matches) != 1:
			raise ValueError(f"Unknown scenario_id: {scenario_id}")
		scenario = matches[0]

	tail = _pick_tail(scenario["family"])

	if scenario["family"] == "one_mean":
		v0 = scenario["null_value_html"]
		unit = scenario["unit_html"]
		if tail == "greater":
			research = f"Is the mean higher than {v0} {unit}?"
		elif tail == "less":
			research = f"Is the mean lower than {v0} {unit}?"
		else:
			research = f"Is the mean different from {v0} {unit}?"
	elif scenario["family"] == "anova":
		research = "Are any of the group means different?"
	else:
		if tail == "greater":
			research = "Is the 2024 value larger than the 2014 value?"
		elif tail == "less":
			research = "Is the 2024 value smaller than the 2014 value?"
		else:
			research = "Are the 2014 and 2024 values different?"

	lab_h0, lab_ha, answer_index = _apply_error_type(scenario, tail, error_type)

	question = ""
	question += "<p>Your lab partner is trying again (eye roll).</p>"
	question += f"<p><b>Scenario:</b> {scenario['title']}</p>"
	question += scenario["context_html"]
	question += f"<p><b>Research question:</b> {research}</p>"
	question += "<hr/> "
	question += "<p>They wrote the hypotheses below:</p>"
	question += "<p>"
	question += f"<b>H<sub>0</sub></b>: {lab_h0}"
	question += f"<br/><span style='font-size: 90%;'>In words: {_hypothesis_in_words(scenario, lab_h0)}</span>"
	question += f"<br/><b>H<sub>A</sub></b>: {lab_ha}"
	question += f"<br/><span style='font-size: 90%;'>In words: {_hypothesis_in_words(scenario, lab_ha)}</span>"
	question += "</p>"
	question += "<p><b>What is the main problem with their hypotheses?</b></p>"

	choices_list = list(ERROR_CHOICES)
	answer_text = choices_list[answer_index]
	random.shuffle(choices_list)
	return question, choices_list, answer_text


#===========================
def write_question(N: int, args) -> str:
	if args.error_type == "random":
		error_type = random.choice(("swap", "null_inequality", "sample_stats", "correct"))
	else:
		error_type = args.error_type

	question_text, choices_list, answer_text = make_question(error_type, args.scenario)
	return bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)


#===========================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Biostatistics hypotheses (dumb lab partner).")
	parser.add_argument(
		"-e", "--error-type", dest="error_type", type=str,
		choices=("random", "swap", "null_inequality", "sample_stats", "correct"),
		help="Force a specific error type (default: random mix).",
		default="random",
	)
	parser.add_argument(
		"-s", "--scenario", dest="scenario", type=str,
		help="Optional fixed scenario id.",
		default=None,
	)
	args = parser.parse_args()
	return args


#===========================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile("hypotheses_partner")
	if args.error_type != "random":
		outfile = bptools.make_outfile("hypotheses_partner", args.error_type)
	if args.scenario is not None:
		outfile = bptools.make_outfile("hypotheses_partner", args.error_type, args.scenario)
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()
