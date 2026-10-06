#!/usr/bin/env python3

"""Advisory checker for student-facing question text in Blackboard BBQ files.

This is a heuristic aid, never a pass/fail gate. It flags mechanical testwiseness
cues and text slips so a reviewer can look closer. Many findings are fine on
inspection, and a clean report does not prove an item is well written. The script
always exits 0.

Input is one or more BBQ text upload files: one question per line, tab separated
(for example `MC<TAB>stem<TAB>choice<TAB>Correct<TAB>choice<TAB>Incorrect ...`).

Text normalization before checks: elements hidden with `display:none` and the
`font-size: 1px` anti-cheat hidden terms are removed, the leading CRC tag paragraph
(`<p>a4e3_61c6</p>`) is removed, remaining tags are stripped (block tags such as
`<p>` act as a word boundary), HTML entities are unescaped, and whitespace is
collapsed for comparisons. Doubled spaces are detected before collapsing.

Checks (each finding names the file, question number, check id, and an excerpt):

- K1 longest key: for MC items with one key, is the key strictly the longest
  choice by character count? The per-file rate is printed next to the chance rate
  (mean of 1/number_of_choices). A per-item finding needs the key to be at least
  1.3x the longest distractor.
- K2 hedge/absolute asymmetry: the share of choices that contain a hedge word
  (commonly, often, may, can, ...) or an absolute word (always, never, only, all,
  ...), for keys vs distractors across the file. Items with a negated stem
  (NOT, EXCEPT, false, incorrect) are pooled apart from affirmative stems, and in
  that pool the distractors are the true statements. A file-level finding needs at
  least 5 items in the pool and a gap of at least 25 percentage points, in the
  direction a test-wise student exploits: hedges on the true statements or
  absolutes on the false statements.
- K3 key-word echo: content words (5+ letters, not stopwords) shared by the stem
  and the key but absent from every distractor. For MAT lines, words shared by a
  prompt and its matched answer but absent from the other answers.
- K4 article slip: "a" before a vowel letter, "an" before a consonant letter, with
  exceptions for vowel letters sounded as consonants (one, uni, use, eu, ur, UV) and
  consonant letters sounded as vowels (hour, X-linked, MRI, mRNA).
- K5 spacing: doubled spaces, a period glued to the next capital letter
  ("hh.A pea"), and a space before ? . , ; or :.
- K6 unit mismatch: the stem uses a volume, mass, or length unit that never
  appears in the choices while the choices use another unit of the same family.
- K7 generic lead-ins: "best describes", "Which of the following best",
  "Which statement best".
"""

# Standard Library
import os
import re
import html
import argparse
import collections
import dataclasses

CHECK_IDS = ('K1', 'K2', 'K3', 'K4', 'K5', 'K6', 'K7')

# K1: key must be this many times the longest distractor to earn a per-item finding
K1_MARGIN = 1.3
# K2: minimum items in a pool, and minimum gap in share of choices, for a finding
K2_MIN_ITEMS = 5
K2_RATE_GAP = 0.25

# marks an inline tag boundary in text kept for the doubled-space check
INLINE_MARK = '\x00'
# a block tag acts as a line break
BLOCK_MARK = '\n'
BLOCK_TAGS = frozenset((
	'p', 'div', 'br', 'li', 'ul', 'ol', 'tr', 'td', 'th', 'table', 'blockquote',
	'pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
))

# regex hex escapes for a double quote and a single quote
QUOTE = r'[\x22\x27]'
NOT_QUOTE = r'[^\x22\x27]*'
CRC_TAG_RE = re.compile(r'^\s*<p>[0-9a-fA-F]{4}_[0-9a-fA-F]{4}</p>\s*')
TAG_RE = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>')
# letter prefix that the BBQ writer places inside the no-click div ("A. text")
CHOICE_PREFIX_RE = re.compile(r'^(\s*<div\b[^>]*>)\s*[A-Z]\.\s+')

#============================================
def build_hidden_regex(style_pattern: str) -> re.Pattern:
	"""Build a regex for a whole element whose style attribute matches a pattern.

	Args:
		style_pattern: Regex for the style declaration that marks the element hidden.

	Returns:
		re.Pattern: Pattern matching the element from open tag through close tag.
	"""
	pattern = r'<(\w+)\b[^>]*style\s*=\s*' + QUOTE + NOT_QUOTE + style_pattern
	pattern += NOT_QUOTE + QUOTE + r'[^>]*>.*?</\1\s*>'
	compiled = re.compile(pattern, re.IGNORECASE | re.DOTALL)
	return compiled


# elements hidden outright
HIDDEN_NONE_RE = build_hidden_regex(r'display\s*:\s*none')
# anti-cheat hidden terms take the place of a space between two words
HIDDEN_TERM_RE = build_hidden_regex(r'font-size\s*:\s*1px')

HEDGE_RE = re.compile(
	r'\b(?:commonly|often|usually|typically|generally|frequently|may|might|can|tend|tends)\b',
	re.IGNORECASE,
)
ABSOLUTE_RE = re.compile(
	r'\b(?:always|never|only|all|none|every|completely|entirely)\b', re.IGNORECASE,
)
NEGATED_CASE_RE = re.compile(r'\b(?:NOT|EXCEPT)\b')
NEGATED_ANY_RE = re.compile(r'\b(?:false|incorrect|untrue|least likely)\b', re.IGNORECASE)
LEAD_IN_RE = re.compile(
	r'which of the following best|which statement best|best describes', re.IGNORECASE,
)

STOPWORDS = frozenset((
	'about', 'above', 'after', 'again', 'against', 'among', 'answer', 'because', 'before',
	'being', 'below', 'between', 'choice', 'correct', 'could', 'during', 'either', 'every',
	'false', 'first', 'following', 'having', 'incorrect', 'other', 'others', 'should',
	'since', 'statement', 'statements', 'their', 'there', 'these', 'those', 'through',
	'under', 'until', 'where', 'whether', 'which', 'while', 'within', 'without', 'would',
))

# an article, then the word it modifies; capital A only counts at a sentence start
ARTICLE_RE = re.compile(r"(?<![\w'-])([Aa][Nn]?)\s+([A-Za-z][A-Za-z0-9'-]*)")
# words that start with a vowel letter but a consonant sound
A_EXCEPTIONS = ('one', 'once', 'uni', 'use', 'usu', 'eu', 'ur', 'ubi', 'ut', 'uv', 'ew')
# words that start with a consonant letter but a vowel sound
AN_EXCEPTIONS = ('hour', 'honest', 'honor', 'honour', 'heir', 'herb', 'hfr')

# unit families: written form -> canonical form (micro sign escapes keep source ASCII)
UNIT_FAMILIES = {
	'volume': {
		'L': 'L', 'l': 'L', 'mL': 'mL', 'ml': 'mL', 'uL': 'uL', 'ul': 'uL',
		'\xb5L': 'uL', '\xb5l': 'uL', '&micro;L': 'uL', '&micro;l': 'uL',
	},
	'mass': {
		'g': 'g', 'kg': 'kg', 'mg': 'mg', 'ng': 'ng', 'pg': 'pg', 'ug': 'ug',
		'\xb5g': 'ug', '&micro;g': 'ug',
	},
	'DNA length': {'bp': 'bp', 'kb': 'kb', 'kbp': 'kb', 'Mb': 'Mb', 'Gb': 'Gb'},
	'length': {
		'm': 'm', 'cm': 'cm', 'mm': 'mm', 'nm': 'nm', 'km': 'km', 'um': 'um',
		'\xb5m': 'um', '&micro;m': 'um',
	},
}

#============================================
@dataclasses.dataclass
class Field:
	"""One cleaned text field of a question.

	Attributes:
		marked: Entity-unescaped text with tag boundaries marked, for the spacing check.
		plain: Whitespace-collapsed text for comparisons.
	"""
	marked: str
	plain: str

#============================================
@dataclasses.dataclass
class Item:
	"""One parsed BBQ question.

	Attributes:
		line_no: Physical line number in the file.
		kind: BBQ type such as MC, MA, MAT, FIB, NUM, ORD.
		stem: Cleaned question stem.
		choices: MC/MA choices or MAT answers.
		correct: MC/MA key flags aligned with choices (empty otherwise).
		prompts: MAT prompts aligned with choices.
		steps: ORD steps.
	"""
	line_no: int
	kind: str
	stem: Field
	choices: list
	correct: list
	prompts: list
	steps: list

#============================================
@dataclasses.dataclass
class Finding:
	"""One advisory finding; line_no 0 marks a file-level finding."""
	line_no: int
	check: str
	message: str

#============================================
def build_unit_regex(units: dict) -> re.Pattern:
	"""Build a regex for a number followed by any written form of a unit.

	Args:
		units: Mapping of written unit form to canonical form.

	Returns:
		re.Pattern: Pattern whose group 1 is the written unit.
	"""
	names = sorted(units, key=len, reverse=True)
	alternation = '|'.join(re.escape(name) for name in names)
	pattern = r'(?<![\w.])\d[\d,]*(?:\.\d+)?[\s-]?(' + alternation + r')(?!\w)'
	compiled = re.compile(pattern)
	return compiled


UNIT_REGEXES = {name: build_unit_regex(units) for name, units in UNIT_FAMILIES.items()}

#============================================
def hidden_term_replacement(match: re.Match) -> str:
	"""Replace a hidden anti-cheat term with a space only between two lowercase letters.

	The anti-cheat inserter swaps a space between lowercase words for the hidden
	term, so removing the term must restore that space.
	"""
	before = match.string[max(match.start() - 1, 0):match.start()]
	after = match.string[match.end():match.end() + 1]
	glued = re.fullmatch(r'[a-z]', before) and re.fullmatch(r'[a-z]', after)
	replacement = ' ' if glued else ''
	return replacement

#============================================
def tag_marker(match: re.Match) -> str:
	"""Replace a tag with a block or inline boundary mark."""
	name = match.group(2).lower()
	marker = BLOCK_MARK if name in BLOCK_TAGS else INLINE_MARK
	return marker

#============================================
def clean_field(raw_html: str) -> Field:
	"""Normalize one HTML field into marked and plain text.

	Args:
		raw_html: Field text as written in the BBQ file.

	Returns:
		Field: Text with hidden elements and tags removed and entities unescaped.
	"""
	text = HIDDEN_NONE_RE.sub('', raw_html)
	text = HIDDEN_TERM_RE.sub(hidden_term_replacement, text)
	text = TAG_RE.sub(tag_marker, text)
	marked = html.unescape(text)
	plain = re.sub(r'\s+', ' ', marked.replace(INLINE_MARK, '')).strip()
	field = Field(marked=marked, plain=plain)
	return field

#============================================
def clean_choice(raw_html: str) -> Field:
	"""Normalize a choice, dropping the letter prefix the BBQ writer adds inside a div."""
	stripped = CHOICE_PREFIX_RE.sub(r'\1', raw_html)
	field = clean_field(stripped)
	return field

#============================================
def parse_line(line_no: int, line: str) -> Item | None:
	"""Parse one BBQ line into an Item.

	Args:
		line_no: Physical line number.
		line: Tab-separated BBQ line.

	Returns:
		Item | None: The parsed item, or None when the line layout is malformed.
	"""
	parts = line.rstrip('\r\n').split('\t')
	if len(parts) < 2:
		return None
	kind = parts[0].strip().upper()
	stem = clean_field(CRC_TAG_RE.sub('', parts[1]))
	rest = parts[2:]
	item = Item(line_no, kind, stem, [], [], [], [])
	if kind in ('MC', 'MA'):
		flags = [flag.strip().lower() for flag in rest[1::2]]
		if len(rest) % 2 != 0 or any(flag not in ('correct', 'incorrect') for flag in flags):
			return None
		item.choices = [clean_choice(choice) for choice in rest[0::2]]
		item.correct = [flag == 'correct' for flag in flags]
	elif kind == 'MAT':
		if len(rest) % 2 != 0:
			return None
		item.prompts = [clean_field(prompt) for prompt in rest[0::2]]
		item.choices = [clean_field(answer) for answer in rest[1::2]]
	elif kind == 'ORD':
		item.steps = [clean_field(step) for step in rest]
	return item

#============================================
def read_items(path: str) -> tuple[list, int]:
	"""Read every item from a BBQ file.

	Args:
		path: BBQ text file.

	Returns:
		tuple: (items, number of malformed non-blank lines skipped).
	"""
	items = []
	skipped = 0
	with open(path, 'r', encoding='utf-8', errors='replace') as handle:
		for line_no, line in enumerate(handle, start=1):
			if line.strip() == '':
				continue
			item = parse_line(line_no, line)
			if item is None:
				skipped += 1
			else:
				items.append(item)
	return items, skipped

#============================================
def shorten(text: str, width: int = 60) -> str:
	"""Shorten text for an excerpt and escape non-ASCII characters as HTML references."""
	if len(text) > width:
		text = text[:width - 3] + '...'
	ascii_text = text.encode('ascii', 'xmlcharrefreplace').decode('ascii')
	return ascii_text

#============================================
def context_excerpt(text: str, start: int, end: int, radius: int = 24) -> str:
	"""Return the text around a match, with ellipses where it was cut."""
	left = text[max(start - radius, 0):start]
	right = text[end:end + radius]
	prefix = '...' if start - radius > 0 else ''
	suffix = '...' if end + radius < len(text) else ''
	excerpt = prefix + left + '[' + text[start:end] + ']' + right + suffix
	return shorten(excerpt, 4 * radius + 10)

#============================================
def text_fields(item: Item) -> list:
	"""List (label, Field) pairs for every prose field of an item."""
	fields = [('stem', item.stem)]
	for i, prompt in enumerate(item.prompts):
		fields.append((f'prompt {i + 1}', prompt))
	for i, choice in enumerate(item.choices):
		label = f'answer {i + 1}' if item.kind == 'MAT' else f'choice {chr(65 + i)}'
		fields.append((label, choice))
	for i, step in enumerate(item.steps):
		fields.append((f'step {i + 1}', step))
	return fields

#============================================
def key_length_pair(item: Item) -> tuple[int, int] | None:
	"""Return (key length, longest distractor length) for a single-key MC item."""
	if item.kind != 'MC' or len(item.choices) < 2 or sum(item.correct) != 1:
		return None
	lengths = [len(choice.plain) for choice in item.choices]
	key_length = lengths[item.correct.index(True)]
	distractors = [n for n, is_key in zip(lengths, item.correct) if not is_key]
	pair = (key_length, max(distractors))
	return pair

#============================================
def check_k1(item: Item) -> list:
	"""K1: the key is the longest choice by a clear margin."""
	pair = key_length_pair(item)
	if pair is None:
		return []
	key_length, other_length = pair
	if other_length == 0 or key_length < K1_MARGIN * other_length:
		return []
	ratio = key_length / other_length
	message = f'key is longest: {key_length} chars vs {other_length} next ({ratio:.2f}x)'
	return [Finding(item.line_no, 'K1', message)]

#============================================
def content_words(text: str) -> set:
	"""Return lowercase words of 5+ letters that are not stopwords."""
	words = re.findall(r'[a-z]+', text.lower())
	kept = {word for word in words if len(word) >= 5 and word not in STOPWORDS}
	return kept

#============================================
def check_k3(item: Item) -> list:
	"""K3: words echoed between the stem and the key only (or a MAT prompt and answer)."""
	findings = []
	if item.kind in ('MC', 'MA') and any(item.correct) and not all(item.correct):
		key_words = set()
		distractor_words = set()
		for choice, is_key in zip(item.choices, item.correct):
			words = content_words(choice.plain)
			if is_key:
				key_words |= words
			else:
				distractor_words |= words
		echo = (content_words(item.stem.plain) & key_words) - distractor_words
		if echo:
			message = f'stem and key share, absent from distractors: {", ".join(sorted(echo))}'
			findings.append(Finding(item.line_no, 'K3', message))
	elif item.kind == 'MAT' and len(item.choices) >= 2:
		answer_words = [content_words(answer.plain) for answer in item.choices]
		for i, prompt in enumerate(item.prompts):
			others = set().union(*(w for j, w in enumerate(answer_words) if j != i))
			echo = (content_words(prompt.plain) & answer_words[i]) - others
			if echo:
				message = f'prompt {i + 1} "{shorten(prompt.plain, 30)}" shares '
				message += f'{", ".join(sorted(echo))} with its answer only'
				findings.append(Finding(item.line_no, 'K3', message))
	return findings

#============================================
def at_sentence_start(prefix: str) -> bool:
	"""True when text before a word is empty or ends a sentence."""
	stripped = prefix.rstrip()
	starts = stripped == '' or stripped[-1] in '.?!:'
	return starts

#============================================
def is_a_slip(word: str) -> bool:
	"""True when 'a' precedes a word that starts with a vowel sound."""
	# UV, UGA, U-shaped: the letter U sounds like "you"
	if re.match(r'U(?![a-z])', word):
		return False
	# letter names with a vowel sound: A-site, ATP, E. coli, OH group
	if re.match(r'[AEIOU](?![a-z])', word):
		return True
	# consonant letter names sounded with a vowel: F1, X-linked, S phase
	if re.match(r'[FHLMNRSX](?:$|-|\d)', word):
		return True
	if word[0].lower() not in 'aeiou':
		return False
	slip = not word.lower().startswith(A_EXCEPTIONS)
	return slip

#============================================
def is_an_slip(word: str) -> bool:
	"""True when 'an' precedes a word that starts with a consonant sound."""
	if word[0].lower() in 'aeiou':
		return False
	# letter name or acronym: X-linked, MRI, F1
	if re.match(r'[A-Z](?![a-z])', word):
		return False
	# lowercase prefix on an acronym: mRNA, siRNA, mtDNA
	if re.match(r'[a-z]{1,3}[A-Z]', word):
		return False
	slip = not word.lower().startswith(AN_EXCEPTIONS)
	return slip

#============================================
def check_k4(item: Item) -> list:
	"""K4: 'a' before a vowel letter or 'an' before a consonant letter."""
	findings = []
	for label, field in text_fields(item):
		for match in ARTICLE_RE.finditer(field.plain):
			article = match.group(1)
			word = match.group(2)
			if article not in ('a', 'A', 'an', 'An'):
				continue
			if article[0] == 'A' and not at_sentence_start(field.plain[:match.start()]):
				continue
			is_an = article.lower() == 'an'
			slip = is_an_slip(word) if is_an else is_a_slip(word)
			if slip:
				suggestion = 'a' if is_an else 'an'
				excerpt = context_excerpt(field.plain, match.start(), match.end())
				message = f'{label}: "{article} {word}" -> use "{suggestion}": {excerpt}'
				findings.append(Finding(item.line_no, 'K4', message))
	return findings

#============================================
def spacing_slips(field: Field) -> list:
	"""Find spacing slips in one field.

	Args:
		field: Cleaned field.

	Returns:
		list: (description, excerpt) pairs.
	"""
	slips = []
	# doubled spaces: tag boundaries break a run, a pure non-breaking run is deliberate
	for match in re.finditer('[ \xa0]{2,}', field.marked):
		if ' ' in match.group():
			left = field.marked[max(match.start() - 20, 0):match.start()]
			right = field.marked[match.end():match.end() + 20]
			shown = (left + '<spaces>' + right).replace(INLINE_MARK, '').replace(BLOCK_MARK, ' ')
			slips.append(('doubled space', shorten(shown.strip(), 70)))
	for match in re.finditer(r'[a-z0-9]\.[A-Z]', field.plain):
		excerpt = context_excerpt(field.plain, match.start(), match.end())
		slips.append(('no space after period', excerpt))
	# a ratio such as 3 : 1, a decimal such as .5, and an ellipsis are not slips
	for match in re.finditer(r'\s(?:[?,;]|\.(?![.\d])|:(?!\s*\d))', field.plain):
		excerpt = context_excerpt(field.plain, match.start(), match.end())
		slips.append(('space before punctuation', excerpt))
	return slips

#============================================
def check_k5(item: Item) -> list:
	"""K5: doubled spaces, missing space after a period, space before punctuation."""
	findings = []
	for label, field in text_fields(item):
		for description, excerpt in spacing_slips(field):
			findings.append(Finding(item.line_no, 'K5', f'{label}: {description}: {excerpt}'))
	return findings

#============================================
def found_units(text: str) -> dict:
	"""Map each unit family to the canonical units written with a number in the text."""
	found = {}
	for family, regex in UNIT_REGEXES.items():
		canonical = {UNIT_FAMILIES[family][written] for written in regex.findall(text)}
		if canonical:
			found[family] = canonical
	return found

#============================================
def check_k6(item: Item) -> list:
	"""K6: the stem uses a unit that the choices never use, in a unit family the choices use."""
	if item.kind not in ('MC', 'MA'):
		return []
	findings = []
	stem_units = found_units(item.stem.plain)
	choice_units = found_units(' | '.join(choice.plain for choice in item.choices))
	for family, stem_set in stem_units.items():
		choice_set = choice_units.get(family, set())
		missing = stem_set - choice_set
		if missing and choice_set:
			message = f'{family}: stem uses {", ".join(sorted(missing))}; '
			message += f'choices use {", ".join(sorted(choice_set))}'
			findings.append(Finding(item.line_no, 'K6', message))
	return findings

#============================================
def check_k7(item: Item) -> list:
	"""K7: generic lead-in phrases in the stem."""
	findings = []
	for match in LEAD_IN_RE.finditer(item.stem.plain):
		excerpt = context_excerpt(item.stem.plain, match.start(), match.end())
		findings.append(Finding(item.line_no, 'K7', f'generic lead-in: {excerpt}'))
	return findings

#============================================
def item_findings(item: Item) -> list:
	"""Run every per-item check on one item."""
	findings = []
	for check in (check_k1, check_k3, check_k4, check_k5, check_k6, check_k7):
		findings += check(item)
	return findings

#============================================
def k1_summary(items: list) -> tuple[int, int, float]:
	"""Return (items with the key strictly longest, single-key MC items, chance rate)."""
	longest = 0
	total = 0
	chance_sum = 0.0
	for item in items:
		pair = key_length_pair(item)
		if pair is None:
			continue
		total += 1
		chance_sum += 1 / len(item.choices)
		if pair[0] > pair[1]:
			longest += 1
	chance = chance_sum / total if total else 0.0
	return longest, total, chance

#============================================
def is_negated(stem: str) -> bool:
	"""True when the stem asks for the false statement (NOT, EXCEPT, false, ...)."""
	negated = bool(NEGATED_CASE_RE.search(stem) or NEGATED_ANY_RE.search(stem))
	return negated

#============================================
def k2_tally(items: list) -> dict:
	"""Count choices holding hedge and absolute words, split by pool and by key side.

	Args:
		items: Parsed items.

	Returns:
		dict: Pool name ('affirmative' or 'negated') to a Counter of tallies.
	"""
	pools = {'affirmative': collections.Counter(), 'negated': collections.Counter()}
	for item in items:
		if item.kind not in ('MC', 'MA') or not any(item.correct) or all(item.correct):
			continue
		pool = pools['negated' if is_negated(item.stem.plain) else 'affirmative']
		pool['items'] += 1
		for choice, is_key in zip(item.choices, item.correct):
			side = 'key' if is_key else 'distractor'
			pool[f'{side}_n'] += 1
			pool[f'{side}_hedge'] += int(bool(HEDGE_RE.search(choice.plain)))
			pool[f'{side}_absolute'] += int(bool(ABSOLUTE_RE.search(choice.plain)))
	return pools

#============================================
def k2_rate(pool: collections.Counter, side: str, kind: str) -> float:
	"""Share of choices on one side of a pool that hold hedge or absolute words."""
	rate = pool[f'{side}_{kind}'] / pool[f'{side}_n']
	return rate

#============================================
def k2_findings(pools: dict) -> list:
	"""File-level K2 findings for pools with enough items and a clear gap."""
	findings = []
	for name, pool in pools.items():
		if pool['items'] < K2_MIN_ITEMS:
			continue
		# the true statements are the keys, except under a negated stem
		true_side, false_side = ('distractor', 'key') if name == 'negated' else ('key', 'distractor')
		cues = []
		hedge_gap = k2_rate(pool, true_side, 'hedge') - k2_rate(pool, false_side, 'hedge')
		if hedge_gap >= K2_RATE_GAP:
			cues.append(f'hedges concentrate on {true_side}s')
		absolute_gap = k2_rate(pool, false_side, 'absolute') - k2_rate(pool, true_side, 'absolute')
		if absolute_gap >= K2_RATE_GAP:
			cues.append(f'absolutes concentrate on {false_side}s')
		if cues:
			message = f'{name} stems ({pool["items"]} items): {k2_describe(pool)}; '
			message += ', '.join(cues)
			findings.append(Finding(0, 'K2', message))
	return findings

#============================================
def k2_describe(pool: collections.Counter) -> str:
	"""Describe the hedge and absolute rates of a pool for the report."""
	parts = []
	for kind in ('hedge', 'absolute'):
		key_rate = k2_rate(pool, 'key', kind)
		distractor_rate = k2_rate(pool, 'distractor', kind)
		parts.append(f'{kind} key {key_rate:.0%} vs distractor {distractor_rate:.0%}')
	text = '; '.join(parts)
	return text

#============================================
def format_report(path: str, items: list, skipped: int) -> list:
	"""Build the report lines for one file.

	Args:
		path: File path shown in the report.
		items: Parsed items.
		skipped: Count of malformed lines.

	Returns:
		list: Report lines.
	"""
	findings = []
	for item in items:
		findings += item_findings(item)
	pools = k2_tally(items)
	findings += k2_findings(pools)
	findings.sort(key=lambda f: (f.line_no, f.check))

	lines = [f'=== {path} ===', 'Findings:']
	if not findings:
		lines.append('  (none)')
	for finding in findings:
		where = f'Q{finding.line_no}' if finding.line_no else 'file'
		lines.append(f'  {where:<6} {finding.check}  {finding.message}')

	lines.append('Summary:')
	kind_counts = collections.Counter(item.kind for item in items)
	counts_text = ', '.join(f'{kind}={n}' for kind, n in sorted(kind_counts.items()))
	items_line = f'  items: {len(items)}'
	if counts_text:
		items_line += f' ({counts_text})'
	items_line += f'; malformed lines skipped: {skipped}'
	lines.append(items_line)
	longest, total, chance = k1_summary(items)
	if total:
		k1_line = f'  K1 key is the longest choice in {longest} of {total} single-key MC items '
		k1_line += f'({longest / total:.0%}); chance rate {chance:.0%}'
		lines.append(k1_line)
	else:
		lines.append('  K1 no single-key MC items')
	for name, pool in pools.items():
		if pool['items']:
			lines.append(f'  K2 {name} stems ({pool["items"]} items): {k2_describe(pool)}')
	by_check = collections.Counter(finding.check for finding in findings)
	lines.append('  findings by check: ' + ' '.join(f'{c}={by_check[c]}' for c in CHECK_IDS))
	return lines

#============================================
def build_report(paths: list) -> list:
	"""Build the full advisory report for several files.

	Args:
		paths: BBQ text file paths.

	Returns:
		list: Report lines.
	"""
	lines = [
		'Question text advisory report',
		'Heuristic aid only: each finding is a mechanical cue for a reviewer to look at,',
		'never a pass/fail gate. Exit status is always 0.',
	]
	for path in paths:
		lines.append('')
		if not os.path.isfile(path):
			lines.append(f'=== {path} ===')
			lines.append('  skipped: not a file')
			continue
		items, skipped = read_items(path)
		lines += format_report(path, items, skipped)
	return lines

#============================================
def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(
		description='Advisory report of testwiseness cues and text slips in BBQ question files.'
	)
	parser.add_argument(
		'-i', '--input', dest='input_files', nargs='+', required=True,
		help='One or more Blackboard BBQ text files',
	)
	args = parser.parse_args()
	return args

#============================================
def main() -> None:
	args = parse_args()
	for line in build_report(args.input_files):
		print(line)

#============================================
if __name__ == '__main__':
	main()
