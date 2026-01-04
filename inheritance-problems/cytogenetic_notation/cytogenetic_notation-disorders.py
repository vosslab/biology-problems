#!/usr/bin/env python3

# built-in python modules
import os
import random
import re

# external pip modules
import yaml

# local repo modules
import bptools

DATA_FILE = os.path.abspath(
	os.path.join(os.path.dirname(__file__), "..", "data", "cytogenetic_disorders.yml")
)

#======================================
#======================================
def load_disorder_data(input_file: str) -> list:
	"""
	Load disorder data from a YAML file and flatten it into a list.

	Args:
		input_file (str): Path to the YAML file.

	Returns:
		list: List of disorder dictionaries with category and name.
	"""
	with open(input_file, "r") as handle:
		raw_data = yaml.safe_load(handle)

	disorders = []
	for category, entries in raw_data.items():
		if entries is None:
			continue
		for disorder_name, entry in entries.items():
			if entry is None:
				entry = {}
			entry_copy = dict(entry)
			entry_copy["category"] = category
			entry_copy["name"] = disorder_name
			disorders.append(entry_copy)
	return disorders

#======================================
#======================================
def choose_notation(notations: list, prefer_mosaic: bool) -> str:
	"""
	Choose a notation string, optionally preferring mosaic examples.

	Args:
		notations (list): List of notation strings.
		prefer_mosaic (bool): Prefer notation with a slash.

	Returns:
		str: Selected notation string.
	"""
	mosaic_notations = [k for k in notations if "/" in k]
	if prefer_mosaic and len(mosaic_notations) > 0:
		return random.choice(mosaic_notations)
	return random.choice(notations)

#======================================
#======================================
def split_karyotype_lines(karyo_str: str) -> list:
	"""
	Split a mosaic karyotype into its component lines.

	Args:
		karyo_str (str): Karyotype string.

	Returns:
		list: List of line strings.
	"""
	return karyo_str.split("/")

#======================================
#======================================
def strip_bracket_counts(karyo_str: str) -> str:
	"""
	Remove bracketed cell counts from a karyotype string.

	Args:
		karyo_str (str): Karyotype string.

	Returns:
		str: Karyotype string without bracket counts.
	"""
	return re.sub(r"\[\d+\]", "", karyo_str)

#======================================
#======================================
def parse_bracket_counts(karyo_str: str) -> list:
	"""
	Parse bracket counts for mosaic lines.

	Args:
		karyo_str (str): Karyotype string.

	Returns:
		list: List of counts or None for each line.
	"""
	lines = split_karyotype_lines(karyo_str)
	counts = []
	for line in lines:
		match = re.search(r"\[(\d+)\]", line)
		if match is None:
			counts.append(None)
		else:
			counts.append(int(match.group(1)))
	return counts

#======================================
#======================================
def parse_karyotype_to_features(karyo_str: str) -> dict:
	"""
	Parse a karyotype string into biological features.

	Args:
		karyo_str (str): Karyotype string.

	Returns:
		dict: Feature dictionary.
	"""
	if "/" in karyo_str:
		clean_lines = [strip_bracket_counts(line) for line in split_karyotype_lines(karyo_str)]
		features = {
			"raw": karyo_str,
			"is_mosaic": True,
			"cell_lines": clean_lines,
			"cell_counts": parse_bracket_counts(karyo_str),
			"cell_line_features": [parse_karyotype_to_features(line) for line in clean_lines],
		}
		features["sex"] = features["cell_line_features"][0].get("sex")
		return features

	tokens = [tok.strip() for tok in karyo_str.split(",") if tok.strip() != ""]
	if len(tokens) < 2:
		raise ValueError(f"Invalid karyotype string: {karyo_str}")

	features = {
		"raw": karyo_str,
		"is_mosaic": False,
		"total_chromosomes": int(tokens[0]),
		"sex": tokens[1],
	}

	aneuploidy = []
	for tok in tokens[2:]:
		if tok.startswith("+") or tok.startswith("-"):
			aneuploidy.append(tok)
	if len(aneuploidy) > 0:
		features["aneuploidy"] = aneuploidy

	if "rob(" in karyo_str:
		match = re.search(r"rob\(([^)]+)\)\(([^)]+)\)", karyo_str)
		if match is not None:
			chr_pair = match.group(1)
			break_pair = match.group(2)
			chr_a, chr_b = [p.strip() for p in chr_pair.split(";")]
			break_a, break_b = [p.strip() for p in break_pair.split(";")]
			features["event_type"] = "robertsonian_translocation"
			features["chr_a"] = chr_a
			features["chr_b"] = chr_b
			features["break_a"] = break_a
			features["break_b"] = break_b
		elif "event_type" not in features:
			features["event_type"] = "robertsonian_translocation"

	elif "t(" in karyo_str:
		match = re.search(r"t\(([^)]+)\)\(([^)]+)\)", karyo_str)
		if match is not None:
			chr_pair = match.group(1)
			break_pair = match.group(2)
			chr_a, chr_b = [p.strip() for p in chr_pair.split(";")]
			break_a, break_b = [p.strip() for p in break_pair.split(";")]
			features["event_type"] = "reciprocal_translocation"
			features["chr_a"] = chr_a
			features["chr_b"] = chr_b
			features["band_a"] = break_a
			features["band_b"] = break_b
		elif "event_type" not in features:
			features["event_type"] = "reciprocal_translocation"

	elif "del(" in karyo_str:
		match = re.search(r"del\(([^)]+)\)\(([^)]+)\)", karyo_str)
		if match is not None:
			features["event_type"] = "deletion"
			features["chromosome"] = match.group(1).strip()
			features["breakpoint"] = match.group(2).strip()
		elif "event_type" not in features:
			features["event_type"] = "deletion"

	elif "dup(" in karyo_str:
		match = re.search(r"dup\(([^)]+)\)\(([^)]+)\)", karyo_str)
		if match is not None:
			features["event_type"] = "duplication"
			features["chromosome"] = match.group(1).strip()
			features["breakpoint"] = match.group(2).strip()
		elif "event_type" not in features:
			features["event_type"] = "duplication"

	if "event_type" not in features:
		if "aneuploidy" in features:
			features["event_type"] = "aneuploidy"
		else:
			features["event_type"] = "other_or_normal"

	return features

#======================================
#======================================
def build_karyotype_from_features(features: dict) -> str:
	"""
	Build a karyotype string from a feature dictionary.

	Args:
		features (dict): Feature dictionary for a non-mosaic karyotype.

	Returns:
		str: Karyotype string.
	"""
	parts = [str(features["total_chromosomes"]), features["sex"]]
	event_type = features.get("event_type")

	if event_type == "deletion":
		parts.append(f"del({features['chromosome']})({features['breakpoint']})")
	elif event_type == "duplication":
		parts.append(f"dup({features['chromosome']})({features['breakpoint']})")
	elif event_type == "reciprocal_translocation":
		parts.append(
			f"t({features['chr_a']};{features['chr_b']})"
			f"({features['band_a']};{features['band_b']})"
		)
	elif event_type == "robertsonian_translocation":
		parts.append(
			f"rob({features['chr_a']};{features['chr_b']})"
			f"({features.get('break_a', 'q10')};{features.get('break_b', 'q10')})"
		)

	for token in features.get("aneuploidy", []):
		parts.append(token)

	return ",".join(parts)

#======================================
#======================================
def describe_sex(sex_token: str) -> str:
	"""
	Convert sex chromosome token to a sex description.
	"""
	if "Y" in sex_token:
		return "male"
	return "female"

#======================================
#======================================
def describe_aneuploidy(aneuploidy_list: list) -> str:
	"""
	Convert aneuploidy tokens into descriptive text.
	"""
	phrases = []
	for token in aneuploidy_list:
		sign = token[0]
		chrom = token[1:]
		if chrom in ("X", "Y"):
			if sign == "+":
				phrases.append(f"an extra {chrom} chromosome")
			else:
				phrases.append(f"missing {chrom} chromosome")
		else:
			if sign == "+":
				phrases.append(f"trisomy {chrom}")
			else:
				phrases.append(f"monosomy {chrom}")
	return " and ".join(phrases)

#======================================
#======================================
def describe_line(features: dict) -> str:
	"""
	Create a concise description for a non-mosaic karyotype line.
	"""
	event_type = features.get("event_type")
	aneuploidy_list = features.get("aneuploidy", [])

	if event_type == "aneuploidy" and len(aneuploidy_list) > 0:
		return describe_aneuploidy(aneuploidy_list)

	if event_type == "deletion":
		return f"a deletion on chromosome {features['chromosome']}{features['breakpoint']}"

	if event_type == "duplication":
		return f"a duplication on chromosome {features['chromosome']}{features['breakpoint']}"

	if event_type == "reciprocal_translocation":
		return (
			"reciprocal translocation between chromosomes "
			f"{features['chr_a']} and {features['chr_b']} at "
			f"{features['band_a']} and {features['band_b']}"
		)

	if event_type == "robertsonian_translocation":
		base = (
			"Robertsonian translocation involving chromosomes "
			f"{features['chr_a']} and {features['chr_b']}"
		)
		if len(aneuploidy_list) > 0:
			return f"{base} with {describe_aneuploidy(aneuploidy_list)}"
		return base

	if len(aneuploidy_list) > 0:
		return describe_aneuploidy(aneuploidy_list)

	return ""

#======================================
#======================================
def is_normal_line(features: dict) -> bool:
	"""
	Check if a line looks like a normal 46 chromosome line.
	"""
	if features.get("total_chromosomes") != 46:
		return False
	if features.get("event_type") != "other_or_normal":
		return False
	if len(features.get("aneuploidy", [])) > 0:
		return False
	return True

#======================================
#======================================
def format_counts_fraction(counts: list, abnormal_index: int) -> str:
	"""
	Format bracket counts as a fraction for mosaic descriptions.
	"""
	if counts is None:
		return ""
	if any(count is None for count in counts):
		return ""
	total = sum(counts)
	if total <= 0:
		return ""
	abnormal = counts[abnormal_index]
	return f" ({abnormal} of {total} cells)"

#======================================
#======================================
def features_to_science_description(features: dict, disorder_entry: dict) -> str:
	"""
	Convert features into a short lab-style description.
	"""
	sex_text = describe_sex(features.get("sex", "XX"))

	if features.get("is_mosaic"):
		lines = features.get("cell_line_features", [])
		normal_index = None
		for i, line_features in enumerate(lines):
			if is_normal_line(line_features):
				normal_index = i
				break
		abnormal_index = 0
		for i, line_features in enumerate(lines):
			if normal_index is None or i != normal_index:
				abnormal_index = i
				if not is_normal_line(line_features):
					break
		abnormal_line = lines[abnormal_index]
		abnormal_phrase = describe_line(abnormal_line)
		count_phrase = format_counts_fraction(features.get("cell_counts"), abnormal_index)
		return (
			f"{sex_text} with mosaicism: a normal 46-chromosome line and a line with "
			f"{abnormal_phrase}{count_phrase}."
		)

	line_description = describe_line(features)
	if line_description != "":
		return f"{sex_text} with {line_description}."

	return f"{sex_text} with a normal chromosome count ({features['total_chromosomes']})."

#======================================
#======================================
def format_karyotype(karyo_str: str) -> str:
	"""
	Wrap a karyotype string in monospace HTML.
	"""
	return (
		"<span style='font-family: monospace; font-weight: bold;'>"
		f"{karyo_str}"
		"</span>"
	)

#======================================
#======================================
def flip_sex_token(sex_token: str) -> str:
	"""
	Create a plausible opposite-sex token.
	"""
	if "Y" in sex_token:
		if sex_token == "XY":
			return "XX"
		if sex_token == "XYY":
			return "XXY"
		if sex_token == "XXY":
			return "XXX"
		return "XX"
	if sex_token == "XXX":
		return "XXY"
	if sex_token == "X":
		return "XX"
	return "XY"

#======================================
#======================================
def choose_alt_chromosome(current: str) -> str:
	"""
	Choose an alternate chromosome label.
	"""
	candidates = [str(i) for i in range(1, 23)] + ["X", "Y"]
	random.shuffle(candidates)
	for candidate in candidates:
		if candidate != current:
			return candidate
	return current

#======================================
#======================================
def mutate_aneuploidy_chromosome(features: dict) -> str:
	"""
	Change the chromosome in the first aneuploidy token.
	"""
	aneuploidy_list = list(features.get("aneuploidy", []))
	if len(aneuploidy_list) == 0:
		return ""
	sign = aneuploidy_list[0][0]
	chrom = aneuploidy_list[0][1:]
	new_chrom = choose_alt_chromosome(chrom)
	aneuploidy_list[0] = f"{sign}{new_chrom}"
	new_features = dict(features)
	new_features["aneuploidy"] = aneuploidy_list
	return build_karyotype_from_features(new_features)

#======================================
#======================================
def mutate_aneuploidy_sign(features: dict) -> str:
	"""
	Flip the sign of the first aneuploidy token.
	"""
	aneuploidy_list = list(features.get("aneuploidy", []))
	if len(aneuploidy_list) == 0:
		return ""
	token = aneuploidy_list[0]
	sign = token[0]
	chrom = token[1:]
	new_sign = "-" if sign == "+" else "+"
	aneuploidy_list[0] = f"{new_sign}{chrom}"
	new_features = dict(features)
	new_features["aneuploidy"] = aneuploidy_list
	return build_karyotype_from_features(new_features)

#======================================
#======================================
def mutate_flip_sex(features: dict) -> str:
	"""
	Flip the sex token for a non-mosaic line.
	"""
	new_features = dict(features)
	new_features["sex"] = flip_sex_token(features["sex"])
	return build_karyotype_from_features(new_features)

#======================================
#======================================
def mutate_flip_band_arm(features: dict) -> str:
	"""
	Flip p/q in a deletion or duplication breakpoint.
	"""
	breakpoint = features.get("breakpoint")
	if breakpoint is None:
		return ""
	if breakpoint.startswith("p"):
		new_breakpoint = "q" + breakpoint[1:]
	elif breakpoint.startswith("q"):
		new_breakpoint = "p" + breakpoint[1:]
	else:
		return ""
	new_features = dict(features)
	new_features["breakpoint"] = new_breakpoint
	return build_karyotype_from_features(new_features)

#======================================
#======================================
def mutate_shift_band_number(features: dict) -> str:
	"""
	Shift a band number or sub-band by one step.
	"""
	breakpoint = features.get("breakpoint")
	if breakpoint is None:
		return ""
	if "." in breakpoint:
		prefix, subband = breakpoint.split(".", 1)
		if not subband.isdigit():
			return ""
		current = int(subband)
		new_subband = 1 if current != 1 else 2
		new_breakpoint = f"{prefix}.{new_subband}"
	else:
		if not breakpoint[-1].isdigit():
			return ""
		last_digit = int(breakpoint[-1])
		new_digit = 1 if last_digit != 1 else 2
		new_breakpoint = breakpoint[:-1] + str(new_digit)
	new_features = dict(features)
	new_features["breakpoint"] = new_breakpoint
	return build_karyotype_from_features(new_features)

#======================================
#======================================
def mutate_del_dup(features: dict) -> str:
	"""
	Swap deletion and duplication event types.
	"""
	event_type = features.get("event_type")
	if event_type not in ("deletion", "duplication"):
		return ""
	new_features = dict(features)
	new_features["event_type"] = "duplication" if event_type == "deletion" else "deletion"
	return build_karyotype_from_features(new_features)

#======================================
#======================================
def mutate_translocation_chromosome(features: dict) -> str:
	"""
	Change one chromosome in a translocation.
	"""
	if features.get("event_type") not in (
		"reciprocal_translocation",
		"robertsonian_translocation",
	):
		return ""
	new_features = dict(features)
	new_features["chr_b"] = choose_alt_chromosome(features["chr_b"])
	return build_karyotype_from_features(new_features)

#======================================
#======================================
def mutate_translocation_breakpoints(features: dict) -> str:
	"""
	Swap breakpoints in a reciprocal translocation.
	"""
	if features.get("event_type") != "reciprocal_translocation":
		return ""
	new_features = dict(features)
	band_a = features["band_a"]
	band_b = features["band_b"]
	new_features["band_a"] = band_b
	new_features["band_b"] = band_a
	return build_karyotype_from_features(new_features)

#======================================
#======================================
def mutate_t_to_rob(features: dict) -> str:
	"""
	Convert a reciprocal translocation into a Robertsonian translocation.
	"""
	if features.get("event_type") != "reciprocal_translocation":
		return ""
	new_features = dict(features)
	new_features["event_type"] = "robertsonian_translocation"
	new_features["break_a"] = "q10"
	new_features["break_b"] = "q10"
	return build_karyotype_from_features(new_features)

#======================================
#======================================
def mutate_rob_to_t(features: dict) -> str:
	"""
	Convert a Robertsonian translocation into a reciprocal translocation.
	"""
	if features.get("event_type") != "robertsonian_translocation":
		return ""
	new_features = dict(features)
	new_features["event_type"] = "reciprocal_translocation"
	new_features["band_a"] = features.get("break_a", "q10")
	new_features["band_b"] = features.get("break_b", "q10")
	return build_karyotype_from_features(new_features)

#======================================
#======================================
def build_mosaic_from_lines(lines: list) -> str:
	"""
	Join karyotype lines into a mosaic string.
	"""
	return "/".join(lines)

#======================================
#======================================
def remove_mosaic_format(features: dict) -> str:
	"""
	Return a single abnormal line from a mosaic karyotype.
	"""
	lines = features.get("cell_line_features", [])
	if len(lines) == 0:
		return ""
	abnormal_index = 0
	for i, line_features in enumerate(lines):
		if not is_normal_line(line_features):
			abnormal_index = i
			break
	return build_karyotype_from_features(lines[abnormal_index])

#======================================
#======================================
def mutate_mosaic_line(features: dict, mutator) -> str:
	"""
	Mutate the abnormal line of a mosaic karyotype.
	"""
	lines = features.get("cell_line_features", [])
	if len(lines) == 0:
		return ""
	abnormal_index = 0
	for i, line_features in enumerate(lines):
		if not is_normal_line(line_features):
			abnormal_index = i
			break
	mutated_lines = []
	for i, line_features in enumerate(lines):
		if i == abnormal_index:
			mutated = mutator(line_features)
			if mutated == "":
				return ""
			mutated_lines.append(mutated)
		else:
			mutated_lines.append(build_karyotype_from_features(line_features))
	return build_mosaic_from_lines(mutated_lines)

#======================================
#======================================
def add_mosaic_format(features: dict) -> str:
	"""
	Add a normal line to create a mosaic distractor.
	"""
	sex_token = features.get("sex", "XX")
	normal_sex = "XY" if "Y" in sex_token else "XX"
	normal_features = {
		"total_chromosomes": 46,
		"sex": normal_sex,
		"event_type": "other_or_normal",
	}
	normal_line = build_karyotype_from_features(normal_features)
	return build_mosaic_from_lines([normal_line, build_karyotype_from_features(features)])

#======================================
#======================================
def make_science_distractors(correct_karyo: str, features: dict) -> list:
	"""
	Create biologically meaningful distractor karyotypes.
	"""
	distractors = set()

	if features.get("is_mosaic"):
		distractors.add(remove_mosaic_format(features))
		distractors.add(mutate_mosaic_line(features, mutate_flip_sex))
		distractors.add(mutate_mosaic_line(features, mutate_aneuploidy_chromosome))
	else:
		event_type = features.get("event_type")
		if event_type == "aneuploidy":
			distractors.add(mutate_flip_sex(features))
			distractors.add(mutate_aneuploidy_chromosome(features))
			distractors.add(mutate_aneuploidy_sign(features))
			distractors.add(add_mosaic_format(features))

		if event_type in ("deletion", "duplication"):
			distractors.add(mutate_flip_sex(features))
			distractors.add(mutate_flip_band_arm(features))
			distractors.add(mutate_shift_band_number(features))
			distractors.add(mutate_del_dup(features))

		if event_type == "reciprocal_translocation":
			distractors.add(mutate_flip_sex(features))
			distractors.add(mutate_translocation_chromosome(features))
			distractors.add(mutate_translocation_breakpoints(features))
			distractors.add(mutate_t_to_rob(features))

		if event_type == "robertsonian_translocation":
			distractors.add(mutate_flip_sex(features))
			distractors.add(mutate_translocation_chromosome(features))
			distractors.add(mutate_rob_to_t(features))

	distractors_list = [d for d in distractors if d not in ("", correct_karyo)]
	return distractors_list

#======================================
#======================================
def collect_all_notations(disorders: list) -> list:
	"""
	Collect all notation strings from disorder data.
	"""
	all_notations = []
	for entry in disorders:
		for notation in entry.get("notation", []):
			all_notations.append(notation)
	return all_notations

#======================================
#======================================
def build_distractor_pool(correct_karyo: str, features: dict, disorder_entry: dict, disorders: list) -> list:
	"""
	Assemble a pool of distractor karyotypes.
	"""
	pool = set(make_science_distractors(correct_karyo, features))
	for notation in disorder_entry.get("notation", []):
		if notation != correct_karyo:
			pool.add(notation)
	for notation in collect_all_notations(disorders):
		if notation != correct_karyo:
			pool.add(notation)
	return list(pool)

#======================================
#======================================
def build_stem_description_to_notation(disorder_entry: dict, description: str) -> str:
	"""
	Build a stem that asks for the correct notation.
	"""
	stem = f"A patient has findings consistent with {disorder_entry['name']}."
	caused_by = disorder_entry.get("caused by")
	if caused_by:
		stem += f" The condition is caused by {caused_by}."
	stem += f" The karyotype is best summarized as: {description} Which notation matches this?"
	return stem

#======================================
#======================================
def build_stem_notation_to_description(disorder_entry: dict, karyo_str: str) -> str:
	"""
	Build a stem that asks for the correct description.
	"""
	stem = f"A patient has findings consistent with {disorder_entry['name']}."
	caused_by = disorder_entry.get("caused by")
	if caused_by:
		stem += f" The condition is caused by {caused_by}."
	stem += (
		" The lab report lists the karyotype "
		f"{format_karyotype(karyo_str)}. Which description best summarizes it?"
	)
	return stem

#======================================
#======================================
def write_question_from_entry(N: int, args, disorder_entry: dict, disorders: list) -> str:
	"""
	Create a formatted question from one disorder entry.
	"""
	notations = disorder_entry.get("notation", [])
	if len(notations) == 0:
		return ""

	target_karyo = choose_notation(notations, args.prefer_mosaic)
	target_features = parse_karyotype_to_features(target_karyo)
	description = features_to_science_description(target_features, disorder_entry)

	distractor_pool = build_distractor_pool(target_karyo, target_features, disorder_entry, disorders)
	random.shuffle(distractor_pool)
	distractor_pool = [k for k in distractor_pool if k != target_karyo]

	num_needed = args.num_choices - 1
	distractors = distractor_pool[:num_needed]

	if args.question_mode == "notation_to_description":
		question_text = build_stem_notation_to_description(disorder_entry, target_karyo)
		choices_list = [description]
		for karyo in distractors:
			features = parse_karyotype_to_features(karyo)
			choices_list.append(features_to_science_description(features, disorder_entry))
		answer_text = description
	else:
		question_text = build_stem_description_to_notation(disorder_entry, description)
		choices_list = [format_karyotype(target_karyo)]
		for karyo in distractors:
			choices_list.append(format_karyotype(karyo))
		answer_text = format_karyotype(target_karyo)

	choices_list = list(set(choices_list))
	random.shuffle(choices_list)
	return bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)

#======================================
#======================================
def write_question(N: int, args) -> str:
	"""
	Write one question using the YAML disorder data.
	"""
	disorders = load_disorder_data(args.input_file)
	valid_entries = [entry for entry in disorders if entry.get("notation")]
	if len(valid_entries) == 0:
		raise ValueError("No disorders with notation entries found.")
	entry = random.choice(valid_entries)
	return write_question_from_entry(N, args, entry, disorders)

#=====================
def parse_arguments():
	"""
	Parse command-line arguments for the script.
	"""
	parser = bptools.make_arg_parser(
		description="Generate cytogenetic notation disorder questions."
	)
	parser = bptools.add_choice_args(parser, default=5)
	parser.add_argument(
		'-i', '--input', dest='input_file', default=DATA_FILE,
		help='YAML file containing cytogenetic disorder data.'
	)
	parser.add_argument(
		'--notation-to-description', dest='question_mode',
		action='store_const', const='notation_to_description',
		help='Ask for the best description given a notation.'
	)
	parser.add_argument(
		'--description-to-notation', dest='question_mode',
		action='store_const', const='description_to_notation',
		help='Ask for the notation given a description.'
	)
	parser.set_defaults(question_mode='description_to_notation')
	parser.add_argument(
		'--prefer-mosaic', dest='prefer_mosaic',
		action='store_true', help='Prefer mosaic notations when available.'
	)
	parser.add_argument(
		'--no-prefer-mosaic', dest='prefer_mosaic',
		action='store_false', help='Do not prefer mosaic notations.'
	)
	parser.set_defaults(prefer_mosaic=True)
	args = parser.parse_args()
	return args

#======================================
#======================================
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""
	args = parse_arguments()
	outfile = bptools.make_outfile(f"{args.num_choices}_choices")
	bptools.collect_and_write_questions(write_question, args, outfile)

#======================================
#======================================
if __name__ == '__main__':
	main()

## THE END
