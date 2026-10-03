"""Acceptance, source parity, and biological state survive rendering changes."""

import random
import pathlib
import dataclasses
import argparse

import pytest

import pedigree_lib.family as family
import pedigree_lib.policy as policy
import pedigree_lib.layout as layout
import pedigree_lib.sources as sources
import pedigree_lib.questions as questions
import pedigree_lib.difficulty as difficulty
import pedigree_lib.inheritance as inheritance
import pedigree_lib.cli as cli
import pedigree_lib.graphs as graphs
import pedigree_lib.scenarios as scenarios
import networkx


@pytest.mark.parametrize('mode', inheritance.MODES)
@pytest.mark.parametrize('depth', (3, 4, 5))
def test_procedural_case_has_supported_unique_teaching_answer(mode: str, depth: int) -> None:
	case = questions.generate_case(mode, random.Random(351), generations=depth)
	assessment = policy.assess(case.case.family, case.case.observations)
	assert assessment.answer == mode
	assert assessment.compatibility[mode].compatible and assessment.evidence[mode]
	assert not layout.layout_errors(case.diagram)
	assert max(case.case.family.generations().values()) + 1 == depth
	assert not any(obs.carrier for obs in case.case.observations.values())
	males = sum(p.sex == 'male' and case.case.observations[p.id].affected for p in case.case.family.people)
	females = sum(p.sex == 'female' and case.case.observations[p.id].affected for p in case.case.family.people)
	assert policy.sex_balance_acceptable(mode, males, females)


@pytest.mark.parametrize('males,females,accepted', ((2, 1, False), (3, 2, True), (2, 3, True)))
def test_autosomal_balance_filters_otherwise_clear_recessive_cases(males, females, accepted) -> None:
	children = tuple(family.Person(f'c{i}', 'male' if i < males else 'female')
		for i in range(males + females))
	pedigree = family.Family((family.Person('f', 'male'), family.Person('m', 'female')) + children,
		(family.Union('f', 'm', tuple(p.id for p in children)),))
	observations = {p.id: family.Observation(p.id.startswith('c')) for p in pedigree.people}
	assessment = policy.assess(pedigree, observations)
	assert assessment.compatibility['autosomal recessive'].compatible
	assert bool(assessment.evidence['autosomal recessive'])
	assert (assessment.answer == 'autosomal recessive') == accepted
	if not accepted:
		assert 'Affected-sex balance fails' in assessment.reasons[0]


@pytest.mark.parametrize('mode,males,females,accepted', (
	('autosomal dominant', 7, 9, False), ('autosomal recessive', 8, 10, True),
	('x-linked dominant', 2, 3, False), ('x-linked dominant', 2, 2, False),
	('x-linked dominant', 1, 3, True), ('x-linked dominant', 3, 1, False),
	('x-linked recessive', 3, 1, True), ('x-linked recessive', 1, 3, False),
	('x-linked recessive', 4, 2, False), ('x-linked recessive', 6, 3, True),
	('x-linked dominant', 0, 1, False), ('x-linked dominant', 0, 2, True),
	('x-linked recessive', 1, 0, False), ('x-linked recessive', 2, 0, True),
	('y-linked', 1, 0, False), ('y-linked', 2, 0, True),
	('autosomal dominant', 0, 0, False)))
def test_sex_balance_boundaries(mode, males, females, accepted) -> None:
	assert policy.sex_balance_acceptable(mode, males, females) == accepted


@pytest.mark.parametrize('authored', (True, False))
def test_matching_set_is_independently_supported(authored: bool) -> None:
	bank = questions.authored_cases(student=True) if authored else None
	matching = questions.matching_set(random.Random(351), bank)
	assert {case.assessment.answer for case in matching} == set(inheritance.MODES)
	assert all(policy.assess(c.case.family, c.case.observations).answer == c.assessment.answer for c in matching)
	sizes = [len(c.case.family.people) for c in matching]
	assert max(sizes) - min(sizes) <= 3
	assert all(max(c.case.family.generations().values()) == 2 for c in matching)


@pytest.mark.parametrize('extra_generations', (0, 1, 2))
def test_affected_evidence_must_reach_one_of_last_two_generations(extra_generations) -> None:
	# A clear recessive sibship followed by an entirely unaffected side branch.
	people = [family.Person(pid, sex) for pid, sex in (
		('father', 'male'), ('mother', 'female'), ('son', 'male'),
		('daughter', 'female'), ('branch0', 'male'))]
	unions = [family.Union('father', 'mother', ('son', 'daughter', 'branch0'))]
	for i in range(extra_generations):
		people.extend((family.Person(f'mate{i}', 'female'), family.Person(f'branch{i+1}', 'male')))
		unions.append(family.Union(f'branch{i}', f'mate{i}', (f'branch{i+1}',)))
	pedigree = family.Family(tuple(people), tuple(unions))
	visible = {p.id: family.Observation(p.id in ('son', 'daughter')) for p in people}
	assessment = policy.assess(pedigree, visible)
	assert assessment.compatibility['autosomal recessive'].compatible
	assert assessment.evidence['autosomal recessive']
	if extra_generations < 2:
		assert assessment.answer == 'autosomal recessive'
	else:
		accepted, reasons = questions.evaluate(sources.Case(pedigree, visible))
		assert accepted is None
		assert 'last two generations' in reasons[0]


def test_three_generation_xd_can_meet_squared_bias_without_exhaustion() -> None:
	# This seed exhausted 500 attempts with the former four-child root limit.
	case = questions.generate_case('x-linked dominant', random.Random(400074),
		min_people=12, max_people=15, generations=3)
	assert case.assessment.answer == 'x-linked dominant'
	assert 12 <= len(case.case.family.people) <= 15
	assert max(case.case.family.generations().values()) == 2
	assert not layout.layout_errors(case.diagram)
	males = sum(p.sex == 'male' and case.case.observations[p.id].affected for p in case.case.family.people)
	females = sum(p.sex == 'female' and case.case.observations[p.id].affected for p in case.case.family.people)
	assert females > males and (females - males) ** 2 / (males + females) > 0.99


@pytest.mark.parametrize('question_format', ('identify', 'select', 'match'))
@pytest.mark.parametrize('level,autosomal', (
	('easy', False), ('medium', False), ('rigorous', False), ('easy', True)))
def test_question_formats_use_correct_diagrams_and_depths(question_format, level, autosomal, monkeypatch) -> None:
	captured = []
	monkeypatch.setattr(cli, '_save_review', lambda number, directory, cases, color: captured.extend(cases))
	monkeypatch.setattr(cli.bptools, 'formatBB_MC_Question', lambda *values: values)
	monkeypatch.setattr(cli.bptools, 'formatBB_MAT_Question', lambda *values: values)
	rng = random.Random(72)
	modes = inheritance.AUTOSOMAL_MODES if autosomal else inheritance.MODES
	settings = difficulty.difficulty_settings(level, question_format == 'match')
	if question_format == 'identify':
		cases = [scenarios.generate_candidate(rng.choice(modes), rng, level)]
	else:
		founders = rng.randint(*settings['seed_couples'])
		cases = questions.matching_set(rng, generations=rng.choice(settings['generations']),
			min_people=settings['people'][0], max_people=settings['people'][1], seed_couples=founders,
			couples=settings['couples'], children=settings['children'], root_children=settings['root_children'])
		cases = list(scenarios.assemble(cases, question_format, modes)[0])
	options = argparse.Namespace(review_dir='unused', difficulty=level,
		affected_color='black', random_color=False)
	item = cli.write_question(1, options,
		rng, iter([tuple(cases)]), question_format, modes)
	_, prompt, choices, answer = item
	assert 'carrier' not in prompt
	assert len(captured) == (1 if question_format == 'identify' else len(modes))
	assert len(choices) == len(modes)
	assert all(case.assessment.answer in modes for case in captured)
	for case in captured:
		depth = max(case.case.family.generations().values()) + 1
		assert difficulty.fits_difficulty(case.case.family, level, matching=question_format == 'match')
		if question_format == 'match':
			assert depth in (3, 4) if level == 'rigorous' else depth == 3
	if question_format == 'identify':
		assert answer == captured[0].assessment.answer and answer in choices
		assert set(choices) == set(modes)
	elif question_format == 'select':
		index = choices.index(answer)
		assert f'<strong>{captured[index].assessment.answer}</strong>' in prompt
		assert all(drawing.count('class="pedigree-diagram"') == 1 for drawing in choices)
	else:
		assert answer == [case.assessment.answer for case in captured]


def test_bonus_is_one_large_answerable_family(monkeypatch) -> None:
	captured = []
	monkeypatch.setattr(cli, '_save_review', lambda number, directory, cases, color: captured.extend(cases))
	monkeypatch.setattr(cli.bptools, 'formatBB_MC_Question', lambda *values: values)
	options = argparse.Namespace(review_dir='unused', difficulty='bonus',
		affected_color='black', random_color=False)
	rng = random.Random(72)
	prepared = scenarios.generate_candidate('autosomal recessive', rng, 'bonus')
	item = cli.write_question(1, options, rng, iter([(prepared,)]), 'identify')
	assert len(captured) == 1
	case = captured[0]
	assert len(case.case.family.people) >= 30
	assert difficulty.fits_difficulty(case.case.family, 'bonus')
	assert item[-1] == policy.assess(case.case.family, case.case.observations).answer
	assert not any(obs.carrier for obs in case.case.observations.values())
	assert not layout.layout_errors(case.diagram)
	with pytest.raises(ValueError, match='one pedigree'):
		scenarios.build(random.Random(72), 'bonus', 'match', pool_size=1)


def test_student_bank_hides_carriers_and_excludes_disconnected_cases(monkeypatch) -> None:
	bank = questions.authored_cases()
	cases = [dataclasses.replace(item.case, observations={
		pid: dataclasses.replace(obs, carrier=not obs.affected)
		for pid, obs in item.case.observations.items()}) for item in bank]
	monkeypatch.setattr(sources, 'load_cases', lambda path: cases)
	students = questions.authored_cases(student=True)
	assert len(students) < len(cases)
	assert {item.assessment.answer for item in students} == set(inheritance.MODES)
	for item in students:
		assert len(graphs.components(item.case.family)) == 1
		assert not any(obs.carrier for obs in item.case.observations.values())
		assert policy.assess(item.case.family, item.case.observations).answer == item.assessment.answer
	assert any(obs.carrier for case in cases for obs in case.observations.values())


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


@pytest.mark.parametrize('seeds', (1, 2, 3))
def test_constructor_joins_seed_families_and_honors_couple_budget(seeds) -> None:
	pedigree = sources.procedural_family(random.Random(93), min_people=24, max_people=28,
		generations=4, seed_couples=seeds, couples=(7, 7), children=(1, 3), root_children=(2, 4))
	ranks = pedigree.generations()
	roots = [u for u in pedigree.unions if ranks[u.father] == ranks[u.mother] == 0]
	assert len(roots) == seeds and len(pedigree.unions) == 7
	assert max(ranks.values()) == 3 and 24 <= len(pedigree.people) <= 28
	assert networkx.is_connected(graphs.to_networkx(pedigree))
	for union in pedigree.unions:
		low, high = (2, 4) if union in roots else (1, 3)
		assert low <= len(union.children) <= high
		assert not pedigree.ancestors(union.father) & pedigree.ancestors(union.mother)
	with pytest.raises(ValueError, match='couple/child counts'):
		sources.procedural_family(random.Random(93), seed_couples=3, couples=(4, 4), generations=3)


def test_constructor_supports_exact_child_and_population_bounds() -> None:
	pedigree = sources.procedural_family(random.Random(19), min_people=18, max_people=18,
		generations=4, seed_couples=2, couples=(5, 5), children=(2, 2), root_children=(3, 3))
	ranks = pedigree.generations()
	assert len(pedigree.people) == 18 and len(pedigree.unions) == 5
	assert all(len(u.children) == (3 if ranks[u.father] == 0 else 2) for u in pedigree.unions)


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
