"""Repair conspicuous lower whitespace with a bounded geometry-first growth step."""

# Standard Library
import dataclasses
import random
import re

# local repo modules
import pedigree_lib.difficulty as difficulty
import pedigree_lib.family as family_model
import pedigree_lib.geometry_features as geometry_features
import pedigree_lib.inheritance as inheritance
import pedigree_lib.layout as layout
import pedigree_lib.questions as questions
import pedigree_lib.sources as sources

#============================================
#============================================
def _mirror(accepted: questions.AcceptedCase) -> bool:
	"""Retain the accepted diagram orientation when laying out probes and edits."""
	x = {symbol.person: symbol.x for symbol in accepted.diagram.symbols}
	first = accepted.case.family.unions[0]
	result = x[first.father] > x[first.mother]
	return result


#============================================
def _next_id(family: family_model.Family, reserved: set[str] | None = None) -> str:
	"""Return the next unused p-number for a new person."""
	used = set(family.members())
	if reserved is not None:
		used.update(reserved)
	numbers = [int(match.group(1)) for pid in used
		if (match := re.fullmatch(r'p(\d+)', pid)) is not None]
	number = max(numbers, default=0) + 1
	while f'p{number}' in used:
		number += 1
	result = f'p{number}'
	return result


#============================================
def _recipes(case: sources.Case) -> list[dict]:
	"""List child additions and uncoupled branch promotions in stable family order."""
	family = case.family
	settings = difficulty.difficulty_settings('rigorous')
	if len(family.people) >= settings['people'][1]:
		return []
	ranks = family.generations()
	last_generation = settings['generations'][0] - 1
	result = [dict(kind='add_child', father=union.father, mother=union.mother)
		for union in family.unions if ranks[union.father] < last_generation]
	parents = family.parentage()
	partners = {pid for union in family.unions for pid in (union.father, union.mother)}
	for person in family.people:
		if (person.id in parents and person.id not in partners
				and ranks[person.id] < last_generation
				and len(family.people) + 2 <= settings['people'][1]):
			result.append(dict(kind='promote', person=person.id))
	return result


#============================================
def _probe(case: sources.Case, recipe: dict) -> tuple[family_model.Family, str]:
	"""Create a fixed-sex geometry probe without sampling genetic outcomes."""
	family = case.family
	people = list(family.people)
	unions = list(family.unions)
	if recipe['kind'] == 'add_child':
		child_id = _next_id(family)
		people.append(family_model.Person(child_id, 'male'))
		index = next(index for index, union in enumerate(unions)
			if (union.father, union.mother) == (recipe['father'], recipe['mother']))
		union = unions[index]
		unions[index] = dataclasses.replace(union, children=union.children + (child_id,))
	else:
		mate_id = _next_id(family)
		child_id = _next_id(family, {mate_id})
		person = family.members()[recipe['person']]
		mate_sex = 'female' if person.sex == 'male' else 'male'
		people.extend((family_model.Person(mate_id, mate_sex),
			family_model.Person(child_id, 'male')))
		father, mother = ((person.id, mate_id) if person.sex == 'male'
			else (mate_id, person.id))
		unions.append(family_model.Union(father, mother, (child_id,)))
	probe = family_model.Family(tuple(people), tuple(unions))
	return probe, child_id


#============================================
def _add_child(case: sources.Case, mode: str, father: str, mother: str,
		rng: random.Random) -> sources.Case:
	"""Sample a child's sex and transmitted genotype once from the parental cross."""
	family = case.family
	person_id = _next_id(family)
	sex = rng.choice(('male', 'female'))
	genotype = rng.choice(inheritance.transmissions(mode, case.genotypes[father],
		case.genotypes[mother], sex))
	unions = []
	for union in family.unions:
		if (union.father, union.mother) == (father, mother):
			union = dataclasses.replace(union, children=union.children + (person_id,))
		unions.append(union)
	new_family = family_model.Family(family.people + (family_model.Person(person_id, sex),),
		tuple(unions))
	observations = dict(case.observations)
	observations[person_id] = family_model.Observation(inheritance.phenotype(mode, genotype))
	genotypes = dict(case.genotypes)
	genotypes[person_id] = genotype
	result = dataclasses.replace(case, family=new_family,
		observations=observations, genotypes=genotypes)
	return result


#============================================
def _apply(case: sources.Case, mode: str, recipe: dict, rng: random.Random) -> sources.Case:
	"""Apply one selected growth and sample each new biological state once."""
	if recipe['kind'] == 'add_child':
		result = _add_child(case, mode, recipe['father'], recipe['mother'], rng)
	else:
		family = case.family
		person_id = recipe['person']
		person = family.members()[person_id]
		mate_id = _next_id(family)
		mate_sex = 'female' if person.sex == 'male' else 'male'
		if mode == 'autosomal recessive':
			mate_genotype = (1, 1) if rng.random() < 0.1 else (0, 0)
		else:
			mate_genotype = inheritance.genotype_domain(mode, mate_sex)[0]
		father, mother = ((person_id, mate_id) if person.sex == 'male'
			else (mate_id, person_id))
		union = family_model.Union(father, mother, ())
		intermediate_family = family_model.Family(
			family.people + (family_model.Person(mate_id, mate_sex),),
			family.unions + (union,))
		observations = dict(case.observations)
		observations[mate_id] = family_model.Observation(
			inheritance.phenotype(mode, mate_genotype))
		genotypes = dict(case.genotypes)
		genotypes[mate_id] = mate_genotype
		intermediate = dataclasses.replace(case, family=intermediate_family,
			observations=observations, genotypes=genotypes)
		result = _add_child(intermediate, mode, father, mother, rng)
	return result


#============================================
def _same_teaching_profile(original: questions.AcceptedCase,
		candidate: questions.AcceptedCase) -> bool:
	"""Keep the answer, evidence presence, and mode compatibility unchanged."""
	old, new = original.assessment, candidate.assessment
	if old.answer != new.answer:
		return False
	return all(bool(old.evidence[mode]) == bool(new.evidence[mode])
		and old.compatibility[mode].compatible == new.compatibility[mode].compatible
		for mode in inheritance.MODES)


#============================================
def repair(original: questions.AcceptedCase, rng: random.Random) -> questions.AcceptedCase:
	"""Fill a large lower gap with at most the capacity allowed by rigorous difficulty.

	Geometry selects the branch before sex and Mendelian outcome are sampled. A
	failed sampled candidate ends repair and returns the last accepted pedigree.
	"""
	if (not difficulty.fits_difficulty(original.case.family, 'rigorous')
			or not original.case.genotypes):
		return original
	settings = difficulty.difficulty_settings('rigorous')
	maximum_people = settings['people'][1]
	mode = original.assessment.answer
	mirror = _mirror(original)
	current = original
	while len(current.case.family.people) < maximum_people:
		before = geometry_features.bottom_empty_space(current.diagram)
		if before['score'] <= geometry_features.BOTTOM_EMPTY_TARGET:
			break
		best = None
		best_key = None
		for order, recipe in enumerate(_recipes(current.case)):
			probe_family, child_id = _probe(current.case, recipe)
			if not difficulty.fits_difficulty(probe_family, 'rigorous'):
				continue
			probe_diagram = layout.lay_out(probe_family, mirror=mirror)
			if layout.layout_errors(probe_diagram):
				continue
			probe_metric = geometry_features.bottom_empty_space(probe_diagram)
			rect = before['rect']
			if rect['width'] <= 0 or rect['height'] <= 0:
				continue
			symbol = next(item for item in probe_diagram.symbols if item.person == child_id)
			extent = 15.0 + 1.0 / layout.DISPLAY_SCALE
			intersects = (symbol.x - extent < rect['x'] + rect['width']
				and rect['x'] < symbol.x + extent
				and symbol.y - extent < rect['y'] + rect['height']
				and rect['y'] < symbol.y + extent)
			if not intersects:
				continue
			before_area = rect['width'] * rect['height']
			after_rect = probe_metric['rect']
			after_area = after_rect['width'] * after_rect['height']
			area_reduction = before_area - after_area
			score_reduction = before['score'] - probe_metric['score']
			if area_reduction <= 0 or score_reduction <= 0:
				continue
			key = (score_reduction, area_reduction, -order)
			if best_key is None or key > best_key:
				best = recipe
				best_key = key
		if best is None:
			break
		candidate = _apply(current.case, mode, best, rng)
		accepted, _ = questions.evaluate(candidate, mirror=mirror)
		if accepted is None or not _same_teaching_profile(original, accepted):
			break
		current = dataclasses.replace(accepted,
			attempts=original.attempts, rejections=original.rejections)
	return current
