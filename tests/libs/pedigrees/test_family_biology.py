"""Mendelian contradictions and disclosure are stable assessment contracts."""

import random

import pytest

import pedigree_lib.family as family
import pedigree_lib.inheritance as inheritance


def trio(child_sex: str = 'male') -> family.Family:
	result = family.Family((family.Person('f', 'male'), family.Person('m', 'female'),
		family.Person('c', child_sex)), (family.Union('f', 'm', ('c',)),))
	return result


def observations(father: bool, mother: bool, child: bool) -> dict:
	result = {pid: family.Observation(value) for pid, value in zip('fmc', (father, mother, child))}
	return result


def test_recessive_affected_parents_cannot_have_unaffected_child() -> None:
	result = inheritance.analyze(trio(), observations(True, True, False), 'autosomal recessive')
	assert not result.compatible
	assert inheritance.transmissions('autosomal recessive', (1, 1), (0, 1), 'male').count((1, 1)) == 2


def test_x_linked_father_and_son_is_possible_through_mother() -> None:
	assert inheritance.analyze(trio(), observations(True, False, True), 'x-linked recessive').compatible
	assert inheritance.analyze(trio(), observations(True, True, True), 'x-linked dominant').compatible
	assert not inheritance.analyze(trio(), observations(True, False, True), 'x-linked dominant').compatible


def test_x_linked_daughters_and_maternal_transmission() -> None:
	assert not inheritance.analyze(trio('female'), observations(True, False, False), 'x-linked dominant').compatible
	assert inheritance.analyze(trio('female'), observations(True, False, False), 'x-linked recessive').compatible
	assert not inheritance.analyze(trio(), observations(False, True, False), 'x-linked recessive').compatible


def test_y_contradictions_in_second_founding_family() -> None:
	first = trio()
	second = family.Family(first.people + (family.Person('g', 'male'), family.Person('h', 'female'),
		family.Person('i', 'male')), first.unions + (family.Union('g', 'h', ('i',)),))
	visible = observations(True, False, True)
	visible.update({pid: family.Observation(value) for pid, value in zip('ghi', (True, False, False))})
	assert not inheritance.analyze(second, visible, 'y-linked').compatible


@pytest.mark.parametrize('mode', inheritance.MODES)
def test_simulated_genotypes_and_disclosure(mode: str) -> None:
	pedigree = trio('female')
	genotypes = inheritance.simulate(pedigree, mode, random.Random(24))
	before = dict(genotypes)
	hidden = inheritance.observe(pedigree, mode, genotypes)
	shown = inheritance.observe(pedigree, mode, genotypes, show_carriers=True)
	assert genotypes == before
	assert inheritance.analyze(pedigree, hidden, mode).compatible
	assert inheritance.analyze(pedigree, shown, mode).compatible


def test_carrier_disclosure_does_not_require_noncarriers() -> None:
	pedigree = trio('female')
	genotypes = {'f': (1,), 'm': (0, 0), 'c': (0, 1)}
	assert not inheritance.observe(pedigree, 'x-linked recessive', genotypes)['c'].carrier
	assert inheritance.observe(pedigree, 'x-linked recessive', genotypes, True)['c'].carrier


def test_structural_errors_are_explicit() -> None:
	pedigree = trio()
	with pytest.raises(ValueError):
		family.Family(pedigree.people, (family.Union('f', 'm', ('c', 'c')),)).generations()
	with pytest.raises(ValueError):
		family.Family(pedigree.people, (family.Union('f', 'm', ('missing',)),)).generations()
	with pytest.raises(ValueError):
		family.Family(pedigree.people, (family.Union('f', 'm', ('f',)),)).generations()
	with pytest.raises(ValueError):
		family.Family(pedigree.people, pedigree.unions * 2).generations()


def test_male_carrier_and_affected_female_exclude_sex_linked_modes() -> None:
	visible = observations(False, False, False)
	visible['f'] = family.Observation(False, carrier=True)
	assert inheritance.analyze(trio(), visible, 'autosomal recessive').compatible
	assert not inheritance.analyze(trio(), visible, 'x-linked recessive').compatible
	assert not inheritance.analyze(trio('female'), observations(True, False, True), 'y-linked').compatible
