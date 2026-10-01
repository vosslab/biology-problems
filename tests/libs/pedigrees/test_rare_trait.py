"""Rare-trait homework excludes later carrier spouses, not inherited carriers."""

import pytest

import pedigree_lib.family as family
import pedigree_lib.inheritance as inheritance
import pedigree_lib.policy as policy
import pedigree_lib.questions as questions
import pedigree_lib.sources as sources


def recessive_case(spouse: tuple[int, int], affected_children: bool) -> sources.Case:
	"""A carrier founding couple has affected children; their son has an unrelated spouse."""
	people = tuple(family.Person(pid, sex) for pid, sex in (
		('f', 'male'), ('m', 'female'), ('s', 'male'), ('d', 'female'),
		('w', 'female'), ('boy', 'male'), ('girl', 'female')))
	pedigree = family.Family(people, (family.Union('f', 'm', ('s', 'd')),
		family.Union('s', 'w', ('boy', 'girl'))))
	child = (1, 1) if affected_children else (0, 1)
	genotypes = {'f': (0, 1), 'm': (0, 1), 's': (1, 1), 'd': (1, 1),
		'w': spouse, 'boy': child, 'girl': child}
	visible = inheritance.observe(pedigree, 'autosomal recessive', genotypes)
	result = sources.Case(pedigree, visible, genotypes)
	return result


def test_multiple_founding_couples_and_descendant_partners_are_not_later_spouses() -> None:
	people = tuple(family.Person(pid, sex) for pid, sex in (
		('a', 'male'), ('b', 'female'), ('c', 'male'), ('d', 'female'),
		('son', 'male'), ('daughter', 'female'), ('grandson', 'male'),
		('spouse', 'female'), ('child', 'female')))
	pedigree = family.Family(people, (
		family.Union('a', 'b', ('son',)), family.Union('c', 'd', ('daughter',)),
		family.Union('son', 'daughter', ('grandson',)),
		family.Union('grandson', 'spouse', ('child',))))
	assert family.later_spouses(pedigree) == frozenset({'spouse'})


@pytest.mark.parametrize('spouse, affected_children', [((0, 0), False), ((1, 1), True)])
def test_founder_carriers_inherited_carriers_and_affected_spouses_are_allowed(
		spouse: tuple[int, int], affected_children: bool) -> None:
	case = recessive_case(spouse, affected_children)
	accepted, reasons = questions.evaluate(case)
	assert accepted is not None, reasons
	assert accepted.assessment.answer == 'autosomal recessive'


def test_required_carrier_spouse_is_biologically_possible_but_not_rare_trait_homework() -> None:
	case = recessive_case((0, 1), True)
	assert inheritance.analyze(case.family, case.observations, 'autosomal recessive').compatible
	assessment = policy.assess(case.family, case.observations)
	assert not assessment.compatibility['autosomal recessive'].compatible
	assert assessment.answer is None
	# Authored cases without hidden genotypes must also be rejected.
	accepted, reasons = questions.evaluate(sources.Case(case.family, case.observations))
	assert accepted is None and reasons


def test_hidden_carrier_spouse_is_rejected_even_when_not_required_by_the_drawing() -> None:
	case = recessive_case((0, 1), False)
	assert policy.assess(case.family, case.observations).answer == 'autosomal recessive'
	accepted, reasons = questions.evaluate(case)
	assert accepted is None and reasons


def test_x_linked_recessive_cannot_require_an_unaffected_carrier_wife() -> None:
	pedigree = recessive_case((0, 0), False).family
	visible = {pid: family.Observation(pid == 'boy') for pid in pedigree.members()}
	assert inheritance.analyze(pedigree, visible, 'x-linked recessive').compatible
	assert not policy.assess(pedigree, visible).compatibility['x-linked recessive'].compatible
