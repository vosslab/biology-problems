"""Acceptance, source parity, and biological state survive rendering changes."""

import random
import pathlib
import dataclasses

import pytest

import pedigree_lib.family as family
import pedigree_lib.policy as policy
import pedigree_lib.layout as layout
import pedigree_lib.sources as sources
import pedigree_lib.questions as questions
import pedigree_lib.inheritance as inheritance


@pytest.mark.parametrize('mode', inheritance.MODES)
def test_procedural_case_has_supported_unique_teaching_answer(mode: str) -> None:
	case = questions.generate_case(mode, random.Random(351))
	assessment = policy.assess(case.case.family, case.case.observations)
	assert assessment.answer == mode
	assert assessment.compatibility[mode].compatible and assessment.evidence[mode]
	assert not layout.layout_errors(case.diagram)


@pytest.mark.parametrize('authored', (True, False))
def test_matching_set_is_independently_supported(authored: bool) -> None:
	bank = questions.authored_cases() if authored else None
	matching = questions.matching_set(random.Random(351), bank)
	assert {case.assessment.answer for case in matching} == set(inheritance.MODES)
	assert all(policy.assess(c.case.family, c.case.observations).answer == c.assessment.answer for c in matching)
	sizes = [len(c.case.family.people) for c in matching]
	assert max(sizes) - min(sizes) <= 3


def test_weak_case_is_rejected_and_exhaustion_is_explicit() -> None:
	pedigree = family.Family((family.Person('f', 'male'), family.Person('m', 'female'),
		family.Person('s', 'male')), (family.Union('f', 'm', ('s',)),))
	visible = {pid: family.Observation(pid != 'm') for pid in ('f', 'm', 's')}
	accepted, reasons = questions.evaluate(sources.Case(pedigree, visible))
	assert accepted is None and reasons
	with pytest.raises(questions.GenerationFailure, match='0 attempts'):
		questions.generate_case('autosomal dominant', random.Random(2), max_attempts=0)


def test_hidden_state_does_not_choose_answer() -> None:
	case = questions.generate_case('x-linked recessive', random.Random(351))
	changed = dataclasses.replace(case.case, genotypes={}, metadata={'expected_mode': 'y-linked'})
	accepted, _ = questions.evaluate(changed)
	assert accepted.assessment.answer == case.assessment.answer


def test_yaml_labels_and_sibling_order_are_person_bound(tmp_path: pathlib.Path) -> None:
	path = tmp_path / 'family.yml'
	path.write_text('cases:\n- people:\n'
		'  - {id: f, sex: male, affected: false}\n'
		'  - {id: m, sex: female, affected: false}\n'
		'  - {id: a, sex: male, affected: true, label: Alpha}\n'
		'  - {id: b, sex: female, affected: true, label: Beta}\n'
		'  unions:\n  - {father: f, mother: m, children: [a, b], sibling_order: [b, a]}\n')
	case = questions.authored_cases(path)[0]
	variant = questions.present(case, random.Random(351))
	assert variant.case.family.unions[0].children == ('b', 'a')
	assert {p.person: p.label for p in variant.diagram.symbols}['a'] == 'Alpha'


def test_infeasible_size_bounds_fail_before_construction() -> None:
	with pytest.raises(ValueError, match='Size bounds'):
		sources.procedural_family(random.Random(351), min_people=2, max_people=5)


def test_recessive_cousin_family_with_tied_profiles_is_rejected() -> None:
	people = tuple(family.Person(pid, sex) for pid, sex in zip('ABCDEFGHI',
		('male', 'female', 'male', 'female', 'female', 'male', 'male', 'female', 'male')))
	unions = (family.Union('A', 'B', ('C', 'D')), family.Union('C', 'E', ('G',)),
		family.Union('F', 'D', ('H',)), family.Union('G', 'H', ('I',)))
	pedigree = family.Family(people, unions)
	visible = {p.id: family.Observation(p.id in ('F', 'I')) for p in people}
	assessment = policy.assess(pedigree, visible)
	assert assessment.answer is None
	assert assessment.evidence['autosomal recessive'] and assessment.evidence['x-linked recessive']
	assert assessment.compatibility['autosomal recessive'].compatible
	assert assessment.compatibility['x-linked recessive'].compatible
