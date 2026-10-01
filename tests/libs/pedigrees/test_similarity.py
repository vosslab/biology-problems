"""Pedigree comparison measures relationships, independently of drawing choices."""

import dataclasses

import pytest
import networkx

import pedigree_lib.family as family
import pedigree_lib.sources as sources
import pedigree_lib.similarity as similarity
import pedigree_lib.graphs as graphs


def example() -> sources.Case:
	# Two founding couples join through their children, with a shared grandchild.
	people = tuple(family.Person(pid, sex) for pid, sex in zip('abcdefg',
		('male', 'female', 'male', 'female', 'male', 'female', 'female')))
	f = family.Family(people, (family.Union('a', 'b', ('e',)),
		family.Union('c', 'd', ('f',)), family.Union('e', 'f', ('g',))))
	return sources.Case(f, {p.id: family.Observation(p.id == 'g') for p in people})


def test_relabeling_and_order_do_not_change_similarity() -> None:
	case = example()
	# Include an actual multi-child sibship so reversing order exercises the invariant.
	case = dataclasses.replace(case, family=dataclasses.replace(case.family,
		people=case.family.people + (family.Person('h', 'male'),),
		unions=case.family.unions[:-1] + (family.Union('e', 'f', ('g', 'h')),)),
		observations={**case.observations, 'h': family.Observation(False)})
	ids = {p.id: str(index) for index, p in enumerate(reversed(case.family.people))}
	people = tuple(dataclasses.replace(p, id=ids[p.id], label='renamed')
		for p in reversed(case.family.people))
	unions = tuple(family.Union(ids[u.father], ids[u.mother],
		tuple(ids[c] for c in reversed(u.children))) for u in reversed(case.family.unions))
	other = sources.Case(family.Family(people, unions),
		{ids[pid]: obs for pid, obs in case.observations.items()},
		genotypes={pid: (1, 1) for pid in ids.values()}, metadata={'answer': 'ignored'})
	result = similarity.compare(case, other)
	assert result.structure == result.visible == 1.0
	assert result.same_structure and result.same_visible


def test_visible_change_preserves_structure_and_symmetry() -> None:
	case = example()
	observations = dict(case.observations)
	observations['g'] = family.Observation(False)
	other = dataclasses.replace(case, observations=observations)
	result = similarity.compare(case, other)
	assert result == similarity.compare(other, case)
	assert result.structure == 1 and result.same_structure
	assert 0 < result.visible < 1 and not result.same_visible


def test_graph_snapshots_and_batch_reuse_do_not_keep_stale_observations() -> None:
	left, right = example(), example()
	graph = graphs.to_networkx(left.family, left.observations)
	graph.remove_node(('person', 'g'))
	graph.nodes[('person', 'a')]['label'] = 'changed'
	fresh = graphs.to_networkx(left.family, left.observations)
	assert ('person', 'g') in fresh
	assert fresh.nodes[('person', 'a')]['label'] != 'changed'
	assert similarity.pairwise([left, right])[0]['same_visible']
	right.observations['g'] = family.Observation(False)
	batch = similarity.pairwise([left, right])[0]
	assert batch['same_structure'] and not batch['same_visible']
	assert batch['visible'] == similarity.compare(left, right).visible


def test_parentage_change_is_detected_with_identical_people_and_traits() -> None:
	case = example()
	unions = (family.Union('a', 'b', ('e', 'f')),
		family.Union('c', 'd', ()), family.Union('e', 'f', ('g',)))
	other = dataclasses.replace(case, family=dataclasses.replace(case.family, unions=unions))
	result = similarity.compare(case, other)
	assert 0 < result.structure < 1 and not result.same_structure
	assert 0 < result.visible < 1 and not result.same_visible


def test_pairwise_reports_each_unordered_pair_once() -> None:
	case = example()
	report = similarity.pairwise([case, case, case])
	assert [(row['left'], row['right']) for row in report] == [(1, 2), (1, 3), (2, 3)]
	assert all(row['same_visible'] for row in report)
	assert similarity.pairwise([]) == []


def test_invalid_observations_are_not_silently_ignored() -> None:
	case = example()
	with pytest.raises(ValueError):
		similarity.compare(case, dataclasses.replace(case, observations={}))


def test_complexity_distinguishes_joined_families_from_shared_ancestry() -> None:
	f = example().family
	joined = similarity.complexity(f)
	assert (joined.generations, joined.founder_couples, joined.joining_unions) == (3, 2, 1)
	assert joined.components == 1 and joined.cycle_rank == 0 and joined.diameter == 6
	# Make the partners siblings; the other founding couple remains disconnected.
	f = dataclasses.replace(f, unions=(family.Union('a', 'b', ('e', 'f')),
		family.Union('c', 'd', ()), family.Union('e', 'f', ('g',))))
	metrics = similarity.complexity(f)
	assert metrics.components == 2 and metrics.cycle_rank == 1
	assert metrics.cycle_rank == len(networkx.cycle_basis(graphs.to_networkx(f)))
	assert joined.sort_key() < metrics.sort_key()
	isolated = similarity.complexity(family.Family((family.Person('x', 'female'),), ()))
	assert isolated.diameter == isolated.cycle_rank == isolated.max_sibship == 0


def test_neighborhood_score_one_does_not_claim_isomorphism() -> None:
	people, unions = [], []
	for i in range(4):
		people.extend(family.Person(f'{role}{i}', sex) for role, sex in
			(('p', 'male'), ('q', 'female'), ('s', 'male'), ('d', 'female')))
		unions.append(family.Union(f'p{i}', f'q{i}', (f's{i}', f'd{i}')))
	cases = []
	for offset in (1, 2):
		marriages = [family.Union(f's{i}', f'd{(i + offset) % 4}', ()) for i in range(4)]
		f = family.Family(tuple(people), tuple(unions + marriages))
		cases.append(sources.Case(f, {p.id: family.Observation(False) for p in people}))
	result = similarity.compare(*cases)
	assert result.structure == result.visible == 1
	assert not result.same_structure and not result.same_visible
