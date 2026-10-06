"""Terminal frontier construction contracts stay separate from biology."""

import dataclasses
import random

import pytest

import pedigree_lib.family as family_model
import pedigree_lib.inheritance as inheritance
import pedigree_lib.layout as layout
import pedigree_lib.questions as questions
import pedigree_lib.scenarios as scenarios
import pedigree_lib.sources as sources
import pedigree_lib.terminal_frontier as terminal_frontier


def frontier_case() -> tuple[family_model.Family, tuple[str, ...]]:
	"""Build a small, deterministic family with three terminal designations."""
	result = sources.frontier_family(random.Random(17), 11, 40, 4,
		seed_couples=2, couples=(4, 10), children=(1, 4), root_children=(2, 4),
		frontier_count=3)
	return result


def test_frontier_is_deep_connected_and_uses_distinct_sibships() -> None:
	family, designated = frontier_case()
	ranks = family.generations()
	parents = family.parentage()
	assert 11 <= len(family.people) <= 40
	assert set(ranks.values()) == {0, 1, 2, 3}
	assert all(ranks[pid] == 3 for pid in designated)
	assert len(designated) == 3
	assert len({parents[pid] for pid in designated}) == len(designated)

	# Family validation also enforces one partner union per person; check connectivity.
	neighbors = {person.id: set() for person in family.people}
	for union in family.unions:
		members = (union.father, union.mother, *union.children)
		for person in members:
			neighbors[person].update(member for member in members if member != person)
	pending = [family.people[0].id]
	connected = set()
	while pending:
		person = pending.pop()
		if person not in connected:
			connected.add(person)
			pending.extend(neighbors[person] - connected)
	assert connected == set(neighbors)


def test_bonus_frontier_respects_deep_family_budgets_and_endpoint_contract() -> None:
	family, designated = sources.frontier_family(random.Random(17), 60, 90, 6,
		seed_couples=3, couples=(20, 20), children=(1, 5), root_children=(2, 5),
		frontier_count=9)
	ranks = family.generations()
	parents = family.parentage()
	assert 60 <= len(family.people) <= 90
	assert len(family.unions) == 20
	assert max(ranks.values()) + 1 == 6
	assert len(designated) == 9
	assert all(ranks[person] == 5 for person in designated)
	assert len({parents[person] for person in designated}) == 9
	for mirror in (False, True):
		diagram = layout.lay_out(family, mirror=mirror)
		assert not layout.layout_errors(diagram)
		assert terminal_frontier.endpoints_match(diagram, designated)

	# Family validation above rejects partner reuse; ensure the full graph is connected.
	neighbors = {person.id: set() for person in family.people}
	for union in family.unions:
		members = (union.father, union.mother, *union.children)
		for person in members:
			neighbors[person].update(member for member in members if member != person)
	pending = [family.people[0].id]
	connected = set()
	while pending:
		person = pending.pop()
		if person not in connected:
			connected.add(person)
			pending.extend(neighbors[person] - connected)
	assert connected == set(neighbors)


@pytest.mark.parametrize('children_per_terminal', (1, 2, 3))
def test_terminal_sibships_allow_singletons_and_multiple_siblings(
		children_per_terminal: int) -> None:
	people = 6 + 2 * children_per_terminal
	family, designated = sources.frontier_family(random.Random(31), people, people, 3,
		seed_couples=1, couples=(3, 3), children=(children_per_terminal, children_per_terminal),
		root_children=(2, 2), frontier_count=2)
	terminal_unions = {family.parentage()[pid] for pid in designated}
	assert len(family.people) == people
	assert len(terminal_unions) == 2
	assert {len(union.children) for union in terminal_unions} == {children_per_terminal}


def test_frontier_layout_keeps_transient_endpoints_on_both_mirrors() -> None:
	family, designated = frontier_case()
	for mirror in (False, True):
		diagram = layout.lay_out(family, mirror=mirror)
		assert not layout.layout_errors(diagram)
		assert terminal_frontier.endpoints_match(diagram, designated)
		assert not terminal_frontier.endpoints_match(diagram, (designated[0],))


def test_impossible_capacity_rejects_before_creating_people(monkeypatch: pytest.MonkeyPatch) -> None:
	def unexpected_person(*args: object) -> None:
		raise AssertionError('capacity rejection must precede Person creation')

	monkeypatch.setattr(sources.family_model, 'Person', unexpected_person)
	with pytest.raises(terminal_frontier.Rejected):
		sources.frontier_family(random.Random(5), 1, 2, 4, seed_couples=2,
			couples=(4, 6), children=(1, 4), root_children=(2, 4), frontier_count=3)
	with pytest.raises(ValueError, match='Generation count'):
		sources.frontier_family(random.Random(5), 11, 40, 2, seed_couples=2,
			couples=(4, 6), children=(1, 4), root_children=(2, 4), frontier_count=3)


def test_simulation_uses_family_biology_without_persisting_designations() -> None:
	family, _designated = frontier_case()
	case = sources.simulate_family(family, 'autosomal dominant', random.Random(21))
	repeated = sources.simulate_family(family, 'autosomal dominant', random.Random(21))
	assert case.family is family
	assert case == repeated
	assert set(case.genotypes) == set(family.members())
	assert set(case.observations) == set(family.members())
	assert {person.sex for person in family.people} == {'male', 'female'}
	parents = family.parentage()
	for person in family.people:
		if person.id in parents:
			union = parents[person.id]
			possible = inheritance.transmissions('autosomal dominant',
				case.genotypes[union.father], case.genotypes[union.mother], person.sex)
			assert case.genotypes[person.id] in possible
		else:
			assert case.genotypes[person.id] in inheritance.genotype_domain(
				'autosomal dominant', person.sex)


@pytest.mark.parametrize('level,question_format,matching,expects_frontier', (
	('bonus', 'identify', False, True), ('easy', 'identify', False, False),
	('easy', 'select', False, False), ('easy', 'match', True, False)))
def test_frontier_policy_only_routes_bonus_identification(level: str,
		question_format: str, matching: bool, expects_frontier: bool,
		monkeypatch: pytest.MonkeyPatch) -> None:
	accepted = scenarios.generate_candidate('autosomal dominant', random.Random(9), 'easy')
	captured: list[tuple[int, ...]] = []

	def candidate(mode: str, rng: random.Random, level: str, matching: bool = False,
			*, frontier_counts: tuple[int, ...] = ()) -> tuple[
				questions.AcceptedCase, tuple[str, ...] | None]:
		captured.append(frontier_counts)
		return accepted, None

	monkeypatch.setattr(scenarios, '_generate_candidate_with_receipt', candidate)
	monkeypatch.setattr(scenarios.downward_repair, 'repair', lambda case, rng: case)
	monkeypatch.setattr(scenarios.polishing, 'polish', lambda case, rng, level, matching: case)
	monkeypatch.setattr(scenarios.difficulty, 'fits_difficulty', lambda family, level, matching: True)
	result = scenarios.generate_pool(random.Random(10), level, matching, count=1,
		question_format=question_format)
	assert result == [accepted]
	assert bool(captured[0]) is expects_frontier


def test_frontier_candidate_survives_when_polishing_moves_another_person_to_an_endpoint(
		monkeypatch: pytest.MonkeyPatch) -> None:
	accepted = scenarios.generate_candidate('autosomal dominant', random.Random(11), 'easy')
	last_y = max(symbol.y for symbol in accepted.diagram.symbols)
	last_row = [symbol for symbol in accepted.diagram.symbols if symbol.y == last_y]
	designated = (min(last_row, key=lambda symbol: symbol.x).person,
		max(last_row, key=lambda symbol: symbol.x).person)
	other = next(person.id for person in accepted.case.family.people
		if person.id not in designated)
	other_symbol = next(symbol for symbol in accepted.diagram.symbols if symbol.person == other)
	shifted = dataclasses.replace(other_symbol, x=min(symbol.x for symbol in last_row) - 100,
		y=last_y)
	polished_diagram = dataclasses.replace(accepted.diagram, symbols=tuple(
		shifted if symbol.person == other else symbol for symbol in accepted.diagram.symbols))
	polished = dataclasses.replace(accepted, diagram=polished_diagram)
	assert terminal_frontier.endpoints_match(accepted.diagram, designated)
	assert not terminal_frontier.endpoints_match(polished.diagram, designated)

	monkeypatch.setattr(scenarios, '_generate_candidate_with_receipt',
		lambda mode, rng, level, matching=False, *, frontier_counts=(): (accepted, designated))
	monkeypatch.setattr(scenarios.downward_repair, 'repair', lambda case, rng: case)
	monkeypatch.setattr(scenarios.polishing, 'polish', lambda case, rng, level, matching: polished)
	monkeypatch.setattr(scenarios.difficulty, 'fits_difficulty', lambda family, level, matching: True)
	result = scenarios.generate_pool(random.Random(12), 'easy', count=1, question_format='identify')
	assert result == [accepted]
