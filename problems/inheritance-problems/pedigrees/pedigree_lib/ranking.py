"""One removable compactness preference; not a calibrated interestingness model."""

import pedigree_lib.geometry_features as geometry_features
import pedigree_lib.questions as questions


#============================================
def score(case: questions.AcceptedCase) -> float:
	"""Higher density ranks first, equivalently lower native width per person."""
	result = geometry_features.people_per_width(case.diagram)
	return result
