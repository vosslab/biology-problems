"""Rank only accepted cases, preserve comparable sets, and consume without cycling."""

import argparse
import dataclasses
import random

import pytest

import pedigree_lib.cli as cli
import pedigree_lib.difficulty as difficulty
import pedigree_lib.inheritance as inheritance
import pedigree_lib.policy as policy
import pedigree_lib.questions as questions
import pedigree_lib.ranking as ranking
import pedigree_lib.scenarios as scenarios


def test_density_ranking_uses_native_width_and_preserves_accepted_cases(monkeypatch) -> None:
	case = questions.generate_case('autosomal recessive', random.Random(351))
	wide = dataclasses.replace(case, diagram=dataclasses.replace(case.diagram, width=2 * case.diagram.width))
	monkeypatch.setattr(scenarios, 'generate_pool', lambda *values: [wide, case])
	prepared = scenarios.build(random.Random(1), 'medium', 'identify')
	assert prepared == [(case,), (wide,)]
	assert ranking.score(case) == pytest.approx(2 * ranking.score(wide))
	assert prepared[0][0].case is case.case and prepared[1][0].assessment is case.assessment
	# Equal drawing widths must still distinguish person counts, unlike raw-width ranking.
	larger = questions.generate_case('autosomal recessive', random.Random(352),
		min_people=20, max_people=20, generations=4)
	larger = dataclasses.replace(larger, diagram=dataclasses.replace(larger.diagram, width=wide.diagram.width))
	assert ranking.score(larger) > ranking.score(wide)


@pytest.mark.parametrize('question_format', ('select', 'match'))
def test_sets_use_best_eligible_mode_entries_once_and_skip_incomplete_groups(question_format) -> None:
	first = questions.matching_set(random.Random(351))
	second = [dataclasses.replace(case, diagram=dataclasses.replace(case.diagram,
		width=case.diagram.width + 100)) for case in first]
	incomplete = questions.generate_case('autosomal recessive', random.Random(9), generations=4)
	result = scenarios.assemble([incomplete] + first + second, question_format)
	assert len(result) == 2
	assert {id(case) for case in result[0]} == {id(case) for case in first}
	assert {id(case) for case in result[1]} == {id(case) for case in second}
	for group in result:
		assert {case.assessment.answer for case in group} == set(inheritance.MODES)
		assert len({scenarios.comparable_key(case) for case in group}) == 1
	assert len({id(case) for group in result for case in group}) == 10


def test_writer_consumes_next_scenario_when_collector_retries_same_number(monkeypatch) -> None:
	first, second = questions.matching_set(random.Random(351))[:2]
	captured = []
	monkeypatch.setattr(cli, '_save_review', lambda number, directory, cases: captured.extend(cases))
	monkeypatch.setattr(cli.bptools, 'formatBB_MC_Question', lambda *values: values)
	remaining = iter([(first,), (second,)])
	options = argparse.Namespace(review_dir='unused')
	rng = random.Random(351)
	cli.write_question(1, options, rng, remaining, 'identify')
	cli.write_question(1, options, rng, remaining, 'identify')
	assert captured == [first, second]
	assert cli.write_question(2, options, rng, remaining, 'identify') is None


def test_generated_pool_keeps_existing_acceptance_and_difficulty() -> None:
	pool = scenarios.generate_pool(random.Random(19), 'medium', count=5)
	assert len(pool) == 5
	for case in pool:
		assert difficulty.fits_difficulty(case.case.family, 'medium')
		assert policy.assess(case.case.family, case.case.observations).answer == case.assessment.answer
		assert not any(obs.carrier for obs in case.case.observations.values())
