"""Generation measurements independent of genetics, difficulty, and layout."""

import collections

import pedigree_lib.family as family_model


#============================================
def counts(family: family_model.Family) -> list[int]:
	"""Return population per generation, including generation I."""
	rows = collections.Counter(family.generations().values())
	result = [rows[i] for i in range(max(rows) + 1)]
	return result


#============================================
def progression(rows: list[int]) -> int:
	"""Count expansions minus contractions, ignoring generation I."""
	result = sum((b > a) - (b < a) for a, b in zip(rows[1:-1], rows[2:]))
	return result


#============================================
def shrink(rows: list[int]) -> float:
	"""Mean squared contraction divided by pair population, ignoring generation I."""
	terms = [max(0, a - b) ** 2 / (a + b) for a, b in zip(rows[1:-1], rows[2:])]
	result = sum(terms) / len(terms) if terms else 0.0
	return result
