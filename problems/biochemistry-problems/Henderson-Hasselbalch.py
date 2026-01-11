#!/usr/bin/env python3

import math
import os
import random
import sys

import bptools

#===========================================================
#===========================================================
_BIOCHEM_DIR = os.path.abspath(os.path.dirname(__file__))
_BUFFERS_DIR = os.path.join(_BIOCHEM_DIR, "buffers")
if _BUFFERS_DIR not in sys.path:
	sys.path.insert(0, _BUFFERS_DIR)

import bufferslib

_PKW = 14.00

_WEAK_BASE_BUFFER_LIST = [
	{
		'base_name': 'ethylamine',
		'conj_acid_name': 'ethylammonium',
		'salt_name': 'ethylammonium chloride',
		'pKb': 3.99,
	},
	{
		'base_name': 'ammonia',
		'conj_acid_name': 'ammonium',
		'salt_name': 'ammonium chloride',
		'pKb': 14.00 - float(bufferslib.monoprotic['ammonia']['pKa_list'][0]),
	},
]

#===========================================================
#===========================================================
def get_Henderson_Hasselbalch_equation(
	pH=None, pKa=None, HA=None, A_=None,
	words=False, plus=None, wrong=False):

	open_bracket = "<mo stretchy='true'>[</mo>"
	close_bracket = "<mo stretchy='true'>]</mo>"
	# Define MathML representation for the weak acid (HA)
	if HA is None:
		# Symbolic HA if no value is provided
		if words is True:
			ha_conj_base = open_bracket + "<mi>Acid</mi>" + close_bracket
		else:
			ha_conj_base = open_bracket + "<mi>HA</mi>" + close_bracket
	else:
		# Numeric HA value if provided
		ha_conj_base = open_bracket + f"<mn>{HA:.2f}</mn>" + close_bracket
	# Define MathML representation for the conjugate base (A⁻)
	if A_ is None:
		# Symbolic A⁻ if no value is provided
		a_mathml = "<msup><mi mathvariant='normal'>A</mi><mo>&#8211;</mo></msup>"
		if words is True:
			a__conj_acid = open_bracket + "<mi>Base</mi>" + close_bracket
		else:
			a__conj_acid = open_bracket + a_mathml + close_bracket
	else:
		# Numeric A⁻ value if provided
		a__conj_acid = open_bracket + f"<mn>{A_:.2f}</mn>" + close_bracket
	# Determine the correct or intentionally incorrect structure of the equation
	# Set whether [HA] appears in the numerator
	if wrong is False:
		# Correct format: [A⁻] / [HA]
		ha_on_top = False
	else:
		# Incorrect format: [HA] / [A⁻]
		ha_on_top = True
	# Initialize the MathML string for the equation
	equation_text = ""
	equation_text += "<p><math xmlns='http://www.w3.org/1998/Math/MathML'>"
	# Add pH to the equation
	if pH is None:
		# Symbolic pH if no value is provided
		equation_text += "<mi>pH</mi><mo>&#8201;</mo><mo>=</mo><mo>&#8201;</mo>"
	else:
		# Numeric pH value if provided
		equation_text += f"<mn>{pH:.2f}</mn><mo>&#8201;</mo><mo>=</mo><mo>&#8201;</mo>"
	# Add pKa to the equation
	if pKa is None:
		# Symbolic pKa if no value is provided
		equation_text += "<msub><mi>pK</mi><mi>a</mi></msub>"
	else:
		# Numeric pKa value if provided
		equation_text += f"<mn>{pKa:.2f}</mn>"
	# Add the plus or minus sign based on the 'plus' argument
	if plus == "-" or plus == "minus":
		# Add minus sign and flip numerator and denominator
		equation_text += "<mo>&#160;</mo><mo>&ndash;</mo><mo>&#8201;</mo>"
		ha_on_top = not ha_on_top
	else:
		# Add plus sign
		equation_text += "<mo>&#160;</mo><mo>+</mo><mo>&#8201;</mo>"
	# Add the log function and start the fraction
	equation_text += "<msub><mo>log</mo><mn>10</mn></msub>"
	# Begin the numerator of the fraction
	equation_text += "<mfenced><mfrac><mrow>"
	# Insert the numerator based on the 'ha_on_top' flag
	if ha_on_top is False:
		# A⁻ goes on top in the correct format
		equation_text += a__conj_acid
	else:
		# HA goes on top in the incorrect format
		equation_text += ha_conj_base
	# Close the numerator
	equation_text += "</mrow><mrow>"
	# Insert the denominator based on the 'ha_on_top' flag
	if ha_on_top is False:
		# HA goes on bottom in the correct format
		equation_text += ha_conj_base
	else:
		# A⁻ goes on bottom in the incorrect format
		equation_text += a__conj_acid
	# Close the denominator and log function
	equation_text += "</mrow></mfrac></mfenced>"
	# Complete the MathML structure
	equation_text += "</math></p>"
	# Return the final MathML equation string
	return equation_text


#===========================================================
#===========================================================
def _safe_log10(value: float) -> float:
	if value <= 0.0:
		raise ValueError(f"log10 domain error: {value}")
	return math.log10(value)


#===========================================================
#===========================================================
def compute_pH_from_pKa_conc(pKa: float, base_conc: float, acid_conc: float) -> float:
	return float(pKa) + _safe_log10(float(base_conc) / float(acid_conc))


#===========================================================
#===========================================================
def compute_pKa_from_pH_conc(pH: float, base_conc: float, acid_conc: float) -> float:
	return float(pH) - _safe_log10(float(base_conc) / float(acid_conc))


#===========================================================
#===========================================================
def compute_ratio_from_pH_pKa(pH: float, pKa: float) -> float:
	return pow(10.0, float(pH) - float(pKa))


#===========================================================
#===========================================================
def compute_pH_from_pKb_conc(pKb: float, base_conc: float, conj_acid_conc: float) -> float:
	ratio_base_to_acid = float(base_conc) / float(conj_acid_conc)
	pKa_conj_acid = _PKW - float(pKb)
	return float(pKa_conj_acid) + _safe_log10(ratio_base_to_acid)


#===========================================================
#===========================================================
def compute_pKb_from_pH_conc(pH: float, base_conc: float, conj_acid_conc: float) -> float:
	ratio_base_to_acid = float(base_conc) / float(conj_acid_conc)
	pKa_conj_acid = float(pH) - _safe_log10(ratio_base_to_acid)
	return _PKW - float(pKa_conj_acid)


#===========================================================
#===========================================================
def compute_ratio_from_pH_pKb(pH: float, pKb: float) -> float:
	pKa_conj_acid = _PKW - float(pKb)
	return compute_ratio_from_pH_pKa(pH, pKa_conj_acid)


#===========================================================
#===========================================================
def _html_monospace(text: str) -> str:
	return f"<span style='font-family: monospace;'>{text}</span>"


#===========================================================
#===========================================================
def _format_concentration(value_molar: float) -> str:
	value_molar = float(value_molar)
	abs_value = abs(value_molar)
	if abs_value >= 1.0:
		return _html_monospace(f"{value_molar:.3f} M")
	if abs_value >= 1e-3:
		return _html_monospace(f"{value_molar * 1e3:.1f} mM")
	if abs_value >= 1e-6:
		return _html_monospace(f"{value_molar * 1e6:.1f} &mu;M")
	return _html_monospace(f"{value_molar * 1e9:.1f} nM")


#===========================================================
#===========================================================
def _format_pK(value: float, decimals: int = 2) -> str:
	return _html_monospace(f"{value:.{decimals}f}")


#===========================================================
#===========================================================
def _format_pH(value: float, decimals: int = 2) -> str:
	return _html_monospace(f"{value:.{decimals}f}")


#===========================================================
#===========================================================
def _format_ratio(value: float) -> str:
	if value < 0.01 or value > 100.0:
		return _html_monospace(f"{value:.3g}")
	return _html_monospace(f"{value:.3f}")


#===========================================================
#===========================================================
def _pick_float(low: float, high: float, decimals: int) -> float:
	value = random.random() * (high - low) + low
	return round(value, decimals)


#===========================================================
#===========================================================
def _make_mc_value_choices(
	answer_value: float,
	num_choices: int,
	decimals: int,
	min_value: float | None = None,
	max_value: float | None = None,
) -> list[float]:
	offset_pool = [-1.00, -0.60, -0.35, -0.20, 0.20, 0.35, 0.60, 1.00]
	random.shuffle(offset_pool)

	choices: list[float] = [round(float(answer_value), decimals)]
	for offset in offset_pool:
		if len(choices) >= int(num_choices):
			break
		cand = round(float(answer_value) + float(offset), decimals)
		if min_value is not None and cand < float(min_value):
			continue
		if max_value is not None and cand > float(max_value):
			continue
		if cand in choices:
			continue
		choices.append(cand)

	while len(choices) < int(num_choices):
		cand = round(float(answer_value) + _pick_float(-1.2, 1.2, decimals), decimals)
		if min_value is not None and cand < float(min_value):
			continue
		if max_value is not None and cand > float(max_value):
			continue
		if cand in choices:
			continue
		choices.append(cand)

	random.shuffle(choices)
	return choices

#===========================================================
#===========================================================
# This function creates and formats a complete question for output.
def write_equation_question(N: int) -> str:
	"""
	Creates a complete formatted question for output.

	Args:
		N (int): The question number, used for labeling the question.
		num_choices (int): The number of answer choices to include.

	Returns:
		str: A formatted question string containing the question text,
		answer choices, and the correct answer.
	"""
	# Generate the main question text
	question_text = "<p>Which one of the following equations is the correct form of the "
	question_text += "Henderson-Hasselbalch equation?</p>"

	words_bool = (N%2 == 0)
	if (N // 2) % 2 == 0:
		answer_html = get_Henderson_Hasselbalch_equation(
			plus='plus', wrong=False, words=words_bool)
	else:
		answer_html = get_Henderson_Hasselbalch_equation(
			plus='minus', wrong=False, words=words_bool)
	if (N // 4) % 2 == 0:
		wrong_html = get_Henderson_Hasselbalch_equation(
			plus='plus', wrong=True, words=words_bool)
	else:
		wrong_html = get_Henderson_Hasselbalch_equation(
			plus='minus', wrong=True, words=words_bool)

	# Generate answer choices and the correct answer
	if (N // 8) % 2 == 0:
		choices_list = [answer_html, wrong_html]
	else:
		choices_list = [wrong_html, answer_html]

	# Format the question using a helper function from the bptools module
	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_html)

	# Return the formatted question string
	return complete_question

#===========================================================
#===========================================================
def _pick_monoprotic_acid_buffer():
	acid_buffer_list = []
	for buffer_dict in bufferslib.monoprotic.values():
		# Exclude ammonia/ammonium here: they are typically presented as a weak base buffer
		# (ammonia + ammonium chloride), not "sodium ammonia".
		if buffer_dict.get('base_name') == 'ammonia':
			continue
		acid_buffer_list.append(buffer_dict)
	buffer_dict = bufferslib.expand_buffer_dict(random.choice(acid_buffer_list))
	pKa = float(buffer_dict['pKa_list'][0])
	return buffer_dict, pKa


#===========================================================
#===========================================================
def _write_pH_question(N: int, args) -> str:
	ask_base_buffer = (random.random() < 0.35)
	equation_html = get_Henderson_Hasselbalch_equation(words=True, plus='plus', wrong=False)

	if ask_base_buffer is True:
		base_buffer = random.choice(_WEAK_BASE_BUFFER_LIST)
		pKb = float(base_buffer['pKb'])
		base_conc = _pick_float(0.0200, 0.1200, 4)
		conj_acid_conc = _pick_float(0.0200, 0.1200, 4)
		pH_value = compute_pH_from_pKb_conc(pKb, base_conc, conj_acid_conc)

		question_text = ""
		question_text += "<p><b>Calculate the pH of the buffer solution.</b></p>"
		question_text += (f"<p>The solution contains {_format_concentration(base_conc)} of "
			f"<strong>{base_buffer['base_name']}</strong> and {_format_concentration(conj_acid_conc)} of "
			f"<strong>{base_buffer['salt_name']}</strong>.</p>")
		question_text += f"<p>(pK<sub>b</sub> of {base_buffer['base_name']} = {_format_pK(pKb)})</p>"
		question_text += "<p>Hint: pK<sub>a</sub> + pK<sub>b</sub> = 14.00 for a conjugate acid-base pair.</p>"
		question_text += "<p>Henderson-Hasselbalch form:</p>"
		question_text += equation_html

		answer_value = round(float(pH_value), 2)
		if args.question_format == 'mc':
			choices = _make_mc_value_choices(answer_value, args.num_choices, 2, 0.00, 14.00)
			choices_list = [_format_pH(v, 2) for v in choices]
			answer_text = _format_pH(answer_value, 2)
			return bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
		tolerance = 0.05
		return bptools.formatBB_NUM_Question(N, question_text, answer_value, tolerance)

	buffer_dict, pKa = _pick_monoprotic_acid_buffer()
	acid_conc = _pick_float(0.050, 0.700, 3)
	base_conc = _pick_float(0.050, 0.700, 3)
	pH_value = compute_pH_from_pKa_conc(pKa, base_conc, acid_conc)

	use_mass_volume = (
		buffer_dict['acid_name'] == 'acetic acid'
		and buffer_dict['base_name'] == 'acetate'
		and random.random() < 0.40
	)
	if use_mass_volume is True:
		# Example-style: masses and a final volume.
		m_acid_g = _pick_float(6.0, 14.0, 1)
		m_salt_g = _pick_float(6.0, 14.0, 1)
		vol_ml = _pick_float(100.0, 250.0, 1)
		mm_acid = 60.05
		mm_salt = 82.03
		moles_acid = float(m_acid_g) / mm_acid
		moles_base = float(m_salt_g) / mm_salt
		vol_l = float(vol_ml) / 1000.0
		acid_conc = float(moles_acid) / vol_l
		base_conc = float(moles_base) / vol_l
		pH_value = compute_pH_from_pKa_conc(pKa, base_conc, acid_conc)

		question_text = ""
		question_text += "<p><b>Use the Henderson-Hasselbalch equation to calculate the pH.</b></p>"
		question_text += (f"<p>A solution contains {_html_monospace(f'{m_acid_g:.1f} g')} of "
			f"<strong>HC<sub>2</sub>H<sub>3</sub>O<sub>2</sub></strong> and {_html_monospace(f'{m_salt_g:.1f} g')} of "
			f"<strong>NaC<sub>2</sub>H<sub>3</sub>O<sub>2</sub></strong> in {_html_monospace(f'{vol_ml:.1f} mL')} of solution.</p>")
		question_text += f"<p>(pK<sub>a</sub> of {buffer_dict['acid_name']} = {_format_pK(pKa)})</p>"
		question_text += "<p>Molar masses: HC<sub>2</sub>H<sub>3</sub>O<sub>2</sub> = 60.05 g/mol; NaC<sub>2</sub>H<sub>3</sub>O<sub>2</sub> = 82.03 g/mol.</p>"
		question_text += "<p>Henderson-Hasselbalch equation:</p>"
		question_text += equation_html
	else:
		question_text = ""
		question_text += "<p><b>Calculate the pH of the buffer solution.</b></p>"
		question_text += (f"<p>The solution contains {_format_concentration(acid_conc)} of "
			f"<strong>{buffer_dict['acid_name']}</strong> and {_format_concentration(base_conc)} of "
			f"<strong>sodium {buffer_dict['base_name']}</strong>.</p>")
		question_text += f"<p>(pK<sub>a</sub> of {buffer_dict['acid_name']} = {_format_pK(pKa)})</p>"
		question_text += "<p>Henderson-Hasselbalch equation:</p>"
		question_text += equation_html

	answer_value = round(float(pH_value), 2)
	if args.question_format == 'mc':
		choices = _make_mc_value_choices(answer_value, args.num_choices, 2, 0.00, 14.00)
		choices_list = [_format_pH(v, 2) for v in choices]
		answer_text = _format_pH(answer_value, 2)
		return bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
	tolerance = 0.05
	return bptools.formatBB_NUM_Question(N, question_text, answer_value, tolerance)


#===========================================================
#===========================================================
def _write_pK_question(N: int, args) -> str:
	ask_base_buffer = (random.random() < 0.35)
	equation_html = get_Henderson_Hasselbalch_equation(words=True, plus='plus', wrong=False)

	if ask_base_buffer is True:
		base_buffer = random.choice(_WEAK_BASE_BUFFER_LIST)
		pKb = float(base_buffer['pKb'])
		base_conc = _pick_float(0.0200, 0.1200, 4)
		conj_acid_conc = _pick_float(0.0200, 0.1200, 4)
		pH_value = compute_pH_from_pKb_conc(pKb, base_conc, conj_acid_conc)

		question_text = ""
		question_text += "<p><b>Calculate pK<sub>b</sub> for the weak base.</b></p>"
		question_text += (f"<p>The solution contains {_format_concentration(base_conc)} of "
			f"<strong>{base_buffer['base_name']}</strong> and {_format_concentration(conj_acid_conc)} of "
			f"<strong>{base_buffer['salt_name']}</strong>.</p>")
		question_text += f"<p>The measured pH of the solution is {_format_pH(pH_value, 2)}.</p>"
		question_text += "<p>Hint: pK<sub>a</sub> + pK<sub>b</sub> = 14.00 for a conjugate acid-base pair.</p>"
		question_text += "<p>Henderson-Hasselbalch form:</p>"
		question_text += equation_html

		answer_value = round(float(pKb), 2)
		if args.question_format == 'mc':
			choices = _make_mc_value_choices(answer_value, args.num_choices, 2, 0.00, 14.00)
			choices_list = [_format_pK(v, 2) for v in choices]
			answer_text = _format_pK(answer_value, 2)
			return bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
		tolerance = 0.05
		return bptools.formatBB_NUM_Question(N, question_text, answer_value, tolerance)

	buffer_dict, pKa = _pick_monoprotic_acid_buffer()
	acid_conc = _pick_float(0.050, 0.700, 3)
	base_conc = _pick_float(0.050, 0.700, 3)
	pH_value = compute_pH_from_pKa_conc(pKa, base_conc, acid_conc)

	question_text = ""
	question_text += "<p><b>Calculate pK<sub>a</sub> for the weak acid.</b></p>"
	question_text += (f"<p>The solution contains {_format_concentration(acid_conc)} of "
		f"<strong>{buffer_dict['acid_name']}</strong> and {_format_concentration(base_conc)} of "
		f"<strong>sodium {buffer_dict['base_name']}</strong>.</p>")
	question_text += f"<p>The measured pH of the solution is {_format_pH(pH_value, 2)}.</p>"
	question_text += "<p>Henderson-Hasselbalch equation:</p>"
	question_text += equation_html

	answer_value = round(float(pKa), 2)
	if args.question_format == 'mc':
		choices = _make_mc_value_choices(answer_value, args.num_choices, 2, 0.00, 14.00)
		choices_list = [_format_pK(v, 2) for v in choices]
		answer_text = _format_pK(answer_value, 2)
		return bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
	tolerance = 0.05
	return bptools.formatBB_NUM_Question(N, question_text, answer_value, tolerance)


#===========================================================
#===========================================================
def _write_ratio_question(N: int, args) -> str:
	ask_base_buffer = (random.random() < 0.35)

	if ask_base_buffer is True:
		base_buffer = random.choice(_WEAK_BASE_BUFFER_LIST)
		pKb = float(base_buffer['pKb'])
		pKa_conj_acid = _PKW - pKb
		pH_value = round(float(pKa_conj_acid) + _pick_float(-1.00, 1.00, 2), 2)
		ratio_value = compute_ratio_from_pH_pKb(pH_value, pKb)

		question_text = ""
		question_text += "<p><b>Calculate the ratio of weak base to conjugate acid.</b></p>"
		question_text += (f"<p>For <strong>{base_buffer['base_name']}</strong> / <strong>{base_buffer['conj_acid_name']}</strong>, "
			f"pK<sub>b</sub> = {_format_pK(pKb)} and the desired pH is {_format_pH(pH_value, 2)}.</p>")
		question_text += "<p><b>What is the ratio</b> [base] / [conjugate acid] ?</p>"
		question_text += "<p>Hint: pK<sub>a</sub> + pK<sub>b</sub> = 14.00 for a conjugate acid-base pair.</p>"

		if args.question_format == 'mc':
			answer_value = float(ratio_value)
			choice_values = [
				answer_value,
				1.0 / answer_value,
				answer_value * 10.0,
				answer_value / 10.0,
				answer_value * 2.0,
				answer_value / 2.0,
			]
			random.shuffle(choice_values)
			unique_values: list[float] = []
			for v in choice_values:
				if len(unique_values) >= int(args.num_choices):
					break
				if v <= 0.0:
					continue
				rounded = round(float(v), 3)
				if rounded in unique_values:
					continue
				unique_values.append(rounded)
			while len(unique_values) < int(args.num_choices):
				rounded = round(float(answer_value) * pow(10.0, _pick_float(-0.6, 0.6, 2)), 3)
				if rounded <= 0.0:
					continue
				if rounded in unique_values:
					continue
				unique_values.append(rounded)
			random.shuffle(unique_values)
			choices_list = [_format_ratio(v) for v in unique_values]
			answer_text = _format_ratio(answer_value)
			return bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)

		answer_value = float(ratio_value)
		tolerance = round(max(0.01, abs(answer_value) * 0.05), 3)
		return bptools.formatBB_NUM_Question(N, question_text, answer_value, tolerance)

	buffer_dict, pKa = _pick_monoprotic_acid_buffer()
	pH_value = round(float(pKa) + _pick_float(-1.00, 1.00, 2), 2)
	ratio_value = compute_ratio_from_pH_pKa(pH_value, pKa)

	question_text = ""
	question_text += "<p><b>Calculate the ratio of conjugate base to weak acid.</b></p>"
	question_text += (f"<p>For <strong>{buffer_dict['acid_name']}</strong> / <strong>{buffer_dict['base_name']}</strong>, "
		f"pK<sub>a</sub> = {_format_pK(pKa)} and the desired pH is {_format_pH(pH_value, 2)}.</p>")
	question_text += "<p><b>What is the ratio</b> [A<sup>-</sup>] / [HA] ?</p>"

	if args.question_format == 'mc':
		answer_value = float(ratio_value)
		choice_values = [
			answer_value,
			1.0 / answer_value,
			answer_value * 10.0,
			answer_value / 10.0,
			answer_value * 2.0,
			answer_value / 2.0,
		]
		random.shuffle(choice_values)
		unique_values: list[float] = []
		for v in choice_values:
			if len(unique_values) >= int(args.num_choices):
				break
			if v <= 0.0:
				continue
			rounded = round(float(v), 3)
			if rounded in unique_values:
				continue
			unique_values.append(rounded)
		while len(unique_values) < int(args.num_choices):
			rounded = round(float(answer_value) * pow(10.0, _pick_float(-0.6, 0.6, 2)), 3)
			if rounded <= 0.0:
				continue
			if rounded in unique_values:
				continue
			unique_values.append(rounded)
		random.shuffle(unique_values)
		choices_list = [_format_ratio(v) for v in unique_values]
		answer_text = _format_ratio(answer_value)
		return bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)

	answer_value = float(ratio_value)
	tolerance = round(max(0.01, abs(answer_value) * 0.05), 3)
	return bptools.formatBB_NUM_Question(N, question_text, answer_value, tolerance)


#===========================================================
#===========================================================
def write_question(N: int, args) -> str:
	if args.hh_type == 'equation':
		return write_equation_question(N)
	if args.hh_type == 'pH':
		return _write_pH_question(N, args)
	if args.hh_type == 'pKa':
		return _write_pK_question(N, args)
	if args.hh_type == 'ratio':
		return _write_ratio_question(N, args)
	raise NotImplementedError(f"question type is not implemented: {args.hh_type}")

#===========================================================
#===========================================================
# This function handles the parsing of command-line arguments.
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Returns:
		argparse.Namespace: Parsed arguments with attributes `duplicates`,
		`num_choices`, and `question_type`.
	"""
	parser = bptools.make_arg_parser(description="Generate Henderson-Hasselbalch questions.")
	parser = bptools.add_choice_args(parser, default=4)
	question_group = parser.add_mutually_exclusive_group(required=False)

	format_group = parser.add_mutually_exclusive_group(required=False)
	format_group.add_argument(
		'--format', dest='question_format', type=str,
		choices=('mc', 'num'),
		help='Set question format for numeric-style question types.'
	)
	format_group.add_argument(
		'--mc', dest='question_format', action='store_const', const='mc',
		help='Set question format to multiple choice'
	)
	format_group.add_argument(
		'--num', '--numeric', dest='question_format', action='store_const', const='num',
		help='Set question format to numeric entry'
	)

	# Add an option to manually set the question type
	question_group.add_argument(
		'-t', '--type', dest='hh_type', type=str,
		choices=('equation', 'pH', 'pKa', 'ratio'),
		help='Set the Henderson-Hasselbalch question type.'
	)

	# Add a shortcut option to set the question type to 'equation'
	question_group.add_argument(
		'-e', '--equation', dest='hh_type', action='store_const', const='equation',
		help='Set question type to equation'
	)

	# Add a shortcut option to set the question type to 'pH'
	question_group.add_argument(
		'-p', '--ph', '--pH', dest='hh_type', action='store_const', const='pH',
		help='Set question type to pH'
	)

	# Add a shortcut option to set the question type to 'pKa'
	question_group.add_argument(
		'-k', '--pka', '--pKa', dest='hh_type', action='store_const', const='pKa',
		help='Set question type to pKa'
	)

	# Add a shortcut option to set the question type to 'ratio'
	question_group.add_argument(
		'-r', '--ratio', dest='hh_type', action='store_const', const='ratio',
		help='Set question type to ratio'
	)
	parser.set_defaults(hh_type='equation')
	parser.set_defaults(question_format=None)

	# Parse the provided command-line arguments and return them
	args = parser.parse_args()
	if args.question_format is None:
		if args.hh_type == 'equation':
			args.question_format = 'mc'
		else:
			args.question_format = 'num'
	return args

#===========================================================
#===========================================================
# This function serves as the entry point for generating and saving questions.
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""

	# Parse arguments from the command line
	args = parse_arguments()

	if args.hh_type == 'equation' and args.duplicates > 16:
		args.duplicates = 16
	outfile_suffix = args.hh_type
	if args.hh_type != 'equation':
		outfile_suffix = f"{args.hh_type}_{args.question_format}"
	outfile = bptools.make_outfile(None, outfile_suffix)
	bptools.collect_and_write_questions(write_question, args, outfile)

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
