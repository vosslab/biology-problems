"""Pool-relative interestingness ordering, separate from biological acceptance."""

# Standard Library
import dataclasses

# local repo modules
import pedigree_lib.affected_features as affected_features
import pedigree_lib.family as family_model
import pedigree_lib.generation_features as generation_features
import pedigree_lib.geometry_features as geometry_features
import pedigree_lib.questions as questions
import pedigree_lib.layout as layout

METHOD = 'equal_mean_percentile_rank_v1'


#============================================
def structure_score(family: family_model.Family, diagram: layout.Diagram) -> float:
	"""Score shape without preferring a sampled Mendelian outcome."""
	rows = generation_features.counts(family)
	result = generation_features.progression(rows) - geometry_features.mean_row_density(diagram)
	return result


#============================================
def measurements(case: questions.AcceptedCase) -> dict[str, float]:
	"""Return the five raw structural and geometry signals used for pool ranking."""
	family = case.case.family
	observations = case.case.observations
	rows = generation_features.counts(family)
	empty = geometry_features.bottom_empty_space(case.diagram)['score']
	result = dict(
		outside_affected_reach=affected_features.outside_reach_fraction(family, observations),
		affected_region_fill=affected_features.affected_region_fill(
			family, observations, case.diagram),
		generation_progression=float(generation_features.progression(rows)),
		mean_row_density=geometry_features.mean_row_density(case.diagram),
		excess_bottom_empty=max(0.0, empty - geometry_features.BOTTOM_EMPTY_TARGET))
	return result


#============================================
def _percentile_rank_numerators(values: list[float]) -> list[int]:
	"""Return exact percentile numerators over the shared denominator 2 * N."""
	order = sorted(range(len(values)), key=values.__getitem__)
	ranks = [0] * len(values)
	index = 0
	while index < len(order):
		end = index + 1
		while end < len(order) and values[order[end]] == values[order[index]]:
			end += 1
		# The percentile is (average_rank - 0.5) / N, with denominator 2 * N.
		percentile_numerator = index + end
		for tied_index in range(index, end):
			ranks[order[tied_index]] = percentile_numerator
		index = end
	return ranks


#============================================
def rank(pool: list[questions.AcceptedCase]) -> list[questions.AcceptedCase]:
	"""Return a stable ordering by the equal mean of five favorable pool ranks.

	Lower outside-reach, row density, and above-target empty space are favorable;
	higher affected-region fill and progression are favorable. Sorting is stable,
	so candidates tied on the combined rank retain their randomized arrival order.
	"""
	if not pool:
		return []
	values = [measurements(case) for case in pool]
	features = (
		('outside_affected_reach', -1),
		('affected_region_fill', 1),
		('generation_progression', 1),
		('mean_row_density', -1),
		('excess_bottom_empty', -1))
	score_numerators = [0] * len(pool)
	for name, direction in features:
		column = [direction * row[name] for row in values]
		ranks = _percentile_rank_numerators(column)
		score_numerators = [score + ranks[index]
			for index, score in enumerate(score_numerators)]
	# Convert to display floats only after exact integer totals determine ordering.
	score_denominator = 2 * len(pool) * len(features)
	scores = [score / score_denominator for score in score_numerators]
	order = sorted(range(len(pool)), key=score_numerators.__getitem__, reverse=True)
	ranked = [dataclasses.replace(pool[index], ranking_score=scores[index])
		for index in order]
	return ranked
