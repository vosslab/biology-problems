"""Compact bank round trips, hidden carriers, and difficulty-specific replenishment."""

import pathlib
import random
import os

import pytest

import pedigree_lib.cache as cache
import pedigree_lib.difficulty as difficulty
import pedigree_lib.inheritance as inheritance
import pedigree_lib.questions as questions
import pedigree_lib.scenarios as scenarios


@pytest.mark.parametrize('mode', inheritance.MODES)
def test_cached_biology_round_trip_hides_carriers(mode: str) -> None:
	original = scenarios.generate_candidate(mode, random.Random(72), 'easy')
	record = cache.encode(original)
	restored = cache.decode(record, 'easy')
	accepted, reasons = questions.evaluate(restored)
	assert accepted is not None, reasons
	assert cache.encode(accepted) == record
	assert list(restored.genotypes.values()) == [original.case.genotypes[p.id]
		for p in original.case.family.people]
	assert not any(obs.carrier for obs in restored.observations.values())


def test_replenishment_counts_only_eligible_difficulty(tmp_path: pathlib.Path) -> None:
	path = cache.path_for_level('easy', tmp_path)
	scenarios.build(random.Random(41), 'easy', 'identify', pool_size=4, cache_path=path)
	first = cache.read_records(path)
	result = scenarios.build(random.Random(42), 'easy', 'identify', pool_size=6,
		cache_path=path, use_cache=True)
	assert len(result) == len(cache.read_records(path)) == 6
	assert all(record in cache.read_records(path) for record in first)
	medium_path = cache.path_for_level('medium', tmp_path)
	medium = scenarios.build(random.Random(43), 'medium', 'identify', pool_size=3,
		cache_path=medium_path, use_cache=True)
	assert len(cache.read_records(path)) == 6
	assert len(cache.read_records(medium_path)) == 3
	assert all(difficulty.fits_difficulty(row[0].case.family, 'medium') for row in medium)


def test_cache_deduplicates_and_respects_matching_limits(tmp_path: pathlib.Path) -> None:
	path = cache.path_for_level('easy', tmp_path)
	case = scenarios.generate_candidate('autosomal recessive', random.Random(72), 'easy')
	cache.append(path, [case, case])
	cache.append(path, [case])
	assert len(list(cache.candidates(path, random.Random(1), 'easy'))) == 1
	assert list(cache.candidates(path, random.Random(1), 'easy', matching=True)) == []


def test_autosomal_pool_reuses_only_autosomal_cases_from_shared_bank(tmp_path: pathlib.Path) -> None:
	path = cache.path_for_level('easy', tmp_path)
	rng = random.Random(72)
	bank = [scenarios.generate_candidate(mode, rng, 'easy') for mode in inheritance.MODES]
	cache.append(path, bank)
	result = scenarios.build(random.Random(42), 'easy', 'identify', pool_size=2,
		cache_path=path, use_cache=True, modes=inheritance.AUTOSOMAL_MODES)
	assert {row[0].assessment.answer for row in result} == set(inheritance.AUTOSOMAL_MODES)
	assert len(cache.read_records(path)) == len(bank)


def test_impossible_cached_carriers_are_rejected() -> None:
	record = dict(mode='AR', sex='mfmf', affected=[2], carriers=[],
		genotypes=[[0, 1], [0, 1], [1, 1], [0, 0]], families=[[0, 1, [2, 3]]])
	assert cache.decode(record, 'easy') is None
	record['carriers'] = [0, 1]
	assert cache.decode(record, 'easy') is not None


def test_cache_indices_cannot_reference_other_people() -> None:
	record = dict(mode='AR', sex='mfmf', affected=[-1], carriers=[0, 1],
		genotypes=[[0, 1], [0, 1], [1, 1], [0, 0]], families=[[0, 1, [2, 3]]])
	with pytest.raises(ValueError, match='affected indices'):
		cache.decode(record, 'easy')


def test_legacy_cache_cannot_substitute_inferred_parental_crosses() -> None:
	record = dict(mode='AR', sex='mfmf', affected=[2], carriers=[0, 1],
		families=[[0, 1, [2, 3]]])
	assert cache.decode(record, 'easy') is None


def test_cached_original_genotypes_must_have_possible_transmissions() -> None:
	# All are unaffected, but AA x AA cannot produce a hidden Aa carrier.
	record = dict(mode='AR', sex='mfmf', affected=[], carriers=[2],
		genotypes=[[0, 0], [0, 0], [0, 1], [0, 0]], families=[[0, 1, [2, 3]]])
	assert cache.decode(record, 'easy') is None
	record['genotypes'][2] = [False, 1]
	with pytest.raises(ValueError, match='genotype'):
		cache.decode(record, 'easy')


def test_cache_preserves_homozygous_dominant_parental_cross() -> None:
	record = dict(mode='AD', sex='mfmf', affected=[0, 1, 2, 3], carriers=[],
		genotypes=[[0, 1], [1, 1], [1, 1], [0, 1]], families=[[0, 1, [2, 3]]])
	restored = cache.decode(record, 'easy')
	assert list(restored.genotypes.values()) == [(0, 1), (1, 1), (1, 1), (0, 1)]


def test_cached_extreme_sibship_fails_current_teaching_gate() -> None:
	record = dict(mode='AR', sex='mfmmff', affected=[2, 3, 4, 5], carriers=[0, 1],
		genotypes=[[0, 1], [0, 1]] + [[1, 1]] * 4, families=[[0, 1, [2, 3, 4, 5]]])
	case = cache.decode(record, 'easy')
	accepted, reasons = questions.evaluate(case)
	assert accepted is None
	assert 'affected-count tail' in reasons[0]


@pytest.mark.parametrize('age, available', ((86399, True), (86400, False), (86401, False)))
def test_cache_expires_after_24_hours_without_read_refresh(
		tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch, age: int, available: bool) -> None:
	path = cache.path_for_level('easy', tmp_path)
	case = scenarios.generate_candidate('autosomal recessive', random.Random(72), 'easy')
	cache.append(path, [case])
	os.utime(path, (1000, 1000))
	monkeypatch.setattr(cache.time, 'time', lambda: 1000 + age)
	assert bool(list(cache.candidates(path, random.Random(1), 'easy'))) == available
	assert path.exists() == available
	if available:
		assert path.stat().st_mtime == 1000


@pytest.mark.parametrize('use_cache', (True, False))
def test_stale_bank_is_replaced_when_new_pedigrees_are_added(
		tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch, use_cache: bool) -> None:
	path = cache.path_for_level('easy', tmp_path)
	scenarios.build(random.Random(41), 'easy', 'identify', pool_size=2, cache_path=path)
	original = cache.read_records(path)
	os.utime(path, (1000, 1000))
	monkeypatch.setattr(cache.time, 'time', lambda: 87400)
	scenarios.build(random.Random(42), 'easy', 'identify', pool_size=2,
		cache_path=path, use_cache=use_cache)
	assert len(cache.read_records(path)) == 2
	assert not any(record in cache.read_records(path) for record in original)
	assert path.stat().st_mtime > 1000
