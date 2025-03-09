#General Toosl for These Problems
import os
import re
import sys
import random
import subprocess
from collections import defaultdict

from qti_package_maker.common import yaml_tools
from qti_package_maker.common import color_wheel
from qti_package_maker.common import string_functions
from qti_package_maker.assessment_items import validator
from qti_package_maker.assessment_items import item_types
from qti_package_maker.engines.bbq_text_upload import write_item as bbq_write_item
from qti_package_maker.engines.human_readable import write_item as human_write_item


#anticheating measures
use_nocopy_script = False
use_insert_hidden_terms = False
hidden_term_density = 0.7
use_add_no_click_div = False
noPrint = True
noCopy = True
noScreenshot = False
autoBlur = True

hidden_term_bank = None
answer_histogram = defaultdict(int)
question_count = 0
crc16_dict = {}

#===========================================================
#===========================================================
def number_to_ordinal(integer):
	return string_functions.number_to_ordinal(integer)
#==========================
def number_to_cardinal(integer):
	return string_functions.number_to_cardinal(integer)
#==========================
def makeQuestionPretty(question):
	return string_functions.make_question_pretty(question)
#==========================
def html_monospace(txt, use_nbsp=True):
	return string_functions.html_monospace(txt, use_nbsp)
#==========================
def colorHTMLText(text, hex_code):
	return string_functions.html_color_text(text, hex_code)
#==========================
def generate_gene_letters(num_genes, shift=-1, clear=False):
	return string_functions.generate_gene_letters(num_genes, shift, clear)
#==========================
def checkAscii(mystr):
	return string_functions.check_ascii(mystr)
#==========================
def getCrc16_FromString(mystr):
	return string_functions.get_crc16_from_string(mystr)

#===========================================================
#===========================================================
def readYamlFile(yaml_file):
	return yaml_tools.read_yaml_file(yaml_file)

#===========================================================
#===========================================================
def is_valid_html(html_str: str) -> bool:
	return validator.validate_html(html_str)


#===========================================================
#===========================================================
def min_difference(numbers: list) -> int:
	return color_wheel.min_difference(numbers)
#==========================
dark_color_wheel = color_wheel.dark_color_wheel
light_color_wheel = color_wheel.light_color_wheel
extra_light_color_wheel = color_wheel.extra_light_color_wheel
#==========================
def get_indices_for_color_wheel(num_colors, color_wheel_length):
	return color_wheel.get_indices_for_color_wheel(num_colors, color_wheel_length)
#==========================
def default_color_wheel(num_colors, color_wheel=dark_color_wheel):
	return color_wheel.default_color_wheel(num_colors, color_wheel)
#==========================
def default_color_wheel2(num_colors, random_shift=True):
	return color_wheel.default_color_wheel2(num_colors, random_shift)
#==========================
def light_and_dark_color_wheel(num_colors, dark_color_wheel=dark_color_wheel, light_color_wheel=light_color_wheel):
	return color_wheel.light_and_dark_color_wheel(num_colors, dark_color_wheel, light_color_wheel)
#==========================
def light_and_dark_color_wheel2(num_colors, random_shift=True, extra_light=False):
	return color_wheel.light_and_dark_color_wheel2(num_colors, random_shift, extra_light)
#==========================
def write_html_color_table(filename):
	color_wheel.write_html_color_table(filename)
#==========================
def default_color_wheel_calc(num_colors=4):
	return color_wheel.default_color_wheel_calc(num_colors)
#==========================
def make_color_wheel(r, g, b, degree_step=40):
	return color_wheel.make_color_wheel(r, g, b, degree_step)

#===================================================================================
#===================================================================================
#===================================================================================

#==========================
def generate_js_function():
	#global use_nocopy_script
	if use_nocopy_script is False:
		return ''
	return jsdelivr_js_function()
	#return pdfanticopy_js_function()

#==========================
def pdfanticopy_js_function():
	# Using Python f-string to include global variables in the JavaScript code
	js_code = f'<script>var noPrint={str(noPrint).lower()};var noCopy={str(noCopy).lower()};var noScreenshot={str(noScreenshot).lower()};var autoBlur={str(autoBlur).lower()};</script>'
	js_code += '<script type="text/javascript" '
	js_code += 'src="https://pdfanticopy.com/noprint.js"'
	js_code += '></script>'
	return js_code

#==========================
def jsdelivr_js_function():
	# Similar technique is applied here, variables are inserted dynamically
	js_code = f'<script>var noPrint={str(noPrint).lower()};var noCopy={str(noCopy).lower()};var noScreenshot={str(noScreenshot).lower()};var autoBlur={str(autoBlur).lower()};</script>'
	js_code += '<script type="text/javascript" '
	js_code += 'src="https://cdn.jsdelivr.net/gh/vosslab/biology-problems@main/javascript/noprint.js"'
	js_code += '></script>'
	return js_code

#==========================
def add_no_click_div(text):
	#global use_add_no_click_div
	if use_add_no_click_div is False:
		return text
	number = random.randint(1000,9999)
	output  = f'<div id="drv_{number}" '
	output += 'oncopy="return false;" onpaste="return false;" oncut="return false;" '
	output += 'oncontextmenu="return false;" onmousedown="return false;" onselectstart="return false;" '
	output += '>'
	output += text
	output += '</div>'
	return output

#==========================
def QuestionHeader(question, N, big_question=None, crc16=None):
	global crc16_dict
	#global use_nocopy_script
	if crc16 is None:
		if big_question is not None:
			crc16 = getCrc16_FromString(big_question)
		else:
			crc16 = getCrc16_FromString(question)
	if crc16_dict.get(crc16) == 1:
		print('crc16 first hash collision', crc16)
		crc16_dict[crc16] += 1
	elif crc16_dict.get(crc16) == 3:
		global question_count
		print('crc16 third hash collision', crc16, 'after question #', question_count)
		crc16_dict[crc16] += 1
	else:
		crc16_dict[crc16] = 1
	#header = '<p>{0:03d}. {1}</p> {2}'.format(N, crc16, question)
	pretty_question = makeQuestionPretty(question)
	print('{0:03d}. {1} -- {2}'.format(N, crc16, pretty_question))
	noisy_question = insert_hidden_terms(question)
	text = '<p>{0}</p> {1}'.format(crc16, noisy_question)
	header = ''
	if use_nocopy_script is True:
		js_function_string = generate_js_function()
		header += js_function_string
	header += add_no_click_div(text)
	return header

#==========================
def ChoiceHeader(choice_text):
	noisy_choice_text = insert_hidden_terms(choice_text)
	output = add_no_click_div(noisy_choice_text)
	return output

#==========================
def print_histogram():
	global question_count
	sys.stderr.write("=== Answer Choice Histogram ===\n")
	keys = list(answer_histogram.keys())
	keys.sort()
	total_answers = 0
	for key in keys:
		total_answers += answer_histogram[key]
		sys.stderr.write("{0}: {1},  ".format(key, answer_histogram[key]))
	sys.stderr.write("\n")
	sys.stderr.write("Total Questions = {0:d}; Total Answers = {1:d}\n".format(question_count, total_answers))

#===================================================================================
#===================================================================================
#===================================================================================

def formatBB_MC_Question(N, question_text, choices_list, answer_text):
	global question_count
	item_cls = item_types.MC(question_text, choices_list, answer_text)
	letters = 'ABCDEFGHJKMNPQRSTUWXYZ'
	for i, choice_text in enumerate(choices_list):
		if choice_text == answer_text:
			answer_histogram[letters[i]] += 1
	human_readable_text = human_write_item.MC(item_cls)
	bb_question_text = bbq_write_item.MC(item_cls)
	print(human_readable_text)
	question_count += 1
	return bb_question_text

#=====================
def formatBB_MA_Question(N, question_text, choices_list, answers_list):
	global question_count
	item_cls = item_types.MA(question_text, choices_list, answers_list)
	letters = 'ABCDEFGHJKMNPQRSTUWXYZ'
	for i, choice_text in enumerate(choices_list):
		if choice_text in answers_list:
			answer_histogram[letters[i]] += 1
	human_readable_text = human_write_item.MA(item_cls)
	bb_question_text = bbq_write_item.MA(item_cls)
	print(human_readable_text)
	question_count += 1
	return bb_question_text

#=====================
def formatBB_FIB_Question(N, question, answers_list):
	global question_count
	validator.validate_FIB(question, answers_list)
	global use_add_no_click_div
	use_add_no_click_div = False
	#fill in the black = FIB
	#FIB TAB question text TAB answer text TAB answer two text
	bb_question = ''

	#number = "{0}. ".format(N)
	bb_question += 'FIB\t'
	big_question = question + ' '.join(answers_list)
	bb_question += QuestionHeader(question, N, big_question)

	for i, answer in enumerate(answers_list):
		bb_question += '\t{0}'.format(answer)
		print("- {0}".format(makeQuestionPretty(answer)))
	print("")
	question_count += 1
	return bb_question + '\n'

#=====================
def formatBB_FIB_PLUS_Question(N: int, question: str, answer_map: dict) -> str:
	global question_count
	validator.validate_MULTI_FIB(question, answer_map)
	global use_add_no_click_div
	use_add_no_click_div = False
	#FIB_PLUS TAB question text TAB variable1 TAB answer1 TAB answer2 TAB TAB variable2 TAB answer3
	bb_question = ''
	bb_question += 'FIB_PLUS\t'
	bb_question += QuestionHeader(question, N)
	keys_list = sorted(answer_map.keys())
	for key in keys_list:
		value_list = answer_map[key]
		print(f"- KEY [{key}] -> {value_list}")
		bb_question += f'\t{key}'
		for value in value_list:
			bb_question += f'\t{value}'
		bb_question += '\t'
	bb_question += '\n'
	return bb_question

#=====================
def formatBB_NUM_Question(N, question, answer, tolerance, tol_message=True):
	#NUM TAB question text TAB answer TAB [optional]tolerance
	global question_count
	validator.validate_NUM(question, answer, tolerance, tol_message)

	bb_question = ''
	bb_question += 'NUM\t'
	if tol_message is True:
		question += f'<p><i>Answers need to be within {tolerance/answer*100:.1f}&percnt;'
		question += 'of the actual value to be correct.</i></p> '
	big_question = question + str(answer)
	bb_question += QuestionHeader(question, N, big_question)

	bb_question += '\t{0:.8f}'.format(answer)
	print("=== {0:.3f}".format(answer))
	bb_question += '\t{0:.8f}'.format(tolerance)
	print("+/- {0:.3f}".format(tolerance))
	print("")
	question_count += 1
	return bb_question + '\n'

#=====================
def formatBB_MAT_Question(N, question, prompts_list, choices_list):
	#MAT TAB question text TAB answer text TAB matching text TAB answer two text TAB matching two text
	global question_count
	validator.validate_MATCH(question, prompts_list, choices_list)

	bb_question = ''
	full_quesiton = question + ' '.join(prompts_list) + ' '.join(choices_list)
	crc16 = getCrc16_FromString(full_quesiton)
	bb_question += 'MAT\t'
	bb_question += QuestionHeader(question, N, crc16)

	num_items = min(len(prompts_list), len(choices_list))
	letters = 'ABCDEFGHJKMNPQRSTUWXYZ'
	for i in range(num_items):
		prompt_text = prompts_list[i]
		noisy_prompt_text = ChoiceHeader(prompt_text)
		match_text = choices_list[i]
		noisy_match_text = ChoiceHeader(match_text)
		bb_question += '\t{0}&nbsp;\t{1}&nbsp;'.format(noisy_prompt_text, noisy_match_text)
		print("- {0}. {1} == {2}".format(letters[i], makeQuestionPretty(prompt_text), makeQuestionPretty(match_text)))
	print("")
	question_count += 1
	return bb_question + '\n'

#=====================
def formatBB_ORD_Question(N, question_text, ordered_answers_list):
	#ORD TAB question text TAB answer text TAB answer two text
	global question_count
	validator.validate_ORDER(question_text, ordered_answers_list)

	bb_question = ''
	bb_question += 'ORD\t'
	big_question = question_text + ' '.join(ordered_answers_list)
	bb_question += QuestionHeader(question_text, N, big_question)

	for i, answer_text in enumerate(ordered_answers_list):
		noisy_answer_text = ChoiceHeader(answer_text)
		bb_question += '\t'+noisy_answer_text
		print(f"- [{i+1}] {makeQuestionPretty(answer_text)}")
	print("")
	question_count += 1
	return bb_question + '\n'

#===================================================================================
#===================================================================================
#===================================================================================

def get_git_root(path=None):
	"""Return the absolute path of the repository root."""
	if path is None:
		# Use the path of the script
		path = os.path.dirname(os.path.abspath(__file__))
	try:
		base = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], cwd=path, universal_newlines=True).strip()
		return base
	except subprocess.CalledProcessError:
		# Not inside a git repository
		return None

#==========================
def load_hidden_term_bank():
	git_root = get_git_root()
	data_file_path = os.path.join(git_root, 'data/all_short_words.txt')
	with open(data_file_path, 'r') as file:
		terms = file.readlines()
	return [term.strip() for term in terms]

#==========================
def insert_hidden_terms(text_content):
	if use_insert_hidden_terms is False:
		return text_content

	global hidden_term_bank
	if hidden_term_bank is None:
		hidden_term_bank = load_hidden_term_bank()

	# Separate table, code and non-table/non-code content
	parts = re.split(r'(<table>.*?</table>|<code>.*?</code>)', text_content, flags=re.DOTALL)

	# Process each part
	new_parts = []
	for part in parts:
		if part.startswith('<table>') or part.startswith('<code>'):
			# Keep table and code content unchanged
			new_parts.append(part)
		else:  # Apply the modified logic to non-table parts
			# Replace spaces adjacent to words with '@'
			#part = re.sub(r'([a-z]) +(?![^<>]*>)', r'\1@', part)
			part = re.sub(r'([a-z]) +([a-z])(?![^<>]*>)', r'\1@\2', part)
			#part = re.sub(r'([A-Za-z]) +(?![^<>]*>)', r'\1@', part)
			#part = re.sub(r' +([A-Za-z])(?![^<>]*>)', r'@\1', part)
			words = part.split('@')
			new_words = []
			for word in words:
				new_words.append(word)
				if random.random() < hidden_term_density:
					hidden_term = random.choice(hidden_term_bank)
					new_words.append(f"<span style='font-size: 1px; color: white;'>{hidden_term}</span>")
				else:
					new_words.append(" ")
			new_parts.append(''.join(new_words))
	return ''.join(new_parts)

#==========================
def insert_hidden_terms_old(text_content):
	if use_insert_hidden_terms is False:
		return text_content
	global hidden_term_bank
	if hidden_term_bank is None:
		hidden_term_bank = load_hidden_term_bank()
	# Replace spaces outside HTML tags with '@'
	text_content = re.sub(r'( +)(?![^<>]*>)', '@', text_content)
	words = text_content.split('@')
	new_words = []
	for word in words:
		new_words.append(word)
		hidden_term = random.choice(hidden_term_bank)
		new_words.append(f"<span style='font-size: 1px; color: white;'>{hidden_term}</span>")
	return ''.join(new_words)


#=======================
#=======================

base_replacement_rule_dict = {
	' not ': ' <strong>NOT</strong> ', #BOLD BLACK
	' Not ': ' <strong>NOT</strong> ', #BOLD BLACK
	' NOT ': ' <strong>NOT</strong> ', #BOLD BLACK
	' false ': ' <span style="color: #ba372a;"><strong>FALSE</strong></span> ', #BOLD RED
	' False ': ' <span style="color: #ba372a;"><strong>FALSE</strong></span> ', #BOLD RED
	' FALSE ': ' <span style="color: #ba372a;"><strong>FALSE</strong></span> ', #BOLD RED
	' true ': ' <span style="color: #169179;"><strong>TRUE</strong></span> ', #BOLD GREEN
	' True ': ' <span style="color: #169179;"><strong>TRUE</strong></span> ', #BOLD GREEN
	' TRUE ': ' <span style="color: #169179;"><strong>TRUE</strong></span> ', #BOLD GREEN
	'  ': ' ',
}

#=======================
def append_clear_font_space_to_text(string_text):
	return f'<span style="font-family: sans-serif; letter-spacing: 1px;">{string_text}</span>'

#=======================
def append_clear_font_space_to_list(list_of_text_strings):
	new_list_of_text_strings = []
	for string_text in list_of_text_strings:
		new_string_text = append_clear_font_space_to_text(string_text)
		new_list_of_text_strings.append(new_string_text)
	return new_list_of_text_strings

#=======================
def applyReplacementRulesToText(text_string, replacement_rule_dict):
	if not isinstance(text_string, str):
		raise TypeError(f"value is not string: {text_string}")
	if replacement_rule_dict is None:
		print("no replacement rules found")
		replacement_rule_dict = base_replacement_rule_dict
	else:
		#replacement_rule_dict = {**base_replacement_rule_dict, **replacement_rule_dict}
		replacement_rule_dict |= base_replacement_rule_dict
	for find_text, replace_text in replacement_rule_dict.items():
		if not replace_text.startswith('<strong>'):
			replace_text = f'<strong>{replace_text}</strong>'
		text_string = text_string.replace(find_text, replace_text)
	return text_string

#=======================
def applyReplacementRulesToList(list_of_text_strings, replacement_rule_dict):
	if replacement_rule_dict is None:
		print("no replacement rules found")
		replacement_rule_dict = base_replacement_rule_dict
	else:
		#replacement_rule_dict = {**base_replacement_rule_dict, **replacement_rule_dict}
		replacement_rule_dict |= base_replacement_rule_dict
	new_list_of_text_strings = []
	for text_string in list_of_text_strings:
		if not isinstance(text_string, str):
			raise TypeError(f"value is not string: {text_string}")
		for find_text, replace_text in replacement_rule_dict.items():
			if not replace_text.startswith('<strong>'):
				replace_text = f'<strong>{replace_text}</strong>'
			text_string = text_string.replace(find_text, replace_text)
		new_list_of_text_strings.append(text_string)
	return new_list_of_text_strings
