"""
Shared helpers for generating WeBWorK PG/PGML files.
"""

import datetime
import re

#============================================
def get_yaml_value(yaml_data, *keys):
	"""
	Return the first non-empty value for the provided keys.
	"""
	for key in keys:
		if key in yaml_data and yaml_data.get(key) is not None:
			return yaml_data.get(key)
	return None

#============================================
def escape_perl_string(text_string):
	"""
	Escape text for a Perl single-quoted string and normalize newlines.

	Notes:
	- Safe optimization: early return if no escaping is needed.
	- This function is intentionally not idempotent. Call it once on raw text.
	"""
	if text_string is None:
		return ""
	if not isinstance(text_string, str):
		raise TypeError(f"value is not string: {text_string}")

	if ("\\" not in text_string
		and "'" not in text_string
		and "\r" not in text_string
		and "\n" not in text_string):
		return text_string

	text_string = text_string.replace("\r\n", "\n")
	text_string = text_string.replace("\r", "\n")
	text_string = text_string.replace("\\", "\\\\")
	text_string = text_string.replace("'", "\\'")
	text_string = text_string.replace("\n", "\\n")
	return text_string

def perl_literal(value, indent=""):
	"""
	Convert a Python value to a Perl literal string.
	"""
	if isinstance(value, dict):
		return perl_hash_ref(value, indent)
	if isinstance(value, (list, tuple)):
		return perl_array_ref(value, indent)
	if isinstance(value, bool):
		return "1" if value else "0"
	if value is None:
		return "''"
	if isinstance(value, (int, float)):
		return str(value)
	if isinstance(value, str):
		return "'" + escape_perl_string(value) + "'"
	raise TypeError(f"unsupported perl literal type: {type(value)}")

#============================================
def perl_array_ref(values, indent=""):
	"""
	Convert a list/tuple into a Perl array reference.
	"""
	if len(values) == 0:
		return "[]"
	inner_indent = indent + "  "
	lines = ["["]
	for item in values:
		lines.append(f"{inner_indent}{perl_literal(item, inner_indent)},")
	lines.append(f"{indent}]")
	return "\n".join(lines)

#============================================
def perl_hash_ref(mapping, indent=""):
	"""
	Convert a dict into a Perl hash reference.
	"""
	if len(mapping) == 0:
		return "{}"
	inner_indent = indent + "  "
	lines = ["{"]
	for key, value in mapping.items():
		key_text = escape_perl_string(str(key))
		value_text = perl_literal(value, inner_indent)
		lines.append(f"{inner_indent}'{key_text}' => {value_text},")
	lines.append(f"{indent}}}")
	return "\n".join(lines)

#============================================
def perl_array(name, values):
	"""
	Convert a list/tuple into a Perl array assignment.
	"""
	text = ""
	text += f"@{name} = (\n"
	for item in values:
		text += f"  {perl_literal(item, '  ')},\n"
	text += ");\n"
	text += "\n"
	return text

#============================================
def perl_hash(name, mapping):
	"""
	Convert a dict into a Perl hash assignment.
	"""
	text = ""
	text += f"%{name} = (\n"
	for key, value in mapping.items():
		key_text = escape_perl_string(str(key))
		value_text = perl_literal(value, "  ")
		text += f"  '{key_text}' => {value_text},\n"
	text += ");\n"
	text += "\n"
	return text

#============================================
def sanitize_header_text(text_string):
	"""
	Sanitize header text to plain ASCII without HTML tags.
	"""
	if not isinstance(text_string, str):
		raise TypeError(f"value is not string: {text_string}")
	text_string = re.sub(r'<[^>]+>', '', text_string)
	text_string = text_string.replace("\r", " ")
	text_string = text_string.replace("\n", " ")
	text_string = " ".join(text_string.split())
	text_string = text_string.encode("ascii", "ignore").decode("ascii")
	return text_string

#============================================
def normalize_keywords(raw_keywords):
	"""
	Normalize keywords to a list of strings.
	"""
	if raw_keywords is None:
		return []
	if isinstance(raw_keywords, list):
		keywords = raw_keywords
	elif isinstance(raw_keywords, str):
		if "," in raw_keywords:
			keywords = [item.strip() for item in raw_keywords.split(",")]
		else:
			keywords = [raw_keywords.strip()]
	else:
		raise TypeError("keywords must be a list or string")
	normalized = []
	for keyword in keywords:
		if not keyword:
			continue
		if not isinstance(keyword, str):
			raise TypeError(f"keyword is not string: {keyword}")
		normalized.append(keyword)
	return normalized

#============================================
def build_opl_header_lines(yaml_data, default_description=None, fallback_keywords=None):
	"""
	Build a complete OPL-style header block.
	"""
	description_text = get_yaml_value(yaml_data, 'description', 'DESCRIPTION')
	if description_text is None:
		description_text = default_description or "Matching question."
	description_text = sanitize_header_text(str(description_text))

	keywords = normalize_keywords(get_yaml_value(yaml_data, 'keywords', 'KEYWORDS'))
	if fallback_keywords is None:
		fallback_keywords = []
	if len(keywords) == 0:
		for candidate in fallback_keywords:
			if candidate:
				keywords.append(candidate)
	keywords = [sanitize_header_text(str(keyword)) for keyword in keywords if keyword]

	dbsubject = sanitize_header_text(str(get_yaml_value(yaml_data, 'dbsubject', 'DBsubject') or ''))
	dbchapter = sanitize_header_text(str(get_yaml_value(yaml_data, 'dbchapter', 'DBchapter') or ''))
	dbsection = sanitize_header_text(str(get_yaml_value(yaml_data, 'dbsection', 'DBsection') or ''))

	# Use current date if not specified
	date_text = get_yaml_value(yaml_data, 'date', 'Date')
	if not date_text:
		date_text = datetime.date.today().strftime('%Y-%m-%d')
	date_text = sanitize_header_text(str(date_text))

	# Use default author if not specified
	author_text = get_yaml_value(yaml_data, 'author', 'Author')
	if not author_text:
		author_text = 'Neil R. Voss'
	author_text = sanitize_header_text(str(author_text))

	# Use default institution if not specified
	institution_text = get_yaml_value(yaml_data, 'institution', 'Institution')
	if not institution_text:
		institution_text = 'Roosevelt University'
	institution_text = sanitize_header_text(str(institution_text))
	title_text = sanitize_header_text(str(get_yaml_value(yaml_data, 'titletext1', 'TitleText1') or ''))
	edition_text = sanitize_header_text(str(get_yaml_value(yaml_data, 'editiontext1', 'EditionText1') or ''))
	author_text_1 = sanitize_header_text(str(get_yaml_value(yaml_data, 'authortext1', 'AuthorText1') or ''))
	section_text = sanitize_header_text(str(get_yaml_value(yaml_data, 'section1', 'Section1') or ''))
	problem_text = sanitize_header_text(str(get_yaml_value(yaml_data, 'problem1', 'Problem1') or ''))

	header_lines = []
	header_lines.append("## DESCRIPTION")
	header_lines.append(f"## {description_text}")
	header_lines.append("## ENDDESCRIPTION")
	if len(keywords) == 0:
		header_lines.append("## KEYWORDS('')")
	else:
		escaped_keywords = []
		for keyword in keywords:
			escaped_keywords.append(escape_perl_string(keyword))
		keyword_blob = "','".join(escaped_keywords)
		header_lines.append(f"## KEYWORDS('{keyword_blob}')")
	header_lines.append(f"## DBsubject('{escape_perl_string(dbsubject)}')")
	header_lines.append(f"## DBchapter('{escape_perl_string(dbchapter)}')")
	header_lines.append(f"## DBsection('{escape_perl_string(dbsection)}')")
	header_lines.append(f"## Date('{escape_perl_string(date_text)}')")
	header_lines.append(f"## Author('{escape_perl_string(author_text)}')")
	header_lines.append(f"## Institution('{escape_perl_string(institution_text)}')")
	header_lines.append(f"## TitleText1('{escape_perl_string(title_text)}')")
	header_lines.append(f"## EditionText1('{escape_perl_string(edition_text)}')")
	header_lines.append(f"## AuthorText1('{escape_perl_string(author_text_1)}')")
	header_lines.append(f"## Section1('{escape_perl_string(section_text)}')")
	header_lines.append(f"## Problem1('{escape_perl_string(problem_text)}')")
	return header_lines

#============================================
def build_opl_header(yaml_data, default_description=None, fallback_keywords=None):
	"""
	Return a complete OPL-style header block as a string.
	"""
	lines = build_opl_header_lines(
		yaml_data,
		default_description=default_description,
		fallback_keywords=fallback_keywords,
	)
	return "\n".join(lines) + "\n"
