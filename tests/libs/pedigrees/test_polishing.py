"""Polishing must preserve teaching evidence and existing family data."""

import copy
import random

import pedigree_lib.difficulty as difficulty
import pedigree_lib.inheritance as inheritance
import pedigree_lib.layout as layout
import pedigree_lib.polishing as polishing
import pedigree_lib.scenarios as scenarios


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
	assert result.assessment.evidence == original.assessment.evidence
	assert {m: c.compatible for m, c in result.assessment.compatibility.items()} == {
		m: c.compatible for m, c in original.assessment.compatibility.items()}
	assert difficulty.fits_difficulty(result.case.family, 'rigorous')
	assert not layout.layout_errors(result.diagram)
