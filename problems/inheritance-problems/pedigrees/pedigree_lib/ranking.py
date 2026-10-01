"""Removable interestingness heuristic; no fitted weights or reviewed data."""

import pedigree_lib.geometry_features as geometry_features
import pedigree_lib.generation_features as generation_features
import pedigree_lib.questions as questions


#============================================
def score(case: questions.AcceptedCase) -> float:
	"""Prefer progression, then lower row density among equal progression scores.

	Native row density is below one, so it breaks ties in integer progression.
	This deliberately small heuristic is not a calibrated probability or quality scale.
	"""
	rows = generation_features.counts(case.case.family)
	result = generation_features.progression(rows) - geometry_features.mean_row_density(case.diagram)
	return result
