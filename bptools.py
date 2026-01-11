#General Toosl for These Problems
import os
import sys
import inspect
import argparse
import subprocess
from collections import defaultdict

import tabulate

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
nocheater.use_insert_hidden_terms = True
nocheater.use_no_click_div = True

#==========================
def _patch_anticheat_insert_hidden_terms():
	"""
	Compatibility shim for qti_package_maker AntiCheat API changes.

	Some versions call insert_hidden_terms(text, hidden_term_bank) while others define
	insert_hidden_terms(text) and store the term bank on self.
	"""
	sig = inspect.signature(anti_cheat.AntiCheat.insert_hidden_terms)
	if len(sig.parameters) == 2:
		original = anti_cheat.AntiCheat.insert_hidden_terms

		def insert_hidden_terms(self, text_content: str, hidden_term_bank=None) -> str:
			return original(self, text_content)

		anti_cheat.AntiCheat.insert_hidden_terms = insert_hidden_terms


_patch_anticheat_insert_hidden_terms()

#==========================
def _get_git_root(path=None):
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
def get_repo_data_path(*parts):
	"""
	Build an absolute path under the repo data directory.

	Args:
		parts (tuple): Path components under the data directory.

	Returns:
		str: Absolute path to the requested data file.
	"""
	git_root = _get_git_root()
	if git_root is None:
		raise FileNotFoundError("Unable to locate git root for data path resolution.")
	return os.path.join(git_root, "data", *parts)

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
def light_and_dark_color_wheel(num_colors, dark_color_wheel=dark_color_wheel, light_color_wheel=light_color_wheel):
	return color_wheel.light_and_dark_color_wheel(num_colors, dark_color_wheel, light_color_wheel)
#==========================
def write_html_color_table(filename):
	color_wheel.write_html_color_table(filename)
#==========================
def _default_color_wheel_calc(num_colors=4):
	return color_wheel.default_color_wheel_calc(num_colors)
#==========================
def make_color_wheel(r, g, b, degree_step=40):
	return color_wheel.make_color_wheel(r, g, b, degree_step)

#===================================================================================
#===================================================================================
#===================================================================================

#==========================
def print_histogram():
	sys.stderr.write("=== Answer Choice Histogram ===\n")
	keys = list(answer_histogram.keys())
	keys.sort()
	total_answers = 0
	values_row = []
	for key in keys:
		count = answer_histogram[key]
		total_answers += count
		values_row.append(count)
	headers = list(keys)
	headers.append("TOTAL")
	values_row.append(total_answers)
	table_text = tabulate.tabulate(
		[values_row],
		headers=headers,
		tablefmt="fancy_grid"
	)
	print(table_text, file=sys.stderr)
	sys.stderr.write("Total Questions = {0:d}; Total Answers = {1:d}\n".format(question_count, total_answers))

#===================================================================================
#===================================================================================
#===================================================================================

#==========================
def _add_base_args(parser):
	"""
	Add base CLI arguments for common generators.

	Args:
		parser (argparse.ArgumentParser): Argument parser to extend.

	Returns:
		argparse.ArgumentParser: The updated parser.
	"""
	parser.add_argument(
		'-d', '--duplicate-runs', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='Number of duplicate runs (attempts) to generate questions.',
		default=2
	)
	parser.add_argument(
		'-x', '--max-questions', type=int, dest='max_questions',
		default=None, help='Maximum number of questions to keep.'
	)
	return parser

#==========================
def _add_base_args_batch(parser):
	"""
	Add base CLI arguments for batch generators with a default cap.

	Args:
		parser (argparse.ArgumentParser): Argument parser to extend.

	Returns:
		argparse.ArgumentParser: The updated parser.
	"""
	parser = _add_base_args(
		parser
	)
	parser.set_defaults(max_questions=99)
	return parser

#==========================
def make_arg_parser(description=None, batch=False):
	"""
	Create a standard argument parser with base args.

	Args:
		description (str): Optional parser description.
		batch (bool): Use batch defaults when True.

	Returns:
		argparse.ArgumentParser: Configured parser.
	"""
	if description is None:
		description = "Generate blackboard questions."
	parser = argparse.ArgumentParser(description=description)
	if batch:
		parser = _add_base_args_batch(
			parser
		)
	else:
		parser = _add_base_args(
			parser
		)
	return parser

#==========================
def add_choice_args(parser, default=5):
	"""
	Add a standard number-of-choices argument.

	Args:
		parser (argparse.ArgumentParser): Argument parser to extend.
		default (int | None): Default number of choices.

	Returns:
		argparse.ArgumentParser: The updated parser.
	"""
	parser.add_argument(
		'-c', '--num-choices', metavar='#', type=int, dest='num_choices',
		help="Number of choices to create.", default=default
	)
	return parser

#==========================
def add_hint_args(parser, hint_default=True, dest='hint'):
	"""
	Add standard hint and no-hint boolean flags.

	Args:
		parser (argparse.ArgumentParser): Argument parser to extend.
		hint_default (bool): Default hint setting.
		dest (str): Destination name for the parsed value.

	Returns:
		argparse.ArgumentParser: The updated parser.
	"""
	parser.add_argument(
		'--hint', dest=dest, action='store_true',
		help='Include a hint in the question'
	)
	parser.add_argument(
		'--no-hint', dest=dest, action='store_false',
		help='Do not include a hint in the question'
	)
	parser.set_defaults(**{dest: hint_default})
	return parser

#==========================
def add_scenario_args(parser, dest='scenario_order', default='random'):
	"""
	Add a standard scenario-order toggle for scripts that precompute a scenario list.

	By default, we prefer random ordering for student assessment use-cases.
	"""
	group = parser.add_mutually_exclusive_group(required=False)
	group.add_argument(
		'--sorted', dest=dest, action='store_const', const='sorted',
		help='Use deterministic sorted scenario order.'
	)
	group.add_argument(
		'--random', dest=dest, action='store_const', const='random',
		help='Use randomized scenario order (default).'
	)
	parser.set_defaults(**{dest: default})
	return parser

#==========================
def add_question_format_args(parser, types_list=None, required=True, default=None):
	"""
	Add standard question format arguments.

	Args:
		parser (argparse.ArgumentParser): Argument parser to extend.
		types_list (list): Allowed question formats (ma, mc, num, fib).
		required (bool): Require one of the options.
		default (str | None): Default when not required.

	Returns:
		argparse.ArgumentParser: The updated parser.
	"""
	if types_list is None:
		types_list = ['mc', 'num']
	allowed_types = ['ma', 'mc', 'num', 'fib']
	clean_types = []
	for format_name in types_list:
		format_text = str(format_name).lower()
		if format_text not in allowed_types:
			sys.stderr.write(
				"WARNING: unknown question format ignored ({0})\n".format(format_text)
			)
			continue
		if format_text in clean_types:
			continue
		clean_types.append(format_text)
	if len(clean_types) == 0:
		raise ValueError("No valid question formats were provided.")
	dest = 'question_type'
	question_group = parser.add_mutually_exclusive_group(required=required)
	question_group.add_argument(
		'--format', dest=dest, type=str,
		choices=tuple(clean_types),
		help='Set the question format.'
	)
	if 'mc' in clean_types:
		question_group.add_argument(
			'--mc', dest=dest, action='store_const', const='mc',
			help='Set question format to multiple choice'
		)
		question_group.add_argument(
			'--multiple-choice', dest=dest, action='store_const', const='mc',
			help='Set question format to multiple choice'
		)
	if 'ma' in clean_types:
		question_group.add_argument(
			'--ma', dest=dest, action='store_const', const='ma',
			help='Set question format to multiple answer'
		)
		question_group.add_argument(
			'--multiple-answer', dest=dest, action='store_const', const='ma',
			help='Set question format to multiple answer'
		)
	if 'num' in clean_types:
		question_group.add_argument(
			'--num', dest=dest, action='store_const', const='num',
			help='Set question format to numeric'
		)
		question_group.add_argument(
			'--numeric', dest=dest, action='store_const', const='num',
			help='Set question format to numeric'
		)
	if 'fib' in clean_types:
		question_group.add_argument(
			'--fib', dest=dest, action='store_const', const='fib',
			help='Set question format to fill in the blank'
		)
		question_group.add_argument(
			'--fill-in-blank', dest=dest, action='store_const', const='fib',
			help='Set question format to fill in the blank'
		)
	if required is False and default is not None:
		parser.set_defaults(**{dest: default})
	return parser

#==========================
def add_difficulty_args(parser, dest='difficulty', default='medium'):
	"""
	Add standard difficulty arguments (easy/medium/rigorous).

	Args:
		parser (argparse.ArgumentParser): Argument parser to extend.
		dest (str): Destination name for the parsed value.
		default (str): Default difficulty.

	Returns:
		argparse.ArgumentParser: The updated parser.
	"""
	difficulty_group = parser.add_mutually_exclusive_group(required=False)
	difficulty_group.add_argument(
		'--difficulty', dest=dest, type=str,
		choices=('easy', 'medium', 'rigorous'),
		help='Set difficulty level'
	)
	difficulty_group.add_argument(
		'--easy', dest=dest, action='store_const', const='easy',
		help='Set difficulty to easy'
	)
	difficulty_group.add_argument(
		'--medium', dest=dest, action='store_const', const='medium',
		help='Set difficulty to medium'
	)
	difficulty_group.add_argument(
		'--rigorous', dest=dest, action='store_const', const='rigorous',
		help='Set difficulty to rigorous'
	)
	parser.set_defaults(**{dest: default})
	return parser

#==========================
def _warn_shortfall(question_count: int, args):
	"""
	Warn when fewer than max_questions were generated.

	Args:
		question_count (int): Number of accepted questions.
		args (argparse.Namespace): Parsed args with duplicates and max_questions.
	"""
	if args.max_questions is None:
		return
	if question_count >= args.max_questions:
		return
	sys.stderr.write(
		"WARNING: generated {0} of {1} questions after {2} attempts\n".format(
			question_count, args.max_questions, args.duplicates
		)
	)

#==========================
def _prepare_question_text(question_text: str, question_label: str):
	"""
	Validate and normalize a question string.

	Args:
		question_text (str): Question string or None.
		question_label (str): Label for warnings (usually question number).

	Returns:
		str | None: Normalized question string or None to skip.
	"""
	if question_text is None:
		return None
	if not isinstance(question_text, str):
		sys.stderr.write(
			"WARNING: non-string question skipped ({0})\n".format(question_label)
		)
		return None
	if len(question_text.strip()) == 0:
		sys.stderr.write(
			"WARNING: empty question skipped ({0})\n".format(question_label)
		)
		return None
	check_text = question_text
	if check_text.endswith("\n"):
		check_text = check_text[:-1]
	if "\n" in check_text or "\r" in check_text:
		sys.stderr.write(
			"WARNING: internal newline skipped ({0})\n".format(question_label)
		)
		return None
	if question_text.endswith("\n") is False:
		question_text += "\n"
	return question_text

#==========================
def _should_print_histogram(questions_list: list) -> bool:
	"""
	Check whether questions include MC/MA prefixes.

	Args:
		questions_list (list): List of question strings.

	Returns:
		bool: True when MC/MA questions are present.
	"""
	for question_text in questions_list:
		if question_text.startswith("MC\t") or question_text.startswith("MA\t"):
			return True
	return False

#==========================
def _collect_questions(write_question, args, print_histogram_flag=True) -> list:
	"""
	Collect questions from a single-question writer.

	Args:
		write_question (callable): Function that returns a question string or None.
		args (argparse.Namespace): Parsed arguments with duplicates and max_questions.
		print_histogram_flag (bool): Print histogram when MC/MA questions are present.

	Returns:
		list: List of question strings.
	"""
	questions = []
	n = 0
	max_questions = args.max_questions
	for _ in range(args.duplicates):
		question_text = write_question(n + 1, args)
		if isinstance(question_text, list):
			sys.stderr.write(
				"WARNING: write_question returned a list; use collect_question_batches\n"
			)
			continue
		prepared_question = _prepare_question_text(question_text, str(n + 1))
		if prepared_question is None:
			continue
		questions.append(prepared_question)
		n += 1
		if max_questions is not None and n >= max_questions:
			break
	if print_histogram_flag and _should_print_histogram(questions):
		print_histogram()
	_warn_shortfall(n, args)
	return questions

#==========================
def collect_question_batches(write_question_batch, args, print_histogram_flag=True) -> list:
	"""
	Collect questions from a batch writer.

	Args:
		write_question_batch (callable): Function that returns a list of questions.
		args (argparse.Namespace): Parsed arguments with duplicates and max_questions.
		print_histogram_flag (bool): Print histogram when MC/MA questions are present.

	Returns:
		list: List of question strings.
	"""
	questions = []
	n = 0
	max_questions = args.max_questions
	for _ in range(args.duplicates):
		batch = write_question_batch(n + 1, args)
		if batch is None:
			sys.stderr.write(
				"WARNING: write_question_batch returned None; expected list\n"
			)
			continue
		if not isinstance(batch, list):
			sys.stderr.write(
				"WARNING: write_question_batch did not return a list; skipped\n"
			)
			continue
		if len(batch) == 0:
			continue
		for question_text in batch:
			prepared_question = _prepare_question_text(question_text, str(n + 1))
			if prepared_question is None:
				continue
			questions.append(prepared_question)
			n += 1
			if max_questions is not None and n >= max_questions:
				break
		if max_questions is not None and n >= max_questions:
			break
	if print_histogram_flag and _should_print_histogram(questions):
		print_histogram()
	_warn_shortfall(n, args)
	return questions

#==========================
def make_outfile(*parts) -> str:
	"""
	Build a bbq output filename with optional suffix parts.

	Args:
		parts (tuple): Optional suffix parts to append to the filename.

	Returns:
		str: Output filename.
	"""
	# Backward compatibility:
	# - historical call sites used `make_outfile(None, ...)` or `make_outfile(__file__, ...)`
	#   even though the base name is already derived from sys.argv[0].
	# - some older call sites used `make_outfile("MC")` intending "MC" as a suffix part.
	if len(parts) > 0 and parts[0] is None:
		parts = parts[1:]
	elif len(parts) > 0:
		first = str(parts[0]).strip()
		looks_like_path = (
			(os.sep in first)
			or ("/" in first)
			or ("\\" in first)
			or first.endswith(".py")
		)
		if looks_like_path:
			parts = parts[1:]

	main_file = getattr(sys.modules.get("__main__"), "__file__", None)
	if isinstance(main_file, str) and main_file.endswith(".py") and main_file not in ("<stdin>", "<string>"):
		script_path = main_file
	else:
		script_path = sys.argv[0]
		if isinstance(script_path, str):
			if script_path in ("-c", "-m") or (not script_path.endswith(".py")):
				# Wrapper fallback: when argv[0] is not a useful script path, check for a
				# nearby *.py argument.
				for idx in (1, 2):
					if len(sys.argv) <= idx:
						break
					cand = sys.argv[idx]
					if isinstance(cand, str) and cand.endswith(".py") and cand not in ("<stdin>", "<string>"):
						script_path = cand
						break

	if script_path is None or len(str(script_path)) == 0:
		script_name = "script"
	else:
		script_name = os.path.splitext(os.path.basename(script_path))[0]
	suffix = ""
	for part in parts:
		if part is None:
			continue
		part_text = str(part)
		if len(part_text) == 0:
			continue
		suffix += f"-{part_text}"
	outfile = f"bbq-{script_name}{suffix}-questions.txt"
	return outfile

#==========================
def _write_questions_to_file(questions: list, outfile: str):
	"""
	Write questions to a file and print status messages.

	Args:
		questions (list): List of question strings.
		outfile (str): Output filename.
	"""
	question_count = len(questions)
	word = "question" if question_count == 1 else "questions"
	print(f"\nWriting {question_count} {word} to file: {outfile}")
	with open(outfile, "w") as f:
		for question_text in questions:
			f.write(question_text)
	print(f"... saved {question_count} {word} to {outfile}\n")

#==========================
def write_questions_to_file(questions: list, outfile: str):
	"""
	Public wrapper for writing questions to a file.

	Prefer `collect_and_write_questions(...)` in scripts.
	"""
	return _write_questions_to_file(questions, outfile)

#==========================
def collect_and_write_questions(write_question, args, outfile, print_histogram_flag=True) -> list:
	"""
	Collect questions and write them to a file.

	Args:
		write_question (callable): Function that returns a question string or None.
		args (argparse.Namespace): Parsed arguments with duplicates and max_questions.
		outfile (str): Output filename.
		print_histogram_flag (bool): Print histogram when MC/MA questions are present.

	Returns:
		list: List of question strings.
	"""
	questions = _collect_questions(write_question, args, print_histogram_flag)
	_write_questions_to_file(questions, outfile)
	return questions

#===================================================================================
#===================================================================================
#===================================================================================

def formatBB_MC_Question(N: int, question_text: str, choices_list, answer_text):
	# deal with item classes
	item_cls = item_types.MC(question_text, choices_list, answer_text)
	item_cls.item_number = N
	nocheat_item_cls = nocheater.modify_item_cls(item_cls)
	nocheat_item_cls.answer_text = nocheat_item_cls.choices_list[nocheat_item_cls.answer_index]
	nocheat_item_cls._validate()
	# update histogram
	for i, choice_text in enumerate(choices_list):
		if choice_text == answer_text:
			answer_histogram[letters[i]] += 1
	# get format
	human_readable_text = human_write_item.MC(item_cls)
	bb_question_text = bbq_write_item.MC(nocheat_item_cls)
	if human_readable_text is not None:
		print(f"{N:3d}. {human_readable_text}")

	# update countr and return
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
	nocheat_item_cls.answers_list = [nocheat_item_cls.choices_list[idx] for idx in nocheat_item_cls.answer_index_list]
	nocheat_item_cls._validate()
	# update histogram
	for i, choice_text in enumerate(choices_list):
		if choice_text in answers_list:
			answer_histogram[letters[i]] += 1
	# get format
	human_readable_text = human_write_item.MA(item_cls)
	bb_question_text = bbq_write_item.MA(nocheat_item_cls)
	if human_readable_text is not None:
		print(f"{N:3d}. {human_readable_text}")

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
	nocheat_item_cls._validate()
	# get format
	human_readable_text = human_write_item.MATCH(item_cls)
	bb_question_text = bbq_write_item.MATCH(nocheat_item_cls)
	if human_readable_text is not None:
		print(f"{N:3d}. {human_readable_text}")
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
	nocheat_item_cls.answers_list = item_cls.answers_list
	nocheat_item_cls._validate()
	# get format
	human_readable_text = human_write_item.FIB(item_cls)
	bb_question_text = bbq_write_item.FIB(nocheat_item_cls)
	if human_readable_text is not None:
		print(f"{N:3d}. {human_readable_text}")

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
	#nocheat_item_cls.answer_map = item_cls.answer_map
	nocheat_item_cls._validate()
	# get format
	human_readable_text = human_write_item.MULTI_FIB(item_cls)
	bb_question_text = bbq_write_item.MULTI_FIB(nocheat_item_cls)
	if human_readable_text is not None:
		print(f"{N:3d}. {human_readable_text}")

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
	nocheat_item_cls._validate()
	# get format
	human_readable_text = human_write_item.NUM(item_cls)
	bb_question_text = bbq_write_item.NUM(nocheat_item_cls)
	if human_readable_text is not None:
		print(f"{N:3d}. {human_readable_text}")

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
	nocheat_item_cls._validate()
	# get format
	human_readable_text = human_write_item.ORDER(item_cls)
	bb_question_text = bbq_write_item.ORDER(nocheat_item_cls)
	if human_readable_text is not None:
		print(f"{N:3d}. {human_readable_text}")

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
