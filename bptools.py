#General Toosl for These Problems
import os
import re
import sys
import random
import subprocess
from collections import defaultdict

from qti_package_maker.common import anti_cheat
from qti_package_maker.common import yaml_tools
from qti_package_maker.common import color_wheel
from qti_package_maker.common import string_functions
from qti_package_maker.assessment_items import validator
from qti_package_maker.assessment_items import item_types
from qti_package_maker.engines.bbq_text_upload import write_item as bbq_write_item
from qti_package_maker.engines.human_readable import write_item as human_write_item

answer_histogram = defaultdict(int)
question_count = 0
letters = 'ABCDEFGHJKMNPQRSTUWXYZ'
crc16_dict = {}

nocheater = anti_cheat.AntiCheat()

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
def default_color_wheel(num_colors, my_color_wheel=dark_color_wheel):
	return color_wheel.default_color_wheel(num_colors, my_color_wheel)
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

def formatBB_MC_Question(N: int, question_text: str, choices_list, answer_text):
	# deal with item classes
	item_cls = item_types.MC(question_text, choices_list, answer_text)
	item_cls.item_number = N
	nocheat_item_cls = nocheater.modify_item_cls(item_cls)
	# update histogram
	for i, choice_text in enumerate(choices_list):
		if choice_text == answer_text:
			answer_histogram[letters[i]] += 1
	# get format
	human_readable_text = human_write_item.MC(item_cls)
	bb_question_text = bbq_write_item.MC(nocheat_item_cls)
	if human_readable_text is not None:
		print(human_readable_text)
	# update counter and return
	global question_count
	question_count += 1
	return bb_question_text

#=====================
def formatBB_MA_Question(N: int, question_text: str, choices_list, answers_list,
		min_answers_required: int = 2, allow_all_correct: bool = False):
	# deal with item classes
	item_cls = item_types.MA(question_text, choices_list, answers_list, min_answers_required, allow_all_correct)
	item_cls.item_number = N
	nocheat_item_cls = nocheater.modify_item_cls(item_cls)
	# update histogram
	for i, choice_text in enumerate(choices_list):
		if choice_text in answers_list:
			answer_histogram[letters[i]] += 1
	# get format
	human_readable_text = human_write_item.MA(item_cls)
	bb_question_text = bbq_write_item.MA(nocheat_item_cls)
	if human_readable_text is not None:
		print(human_readable_text)
	# update counter and return
	global question_count
	question_count += 1
	return bb_question_text

#=====================
def formatBB_MAT_Question(N: int, question_text: str, prompts_list, choices_list):
	# deal with item classes
	item_cls = item_types.MATCH(question_text, prompts_list, choices_list)
	item_cls.item_number = N
	nocheat_item_cls = nocheater.modify_item_cls(item_cls)
	# get format
	human_readable_text = human_write_item.MATCH(item_cls)
	bb_question_text = bbq_write_item.MATCH(nocheat_item_cls)
	if human_readable_text is not None:
		print(human_readable_text)
	# update counter and return
	global question_count
	question_count += 1
	return bb_question_text

#=====================
def formatBB_FIB_Question(N: int, question_text: str, answers_list):
	# deal with item classes
	item_cls = item_types.FIB(question_text, answers_list)
	item_cls.item_number = N
	nocheater.use_no_click_div = False
	nocheat_item_cls = nocheater.modify_item_cls(item_cls)
	# get format
	human_readable_text = human_write_item.FIB(item_cls)
	bb_question_text = bbq_write_item.FIB(nocheat_item_cls)
	if human_readable_text is not None:
		print(human_readable_text)
	# update counter and return
	global question_count
	question_count += 1
	return bb_question_text

#=====================
def formatBB_FIB_PLUS_Question(N: int, question_text: str, answer_map: dict) -> str:
	# deal with item classes
	item_cls = item_types.MULTI_FIB(question_text, answer_map)
	item_cls.item_number = N
	nocheater.use_no_click_div = False
	nocheat_item_cls = nocheater.modify_item_cls(item_cls)
	# get format
	human_readable_text = human_write_item.MULTI_FIB(item_cls)
	bb_question_text = bbq_write_item.MULTI_FIB(nocheat_item_cls)
	if human_readable_text is not None:
		print(human_readable_text)
	# update counter and return
	global question_count
	question_count += 1
	return bb_question_text

#=====================
def formatBB_NUM_Question(N: int, question_text: str, answer_float, tolerance_float, tol_message=True):
	# deal with item classes
	item_cls = item_types.NUM(question_text, answer_float, tolerance_float, tol_message)
	item_cls.item_number = N
	nocheater.use_no_click_div = False
	nocheat_item_cls = nocheater.modify_item_cls(item_cls)
	# get format
	human_readable_text = human_write_item.NUM(item_cls)
	bb_question_text = bbq_write_item.NUM(nocheat_item_cls)
	if human_readable_text is not None:
		print(human_readable_text)
	# update counter and return
	global question_count
	question_count += 1
	return bb_question_text

#=====================
def formatBB_ORD_Question(N: int, question_text: str, ordered_answers_list):
	# deal with item classes
	item_cls = item_types.ORDER(question_text, ordered_answers_list)
	item_cls.item_number = N
	nocheater.use_no_click_div = False
	nocheat_item_cls = nocheater.modify_item_cls(item_cls)
	# get format
	human_readable_text = human_write_item.ORDER(item_cls)
	bb_question_text = bbq_write_item.ORDER(nocheat_item_cls)
	if human_readable_text is not None:
		print(human_readable_text)
	# update counter and return
	global question_count
	question_count += 1
	return bb_question_text

#===================================================================================
#===================================================================================
#===================================================================================

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
