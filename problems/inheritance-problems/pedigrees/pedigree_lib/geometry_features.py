"""Rendered measurements, separate from pedigree topology and teaching policy."""

import pedigree_lib.layout as layout


#============================================
def people_per_width(diagram: layout.Diagram) -> float:
	"""Measure horizontal density in native drawing units, before display scaling."""
	result = len(diagram.symbols) / diagram.width
	return result
