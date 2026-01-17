#!/usr/bin/env python3

"""
Shared helpers for generating WeBWorK PG/PGML files.
"""

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
def escape_perl_single_quoted(text_string):
	"""
	Escape text for a Perl single-quoted string.
	"""
	if not isinstance(text_string, str):
		raise TypeError(f"value is not string: {text_string}")
	text_string = text_string.replace("\\", "\\\\")
	text_string = text_string.replace("'", "\\'")
	return text_string

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
	date_text = sanitize_header_text(str(get_yaml_value(yaml_data, 'date', 'Date') or ''))
	author_text = sanitize_header_text(str(get_yaml_value(yaml_data, 'author', 'Author') or ''))
	institution_text = sanitize_header_text(str(get_yaml_value(yaml_data, 'institution', 'Institution') or ''))
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
			escaped_keywords.append(escape_perl_single_quoted(keyword))
		keyword_blob = "','".join(escaped_keywords)
		header_lines.append(f"## KEYWORDS('{keyword_blob}')")
	header_lines.append(f"## DBsubject('{escape_perl_single_quoted(dbsubject)}')")
	header_lines.append(f"## DBchapter('{escape_perl_single_quoted(dbchapter)}')")
	header_lines.append(f"## DBsection('{escape_perl_single_quoted(dbsection)}')")
	header_lines.append(f"## Date('{escape_perl_single_quoted(date_text)}')")
	header_lines.append(f"## Author('{escape_perl_single_quoted(author_text)}')")
	header_lines.append(f"## Institution('{escape_perl_single_quoted(institution_text)}')")
	header_lines.append(f"## TitleText1('{escape_perl_single_quoted(title_text)}')")
	header_lines.append(f"## EditionText1('{escape_perl_single_quoted(edition_text)}')")
	header_lines.append(f"## AuthorText1('{escape_perl_single_quoted(author_text_1)}')")
	header_lines.append(f"## Section1('{escape_perl_single_quoted(section_text)}')")
	header_lines.append(f"## Problem1('{escape_perl_single_quoted(problem_text)}')")
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
