"""Structural measurements must reflect relationships, not IDs or drawing order."""

import dataclasses

import pytest

import pedigree_lib.family as family
import pedigree_lib.features as features


def branching_family() -> family.Family:
	people = tuple(family.Person(pid, sex) for pid, sex in zip('abcdefghij',
		('male', 'female', 'male', 'female', 'female', 'male',
		'male', 'female', 'female', 'male')))
	result = family.Family(people, (
		family.Union('a', 'b', ('c', 'd')),
		family.Union('c', 'e', ('g', 'h', 'i')),
		family.Union('f', 'd', ('j',))))
	return result


def test_branch_measurements_count_descendants_and_degree_distribution() -> None:
	f = branching_family()
	measured = features.measure(f)
	assert measured['branch_points'] == 1
	assert measured['continuing_children'] == 2
	assert measured['branch_balance'] == pytest.approx(1 / 3)
	assert measured['degree_counts'] == {1: 8, 2: 2, 3: 1, 4: 1, 5: 1}
	assert measured['sibship_variance'] == pytest.approx(2 / 3)
	# Reorder every container and rename people without changing topology.
	names = {p.id: f'new_{p.id}' for p in f.people}
	other = family.Family(
		tuple(dataclasses.replace(p, id=names[p.id], label='Changed') for p in reversed(f.people)),
		tuple(family.Union(names[u.father], names[u.mother],
			tuple(names[c] for c in reversed(u.children))) for u in reversed(f.unions)))
	assert features.measure(other) == measured


def test_terminal_and_shared_descendant_branches_have_defined_measurements() -> None:
	isolated = family.Family((family.Person('a', 'female'),), ())
	measured = features.measure(isolated)
	assert measured['branch_points'] == measured['branch_balance'] == 0
	assert measured['degree_counts'] == {0: 1}
	# The same child below two sibling parents counts once per descendant set.
	f = branching_family()
	f = dataclasses.replace(f, unions=(family.Union('a', 'b', ('c', 'd')),
		family.Union('c', 'd', ('g', 'h'))))
	measured = features.measure(f)
	assert measured['branch_points'] == 1 and measured['branch_balance'] == 1
	assert measured['continuing_children'] == 2
