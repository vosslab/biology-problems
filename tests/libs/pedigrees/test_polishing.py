"""Polishing must preserve teaching evidence and existing family data."""

import copy
import random

import pedigree_lib.difficulty as difficulty
import pedigree_lib.downward_repair as downward_repair
import pedigree_lib.geometry_features as geometry_features
import pedigree_lib.inheritance as inheritance
import pedigree_lib.layout as layout
import pedigree_lib.polishing as polishing
import pedigree_lib.scenarios as scenarios
import pedigree_lib.sources as sources


def test_polishing_adds_only_valid_terminal_children_without_changing_evidence() -> None:
	original = scenarios.generate_candidate('autosomal dominant', random.Random(20261010), 'rigorous')
	snapshot = copy.deepcopy(original)
	result = polishing.polish(original, random.Random(1), 'rigorous')
	assert original == snapshot
	assert len(result.case.family.people) > len(original.case.family.people)
	old_ids = set(original.case.family.members())
	for pid in old_ids:
		assert result.case.observations[pid] == original.case.observations[pid]
		assert result.case.genotypes[pid] == original.case.genotypes[pid]
	for old, new in zip(original.case.family.unions, result.case.family.unions, strict=True):
		assert (old.father, old.mother) == (new.father, new.mother)
		assert new.children[:len(old.children)] == old.children
		for child in set(new.children) - old_ids:
			assert result.case.genotypes[child] in inheritance.transmissions(result.assessment.answer,
				result.case.genotypes[new.father], result.case.genotypes[new.mother],
				result.case.family.members()[child].sex)
	assert result.assessment.answer == original.assessment.answer
	assert {m: bool(e) for m, e in result.assessment.evidence.items()} == {
		m: bool(e) for m, e in original.assessment.evidence.items()}
	assert {m: c.compatible for m, c in result.assessment.compatibility.items()} == {
		m: c.compatible for m, c in original.assessment.compatibility.items()}
	assert difficulty.fits_difficulty(result.case.family, 'rigorous')
	assert not layout.layout_errors(result.diagram)


def test_polishing_keeps_either_sampled_outcome_without_changing_placement(monkeypatch) -> None:
	# Evidence includes diagnostic counts: those must not veto an affected addition.
	original = scenarios.generate_candidate('autosomal recessive', random.Random(202610020000), 'rigorous')
	results = []
	for affected in (False, True):
		rng = random.Random(3)
		def draw(values):
			if isinstance(values[0], tuple):
				return max(values) if affected else min(values)
			return values[0]
		monkeypatch.setattr(rng, 'choice', draw)
		result = polishing.polish(original, rng, 'rigorous')
		added = set(result.case.observations) - set(original.case.observations)
		assert added
		assert all(result.case.observations[pid].affected == affected for pid in added)
		assert result.assessment.answer == original.assessment.answer
		results.append(result)
	assert results[0].case.family == results[1].case.family


def test_downward_repair_returns_original_after_one_rejected_sample(monkeypatch) -> None:
	original = scenarios.generate_candidate('autosomal dominant', random.Random(4), 'rigorous')
	snapshot = copy.deepcopy(original)
	assert (geometry_features.bottom_empty_space(original.diagram)['score']
		> geometry_features.BOTTOM_EMPTY_TARGET)
	evaluations = []
	samples = []

	def reject(candidate: sources.Case, mirror: bool = False) -> tuple[None, tuple[str, ...]]:
		evaluations.append(candidate)
		return None, ('forced acceptance failure',)

	apply_growth = downward_repair._apply
	def sample_once(candidate: sources.Case, mode: str, recipe: dict,
			rng: random.Random) -> sources.Case:
		samples.append(recipe)
		return apply_growth(candidate, mode, recipe, rng)

	monkeypatch.setattr(downward_repair.questions, 'evaluate', reject)
	monkeypatch.setattr(downward_repair, '_apply', sample_once)
	result = downward_repair.repair(original, random.Random(1))
	assert result is original
	assert len(evaluations) == 1
	assert len(samples) == 1
	assert original == snapshot
