"""
Shared helpers for generating WeBWorK PG/PGML files.
"""

import datetime
import html
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
def contains_html_table(text_string):
	"""
	Return True if text contains HTML table tags.
	"""
	if text_string is None:
		return False
	if not isinstance(text_string, str):
		raise TypeError(f"value is not string: {text_string}")
	return re.search(r'<\s*(table|tr|td)\b', text_string, flags=re.IGNORECASE) is not None

#============================================
def strip_html_tags(text_string, preserve_pgml_wrappers=True):
	"""
	Strip HTML tags while preserving inner text.
	"""
	if text_string is None:
		return ""
	if not isinstance(text_string, str):
		raise TypeError(f"value is not string: {text_string}")
	text_string = re.sub(r'<\s*br\s*/?\s*>', '\n', text_string, flags=re.IGNORECASE)
	if preserve_pgml_wrappers:
		text_string = re.sub(r'(?<!\[)<[^>]+>', '', text_string)
	else:
		text_string = re.sub(r'<[^>]+>', '', text_string)
	return text_string

#============================================
def convert_sub_sup(text_string):
	"""
	Replace <sub> and <sup> HTML tags with Unicode equivalents.
	"""
	if text_string is None:
		return ""
	if not isinstance(text_string, str):
		raise TypeError(f"value is not string: {text_string}")
	subscript_map = str.maketrans(
		"0123456789+-=()aehijklmnoprstuvx",
		"\u2080\u2081\u2082\u2083\u2084\u2085\u2086\u2087\u2088\u2089"
		"\u208A\u208B\u208C\u208D\u208E"
		"\u2090\u2091\u2095\u1d62\u2c7c\u2096\u2097\u2098\u2099\u2092"
		"\u209a\u209b\u209c\u1d63\u209d\u1d64\u2093",
	)
	superscript_map = str.maketrans(
		"0123456789+-=()in",
		"\u2070\u00B9\u00B2\u00B3\u2074\u2075\u2076\u2077\u2078\u2079"
		"\u207A\u207B\u207C\u207D\u207E\u2071\u207F",
	)

	def normalize_sub_sup_token(token_text):
		normalized = html.unescape(token_text)
		normalized = normalized.replace("\u2013", "-")
		normalized = normalized.replace("\u2212", "-")
		return normalized

	def subscript_replace(match):
		normalized = normalize_sub_sup_token(match.group(1))
		return normalized.translate(subscript_map)

	def superscript_replace(match):
		normalized = normalize_sub_sup_token(match.group(1))
		return normalized.translate(superscript_map)

	text_string = re.sub(r'<sub>(.*?)</sub>', subscript_replace, text_string)
	text_string = re.sub(r'<sup>(.*?)</sup>', superscript_replace, text_string)
	return text_string

#============================================
def unescape_html(text_string):
	"""
	Unescape HTML entities into Unicode characters.
	"""
	if text_string is None:
		return ""
	if not isinstance(text_string, str):
		raise TypeError(f"value is not string: {text_string}")
	return html.unescape(text_string)

#============================================
def normalize_nbsp(text_string):
	"""
	Normalize non-breaking spaces to plain spaces.
	"""
	if text_string is None:
		return ""
	if not isinstance(text_string, str):
		raise TypeError(f"value is not string: {text_string}")
	return text_string.replace("\u00a0", " ")

#============================================
def escape_html_text(text_string):
	"""
	Escape plain text for safe HTML output.
	"""
	if text_string is None:
		return ""
	if not isinstance(text_string, str):
		raise TypeError(f"value is not string: {text_string}")
	return html.escape(text_string, quote=False)

#============================================
def sanitize_text_for_html(text_string):
	"""
	Sanitize text for raw HTML output (tags stripped, entities escaped).
	"""
	if text_string is None:
		return ""
	if not isinstance(text_string, str):
		raise TypeError(f"value is not string: {text_string}")
	text_string = convert_sub_sup(text_string)
	text_string = strip_html_tags(text_string, preserve_pgml_wrappers=True)
	text_string = unescape_html(text_string)
	text_string = normalize_nbsp(text_string)
	return escape_html_text(text_string)

#============================================
def build_html_span(text_string, class_name=None, style=None):
	"""
	Build a safe HTML span with escaped text content.
	"""
	if text_string is None:
		text_string = ""
	if not isinstance(text_string, str):
		raise TypeError(f"value is not string: {text_string}")
	attrs = []
	if class_name:
		attrs.append(f"class=\"{class_name}\"")
	if style:
		attrs.append(f"style=\"{style}\"")
	attr_blob = ""
	if len(attrs) > 0:
		attr_blob = " " + " ".join(attrs)
	return f"<span{attr_blob}>{escape_html_text(text_string)}</span>"

#============================================
def normalize_color_value(color_value):
	"""
	Normalize a CSS color value and return (normalized_color, class_name).
	"""
	if color_value is None:
		raise ValueError("color_value is required")
	if not isinstance(color_value, str):
		raise TypeError(f"value is not string: {color_value}")
	value = color_value.strip()
	if value.startswith("#"):
		value = "#" + value[1:].lower()
	elif re.fullmatch(r'[0-9a-fA-F]{6}', value):
		value = "#" + value.lower()
	else:
		value = value.lower()
	class_slug = re.sub(r'[^a-z0-9]+', '-', value.lstrip("#"))
	class_slug = class_slug.strip("-")
	if not class_slug:
		class_slug = "color"
	class_name = f"color-{class_slug}"
	return value, class_name

#============================================
def build_pgml_tag_wrapper(text_string, tag_name="span", class_name=None, style=None):
	"""
	Build a PGML tag wrapper string for a single HTML tag.
	"""
	if text_string is None:
		return ""
	if not isinstance(text_string, str):
		raise TypeError(f"value is not string: {text_string}")
	if not isinstance(tag_name, str):
		raise TypeError("tag_name must be a string")
	attrs = []
	if class_name:
		attrs.append(f"class => \"{class_name}\"")
	if style:
		attrs.append(f"style => \"{style}\"")
	if len(attrs) == 0:
		return text_string
	attr_blob = ", ".join(attrs)
	return f"[<{text_string}>]{{[\"{tag_name}\", {attr_blob}]}}{{[\"\",\"\"]}}"

#============================================
def extract_strict_color_span(text_string):
	"""
	Extract a strict color span with optional strong wrappers.

	Returns (prefix, inner_text, suffix, color_value, is_bold) or None.
	"""
	if text_string is None:
		return None
	if not isinstance(text_string, str):
		raise TypeError(f"value is not string: {text_string}")
	span_match = re.search(r'<span\b[^>]*>.*?</span>', text_string,
		flags=re.IGNORECASE | re.DOTALL)
	if span_match is None:
		return None
	if re.search(r'<span\b[^>]*>.*?</span>.*<span\b', text_string,
		flags=re.IGNORECASE | re.DOTALL):
		return None
	prefix = text_string[:span_match.start()]
	suffix = text_string[span_match.end():]
	span_block = span_match.group(0)

	is_bold = False
	strong_prefix = re.search(r'<strong>\s*$', prefix, flags=re.IGNORECASE)
	strong_suffix = re.search(r'^\s*</strong>', suffix, flags=re.IGNORECASE)
	if strong_prefix and strong_suffix:
		is_bold = True
		prefix = prefix[:strong_prefix.start()]
		suffix = suffix[strong_suffix.end():]

	attr_match = re.search(r'<span\b([^>]*)>', span_block, flags=re.IGNORECASE)
	if attr_match is None:
		return None
	attrs = attr_match.group(1)
	style_match = re.search(
		r'style\s*=\s*(?P<quote>[\"\'])(?P<style>.*?)(?P=quote)',
		attrs,
		flags=re.IGNORECASE | re.DOTALL,
	)
	if style_match is None:
		style_match = re.search(
			r'style\s*=\s*([^>]+)$',
			attrs,
			flags=re.IGNORECASE | re.DOTALL,
		)
	if style_match is None:
		return None
	style_text = style_match.groupdict().get("style") or style_match.group(1)
	style_text = style_text.strip()
	style_text = style_text.rstrip(";")
	if not style_text:
		return None
	parts = [part.strip() for part in style_text.split(";") if part.strip()]
	if len(parts) != 1:
		return None
	if ":" not in parts[0]:
		return None
	prop, value = parts[0].split(":", 1)
	if prop.strip().lower() != "color":
		return None
	color_value = value.strip()
	if not color_value:
		return None

	inner = re.sub(r'^<span\b[^>]*>', '', span_block, flags=re.IGNORECASE)
	inner = re.sub(r'</span>\s*$', '', inner, flags=re.IGNORECASE)

	inner_strong = re.fullmatch(
		r'\s*<strong>(.*?)</strong>\s*',
		inner,
		flags=re.IGNORECASE | re.DOTALL,
	)
	if inner_strong is not None:
		is_bold = True
		inner = inner_strong.group(1)

	inner = convert_sub_sup(inner)
	inner = unescape_html(inner)
	inner = normalize_nbsp(inner)
	if re.search(r'<[^>]+>', inner):
		return None

	return prefix, inner, suffix, color_value, is_bold

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
