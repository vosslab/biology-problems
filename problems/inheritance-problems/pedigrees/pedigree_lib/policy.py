"""Lecture 05C teaching profiles, evaluated without an answer or hidden genotypes."""

# Standard Library
import dataclasses

# local repo modules
import pedigree_lib.family as family_model
import pedigree_lib.inheritance as inheritance

AUTOSOMAL_MAX_SQUARED_BIAS = 0.25
SEX_LINKED_MIN_SQUARED_BIAS = 0.99


#============================================
@dataclasses.dataclass(frozen=True)
class Assessment:
	compatibility: dict[str, inheritance.Compatibility]
	evidence: dict[str, tuple[str, ...]]
	answer: str | None
	reasons: tuple[str, ...]


#============================================
def teaching_evidence(family: family_model.Family, observations: dict) -> dict[str, tuple]:
	"""Require informative relationships independently of the sex-balance filter.

	Args:
		family: Family to inspect.
		observations: Student-visible observations, without intended answers or genotypes.

	Returns:
		Visible teaching rationale for each mode whose profile is satisfied.
	"""
	family_model.validate_observations(family, observations)
	if any(obs.affected is None for obs in observations.values()):
		return {mode: () for mode in inheritance.MODES}
	people = family.members()
	parents = family.parentage()
	affected = {pid for pid, obs in observations.items() if obs.affected is True}
	if not affected:
		return {mode: () for mode in inheritance.MODES}
	males = sum(people[pid].sex == 'male' for pid in affected)
	females = len(affected) - males
	unaffected = {pid for pid, obs in observations.items() if obs.affected is False}
	sexes = {people[pid].sex for pid in affected}
	both_sexes = sexes == {'male', 'female'}
	vertical = False
	skipping = []
	father_unaffected_daughter = False
	xd_father = False
	maternal = False
	xr_bridge = False
	y_chain = False
	y_sibship = False
	for union in family.unions:
		sons = [pid for pid in union.children if people[pid].sex == 'male']
		daughters = [pid for pid in union.children if people[pid].sex == 'female']
		if union.father in unaffected and union.mother in unaffected:
			skipping.extend(pid for pid in union.children if pid in affected)
		if union.father in affected:
			father_unaffected_daughter |= any(pid in unaffected for pid in daughters)
			xd_father |= bool(sons and daughters) and all(pid in affected for pid in daughters) \
				and all(pid in unaffected for pid in sons) and union.mother in unaffected
			y_sibship |= len(sons) >= 2 and bool(daughters) and all(pid in affected for pid in sons)
			if union.father in parents:
				y_chain |= parents[union.father].father in affected and any(pid in affected for pid in sons)
		if union.mother in affected and union.father in unaffected:
			maternal |= any(pid in affected for pid in sons) and any(pid in unaffected for pid in union.children)
		if union.mother in unaffected and union.mother in parents:
			xr_bridge |= parents[union.mother].father in affected and any(pid in affected for pid in sons)
		for parent in (union.father, union.mother):
			if parent in affected and parent in parents:
				grandparents = parents[parent]
				vertical |= bool({grandparents.father, grandparents.mother} & affected) \
					and any(pid in affected for pid in union.children)
	consanguineous = any(family.ancestors(u.father) & family.ancestors(u.mother)
		for u in family.unions if any(child in skipping for child in u.children))
	result = {mode: () for mode in inheritance.MODES}
	if both_sexes and vertical and father_unaffected_daughter and not skipping:
		result['autosomal dominant'] = ('Affected lineage spans three generations',
			'Both sexes affected', 'Affected father has an unaffected daughter')
	if skipping and (both_sexes or consanguineous):
		result['autosomal recessive'] = ('Unaffected parents have affected offspring',
			'Both sexes affected or affected offspring of related parents')
	if xd_father and maternal:
		result['x-linked dominant'] = ('Affected father: affected daughters and unaffected sons',
			'Affected mother has affected sons and unaffected offspring')
	if sexes == {'male'} and xr_bridge and skipping:
		result['x-linked recessive'] = ('Affected grandfather connects through an unaffected daughter',
			'Unaffected parents have affected sons', 'Observed affected individuals are male')
	if sexes == {'male'} and y_chain and y_sibship:
		result['y-linked'] = ('Affected fathers and sons span three generations',
			'Multiple sons affected in an informative sibship with daughters',
			'Observed females unaffected')
	for mode, evidence in result.items():
		if evidence:
			result[mode] += (f'Affected males: {males}; affected females: {females}',)
	return result


#============================================
def sex_balance_acceptable(mode: str, males: int, females: int) -> bool:
	"""Require at least two affected people before filtering their sex balance."""
	if males + females < 2:
		return False
	bias = (males - females) ** 2 / (males + females)
	if mode in ('autosomal dominant', 'autosomal recessive'):
		return bias < AUTOSOMAL_MAX_SQUARED_BIAS
	if mode == 'x-linked dominant':
		return females > males and bias > SEX_LINKED_MIN_SQUARED_BIAS
	if mode == 'x-linked recessive':
		return males > females and bias > SEX_LINKED_MIN_SQUARED_BIAS
	if mode == 'y-linked':
		return females == 0
	raise ValueError(f'Unknown mode: {mode}')


#============================================
def assess(family: family_model.Family, observations: dict) -> Assessment:
	"""Combine rare-trait compatibility with unique visible teaching evidence.

	Args:
		family: Family to assess.
		observations: Complete visible affected/unaffected and carrier observations.

	Returns:
		Compatibility, evidence, and unique answer, or rejection reasons.

	Raises:
		ValueError: Invalid family or observation data.
	"""
	family_model.validate_observations(family, observations)
	noncarrier_ids = frozenset(pid for pid in family_model.later_spouses(family)
		if observations[pid].affected is False)
	compatibility = {mode: inheritance.analyze(family, observations, mode,
		noncarrier_ids=noncarrier_ids)
		for mode in inheritance.MODES}
	evidence = teaching_evidence(family, observations)
	qualified = [mode for mode in inheritance.MODES
		if compatibility[mode].compatible and evidence[mode]]
	answer = qualified[0] if len(qualified) == 1 else None
	reasons = ()
	if not qualified:
		reasons = ('No compatible mode meets a teaching profile',)
	elif len(qualified) > 1:
		reasons = ('Tied teaching profiles: ' + ', '.join(qualified),)
	if answer is not None:
		males = sum(p.sex == 'male' and observations[p.id].affected for p in family.people)
		females = sum(p.sex == 'female' and observations[p.id].affected for p in family.people)
		if not sex_balance_acceptable(answer, males, females):
			reasons = (f'Affected-sex balance fails {answer}: {males} males, {females} females',)
			answer = None
	if answer is not None:
		ranks = family.generations()
		last_generation = max(ranks.values())
		if not any(obs.affected and ranks[pid] >= last_generation - 1
				for pid, obs in observations.items()):
			reasons = ('An affected individual must appear in one of the last two generations',)
			answer = None
	result = Assessment(compatibility, evidence, answer, reasons)
	return result
