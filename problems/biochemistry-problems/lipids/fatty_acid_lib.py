"""
Shared helpers for the fatty acid question generators.

Provides ASCII-art rendering of unsaturated fatty-acid skeletons suitable
for Blackboard HTML (no SVG, no <table> -- both are blocked by the
Blackboard sanitizer or stripped by bptools sanitization). Bonds are drawn
inside a courier-font span using:

  - '/'  for an upward single bond
  - '\\' for a downward single bond
  - '_'  (double low line, &#8215;) for a flat cis double bond at low y
  - <sup>=</sup> (double high line, &#9552;) for a flat cis double bond at high y

Cis double bonds keep the chain at the same y position and do NOT flip the
zigzag direction, producing the characteristic visible kink.

The library also exposes the pool-elimination position picker (matching
the PGML versions) and HTML helpers for the omega and Delta notation.
"""

# Standard Library
import random


# Monospace span wrapper for the chain. Courier + x-large mirror the look
# of the original fatty_acid_naming.py so the bonds line up cleanly.
CHAIN_SPAN_OPEN = '<span style="font-family: courier; font-size: x-large;">'
CHAIN_SPAN_CLOSE = '</span>'

# Terminal labels.
H3C_PREFIX = 'H<sub>3</sub>C'
COOH_LOW = '<sub>COOH</sub>'
COOH_HIGH = '<sup>COOH</sup>'

# Double-bond glyphs (HTML entities; the &#9552; is wrapped in <sup> so it
# visually sits at the higher zigzag baseline).
DOUBLE_LOW_GLYPH = '&#8215;'
DOUBLE_HIGH_GLYPH = '<sup>&#9552;</sup>'


#============================================
def pool_eliminate_positions(chain_length: int, num_picks: int) -> list:
	"""
	Pick num_picks scattered positions in [3..chain_length-2] with a
	minimum spacing of 3 between adjacent picks.

	Pool-elimination algorithm: pick a random position from the available
	pool, remove that position and +/- 2 around it, repeat. Bonds may
	land tightly clustered (methylene-interrupted, like alpha-linolenic
	omega-3,6,9) or scattered widely across the chain.
	"""
	# valid positions are 3..chain_length-2 inclusive
	pool = set(range(3, chain_length - 1))
	picks = []
	for _ in range(num_picks):
		if not pool:
			break
		# sort the pool before random.choice so the draw is deterministic
		# across runs given a seeded random module
		available = sorted(pool)
		pick = random.choice(available)
		picks.append(pick)
		# Eliminate +/- 2 around the pick to enforce min spacing 3
		for d in range(-2, 3):
			pool.discard(pick + d)
	picks.sort()
	return picks


#============================================
def render_fatty_acid_ascii(chain_length: int, double_bond_indices) -> str:
	"""
	Render the fatty acid as an HTML/ASCII-art string.

	Args:
		chain_length: total number of carbons in the chain.
		double_bond_indices: iterable of 0-based bond indices that should
			be drawn as cis double bonds. Bond i sits between vertex i
			(methyl-side) and vertex i+1.

	Returns:
		HTML string starting with the courier span open tag and ending
		with the closing tag, suitable for embedding directly in a
		Blackboard question stem or MC choice.
	"""
	# Set lookup for fast membership tests
	double_bonds = set(double_bond_indices)
	# y tracks current vertex height: 0 = low (baseline), 1 = high (raised)
	y = 0
	parts = []
	parts.append(CHAIN_SPAN_OPEN)
	parts.append(H3C_PREFIX)
	# Walk each bond
	for i in range(chain_length - 1):
		if i in double_bonds:
			# Flat cis double bond: emit glyph at current y, do NOT change y
			# (the cis kink emerges naturally because direction depends on y)
			if y == 0:
				parts.append(DOUBLE_LOW_GLYPH)
			else:
				parts.append(DOUBLE_HIGH_GLYPH)
		else:
			# Single bond: alternate up/down based on current y
			if y == 0:
				parts.append('/')
				y = 1
			else:
				# backslash needs escaping in Python string but appears as
				# a single '\' in the rendered HTML
				parts.append('\\')
				y = 0
	# Terminal COOH at whichever y the chain ended on
	if y == 0:
		parts.append(COOH_LOW)
	else:
		parts.append(COOH_HIGH)
	parts.append(CHAIN_SPAN_CLOSE)
	html = ''.join(parts)
	return html


#============================================
def omegas_to_bond_indices(omegas) -> list:
	"""
	Convert a list of omega positions to 0-based bond indices.

	omega-k means the double bond between Ck and C(k+1) counted from the
	methyl end. In our methyl-on-left layout, that bond sits at index k-1.
	"""
	bond_indices = [k - 1 for k in omegas]
	return bond_indices


#============================================
def deltas_to_bond_indices(chain_length: int, deltas) -> list:
	"""
	Convert a list of Delta positions to 0-based bond indices.

	Delta-k means the double bond between Ck and C(k+1) counted from the
	carboxyl (COOH = 1) end. In our methyl-on-left layout, that bond
	sits at index (chain_length - k - 1).
	"""
	bond_indices = [chain_length - k - 1 for k in deltas]
	bond_indices.sort()
	return bond_indices


#============================================
def format_omega_html(positions) -> str:
	"""
	Format a list of omega positions as bold HTML, e.g.
	'<b>&omega;-3,6,9</b>'.
	"""
	joined = ','.join(str(p) for p in positions)
	html = '<b>&omega;&ndash;' + joined + '</b>'
	return html


#============================================
def format_delta_html(positions) -> str:
	"""
	Format a list of Delta positions as bold HTML, e.g.
	'<b>&Delta;-9,12,15</b>'.
	"""
	joined = ','.join(str(p) for p in positions)
	html = '<b>&Delta;&ndash;' + joined + '</b>'
	return html


#============================================
def shift_bond_indices(bond_indices, amount: int, chain_length: int):
	"""
	Shift each bond index by amount. Returns the shifted list, or an
	empty list if any shifted index would fall outside [0, chain_length-2].
	Useful for building off-by-one distractors.
	"""
	shifted = []
	for b in bond_indices:
		new_b = b + amount
		if new_b < 0 or new_b > chain_length - 2:
			return []
		shifted.append(new_b)
	return shifted


#============================================
def mirror_bond_indices(bond_indices, chain_length: int) -> list:
	"""
	Mirror each bond index around the chain center. For a student who
	read the notation from the wrong end, their drawn bond at original
	bond_index b would land at (chain_length - 2 - b). Returns sorted
	ascending list.
	"""
	mirrored = [(chain_length - 2 - b) for b in bond_indices]
	mirrored.sort()
	return mirrored
