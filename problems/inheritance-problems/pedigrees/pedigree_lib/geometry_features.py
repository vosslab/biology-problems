"""Rendered measurements, separate from pedigree topology and teaching policy."""

import collections

import pedigree_lib.layout as layout


#============================================
def people_per_width(diagram: layout.Diagram) -> float:
	"""Measure horizontal density in native drawing units, before display scaling."""
	result = len(diagram.symbols) / diagram.width
	return result


#============================================
def mean_row_density(diagram: layout.Diagram) -> float:
	"""People per occupied row width, excluding generation I, in native units."""
	rows = collections.defaultdict(list)
	for symbol in diagram.symbols:
		rows[symbol.y].append(symbol.x)
	# The renderers draw 30-unit symbols; match the experiment's occupied-width definition.
	densities = [len(rows[y]) / (max(rows[y]) - min(rows[y]) + 30)
		for y in sorted(rows)[1:]]
	result = sum(densities) / len(densities) if densities else 0.0
	return result
