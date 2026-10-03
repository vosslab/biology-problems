"""Visible affected ancestry measurements, not judgments of teaching value."""

import pedigree_lib.family as family_model
import pedigree_lib.layout as layout


#============================================
def outside_reach_fraction(family: family_model.Family, observations: dict) -> float:
	"""Measure people outside affected ancestry and its immediate partners.

	Include unaffected ancestors of affected people and immediate partners of anyone
	in that ancestry. Do not recursively include partners' ancestors or descendants.
	Hidden carrier genotypes never enter this measurement. Unaffected relatives outside
	the set can still provide teaching evidence, so this is not a pruning rule.
	"""
	family_model.validate_observations(family, observations)
	parents = family.parentage()
	core = {pid for pid, obs in observations.items() if obs.affected}
	pending = list(core)
	while pending:
		pid = pending.pop()
		if pid in parents:
			union = parents[pid]
			for parent in (union.father, union.mother):
				if parent not in core:
					core.add(parent)
					pending.append(parent)
	reach = set(core)
	for union in family.unions:
		if union.father in core or union.mother in core:
			reach.update((union.father, union.mother))
	result = (len(family.people) - len(reach)) / len(family.people)
	return result


#============================================
def affected_region_fill(family: family_model.Family, observations: dict,
		diagram: layout.Diagram) -> float:
	"""Fraction of person-occupied native regions containing affected people.

	Regions cover two generations by four sibling pitches. Horizontal cells start
	at the left edge of the leftmost layout symbol; connector-only cells are ignored.
	"""
	family_model.validate_observations(family, observations)
	ranks = family.generations()
	left = min(symbol.x for symbol in diagram.symbols) - layout.RADIUS
	cell_width = 4 * (2 * layout.RADIUS + layout.SIBLING_GAP)
	occupied = set()
	affected = set()
	for symbol in diagram.symbols:
		cell = (ranks[symbol.person] // 2, int((symbol.x - left) // cell_width))
		occupied.add(cell)
		if observations[symbol.person].affected:
			affected.add(cell)
	result = len(affected) / len(occupied)
	return result
