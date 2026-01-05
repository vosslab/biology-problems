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
def _set_relation(expr: str, new_op: str) -> str:
	parts = _split_relation(expr)
	if parts is None:
		return expr
	left, _, right = parts
	sep = f" {new_op} " if new_op != "=" else " = "
	return f"{left}{sep}{right}"


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
def _mk_pair(scenario: dict, h0: str, ha: str) -> str:
	h0_words = _hypothesis_in_words(scenario, h0)
	ha_words = _hypothesis_in_words(scenario, ha)
	return (
		"<p>"
		f"<b>H<sub>0</sub></b>: {h0}"
		f"<br/><span style='font-size: 90%;'>In words: {h0_words}</span>"
		f"<br/><b>H<sub>A</sub></b>: {ha}"
		f"<br/><span style='font-size: 90%;'>In words: {ha_words}</span>"
		"</p>"
	)


#===========================
def _mk_statement(scenario: dict, label: str, text: str) -> str:
	words = _hypothesis_in_words(scenario, text)
	return (
		"<p>"
		f"<b>{label}</b>: {text}"
		f"<br/><span style='font-size: 90%;'>In words: {words}</span>"
		"</p>"
	)


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
		years = scenario["group_names"]
		h0 = "All group means are equal."
		ha = "At least one group mean is different."
		_ = years
		return h0, ha

	raise ValueError(f"Unknown family: {family}")


#===========================
def _wrong_pair_choices(scenario: dict, tail: str) -> list[str]:
	h0, ha = _hypotheses_for_scenario(scenario, tail)
	correct = _mk_pair(scenario, h0, ha)

	family = scenario["family"]
	choices = [correct]

	# 1) swapped
	choices.append(_mk_pair(scenario, ha, h0))

	# 2) null written with an inequality (very common student mistake)
	if family == "anova":
		choices.append(_mk_pair(scenario, "At least one group mean is different.", "All group means are equal."))
	else:
		if tail == "greater":
			choices.append(_mk_pair(scenario, _set_relation(h0, "&gt;"), ha))
		elif tail == "less":
			choices.append(_mk_pair(scenario, _set_relation(h0, "&lt;"), ha))
		else:
			choices.append(_mk_pair(scenario, _set_relation(h0, "&ne;"), ha))

	# 3) wrong parameter or wrong baseline
	if family == "one_mean":
		param = _mk_param(scenario["param_html"], scenario.get("param_text"))
		v0 = scenario["null_value_html"]
		wrong_v = "8.0" if v0 == "7.5" else "7.5"
		choices.append(_mk_pair(scenario, f"{param} = {wrong_v}", ha))
	elif family in ("two_mean", "two_variance"):
		p1 = _mk_param(scenario["param1_html"], scenario.get("param1_text"))
		p2 = _mk_param(scenario["param2_html"], scenario.get("param2_text"))
		choices.append(_mk_pair(scenario, f"{p1} &lt; {p2}", f"{p1} &ge; {p2}"))
	else:
		choices.append(_mk_pair(scenario, "The sample means are all equal.", "The sample means are not all equal."))

	return choices, correct


#===========================
def _wrong_single_choices(scenario: dict, tail: str, kind: str) -> tuple[list[str], str]:
	h0, ha = _hypotheses_for_scenario(scenario, tail)
	if kind == "null":
		correct = _mk_statement(scenario, "H<sub>0</sub>", h0)
		family = scenario["family"]
		choices = [correct, _mk_statement(scenario, "H<sub>A</sub>", ha)]
		if family == "anova":
			choices.append(_mk_statement(scenario, "H<sub>0</sub>", "At least one group mean is different."))
			choices.append(_mk_statement(scenario, "H<sub>0</sub>", "The sample means are all equal."))
		elif family == "one_mean":
			param = _mk_param(scenario["param_html"], scenario.get("param_text"))
			v0 = scenario["null_value_html"]
			choices.append(_mk_statement(scenario, "H<sub>0</sub>", f"{param} &gt; {v0}"))
			choices.append(_mk_statement(scenario, "H<sub>0</sub>", "The sample mean equals the population mean."))
		else:
			p1 = _mk_param(scenario["param1_html"], scenario.get("param1_text"))
			p2 = _mk_param(scenario["param2_html"], scenario.get("param2_text"))
			choices.append(_mk_statement(scenario, "H<sub>0</sub>", f"{p1} &ne; {p2}"))
			choices.append(_mk_statement(scenario, "H<sub>0</sub>", "The sample means are equal."))
		return choices, correct

	if kind == "alt":
		correct = _mk_statement(scenario, "H<sub>A</sub>", ha)
		family = scenario["family"]
		choices = [correct, _mk_statement(scenario, "H<sub>0</sub>", h0)]
		if family == "anova":
			choices.append(_mk_statement(scenario, "H<sub>A</sub>", "All group means are equal."))
			choices.append(_mk_statement(scenario, "H<sub>A</sub>", "The sample means are all equal."))
		elif family == "one_mean":
			param = _mk_param(scenario["param_html"], scenario.get("param_text"))
			v0 = scenario["null_value_html"]
			choices.append(_mk_statement(scenario, "H<sub>A</sub>", f"{param} = {v0}"))
			choices.append(_mk_statement(scenario, "H<sub>A</sub>", "The sample mean is not equal to the population mean."))
		else:
			p1 = _mk_param(scenario["param1_html"], scenario.get("param1_text"))
			p2 = _mk_param(scenario["param2_html"], scenario.get("param2_text"))
			choices.append(_mk_statement(scenario, "H<sub>A</sub>", f"{p1} = {p2}"))
			choices.append(_mk_statement(scenario, "H<sub>A</sub>", "The sample means are not equal."))
		return choices, correct

	raise ValueError(f"Unknown kind: {kind}")


#===========================
def make_question(kind: str, scenario_id: str | None = None) -> tuple[str, list[str], str]:
	if scenario_id is None:
		scenario = random.choice(SCENARIOS)
	else:
		matches = [s for s in SCENARIOS if s["id"] == scenario_id]
		if len(matches) != 1:
			raise ValueError(f"Unknown scenario_id: {scenario_id}")
		scenario = matches[0]

	tail = _pick_tail(scenario["family"])

	question = ""
	question += f"<p><b>Hypotheses practice: {scenario['title']}</b></p>"
	question += scenario["context_html"]
	question += "<p>Your task is to correctly identify the null hypothesis (H<sub>0</sub>) "
	question += "and the alternative hypothesis (H<sub>A</sub>).</p>"
	question += "<hr/> "

	if scenario["family"] == "one_mean":
		v0 = scenario["null_value_html"]
		unit = scenario["unit_html"]
		if tail == "greater":
			question += f"<p>Research question: Is the mean higher than {v0} {unit}?</p>"
		elif tail == "less":
			question += f"<p>Research question: Is the mean lower than {v0} {unit}?</p>"
		else:
			question += f"<p>Research question: Is the mean different from {v0} {unit}?</p>"
	elif scenario["family"] == "anova":
		question += "<p>Research question: Are any of the group means different?</p>"
	else:
		if tail == "greater":
			question += "<p>Research question: Is the 2024 value larger than the 2014 value?</p>"
		elif tail == "less":
			question += "<p>Research question: Is the 2024 value smaller than the 2014 value?</p>"
		else:
			question += "<p>Research question: Are the 2014 and 2024 values different?</p>"

	if kind == "pair":
		question += "<p>Which option correctly states H<sub>0</sub> and H<sub>A</sub>?</p>"
		choices_list, answer_text = _wrong_pair_choices(scenario, tail)
	else:
		if kind == "null":
			question += "<p>Which statement is the <b>null hypothesis</b> (H<sub>0</sub>)?</p>"
		else:
			question += "<p>Which statement is the <b>alternative hypothesis</b> (H<sub>A</sub>)?</p>"
		choices_list, answer_text = _wrong_single_choices(scenario, tail, kind)

	random.shuffle(choices_list)
	return question, choices_list, answer_text


#===========================
def write_question(N: int, args) -> str:
	question_text, choices_list, answer_text = make_question(args.kind, args.scenario)
	return bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)


#===========================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Biostatistics hypothesis statements (H0 vs HA).")
	parser.add_argument(
		"-k", "--kind", dest="kind", type=str,
		choices=("pair", "null", "alt"),
		help="Question kind: choose H0/HA pair, H0 only, or HA only.",
		default="pair",
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
	outfile = bptools.make_outfile(None, args.kind)
	if args.scenario is not None:
		outfile = bptools.make_outfile(None, args.kind, args.scenario)
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()
