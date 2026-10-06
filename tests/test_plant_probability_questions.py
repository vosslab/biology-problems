"""Protect genetic weighting, distinct answers, and the requested scenario capacity."""

import random
import argparse
import fractions

import pytest
import lib_test_utils


@pytest.mark.parametrize("filename", [
	"two_gene_dominance_probability.py",
	"two_gene_selected_offspring_bonus.py",
])
def test_at_least_100_unique_scenarios_with_distinct_answers(
		filename: str, monkeypatch: pytest.MonkeyPatch) -> None:
	module = lib_test_utils.import_from_repo_path(f"problems/inheritance-problems/{filename}")
	monkeypatch.setattr(module.plantprobabilitylib, "random", random.Random(31415))
	module.SCENARIOS = module.build_scenarios()
	items = [module.write_question(n, argparse.Namespace())
		for n in range(1, len(module.SCENARIOS) + 1)]
	stems = {item.question_text for item in items}
	assert len(stems) == len(items) >= 100
	assert module.write_question(len(items) + 1, argparse.Namespace()) is None
	for item in items:
		values = [fractions.Fraction(choice.rsplit(" = ", 1)[1]) for choice in item.choices_list]
		assert len(set(values)) == len(values)
		assert values == sorted(values)
		assert item.choices_list.count(item.answer_text) == 1
	for scenario, item in zip(module.SCENARIOS, items):
		if filename.endswith("bonus.py"):
			errors = module.distractor_terms(*scenario)
		else:
			errors = module.distractor_terms(scenario[1], scenario[2], scenario[4])
		named_errors = {module.plantprobabilitylib.calculation_text(terms)
			for error, terms in errors if error}
		assert all(c == item.answer_text or c in named_errors for c in item.choices_list)


def test_bonus_weights_genotypes_with_the_same_phenotype() -> None:
	"""Medium offspring occur in a 1:4:1 genotype ratio, not three equal groups."""
	module = lib_test_utils.import_from_repo_path(
		"problems/inheritance-problems/two_gene_selected_offspring_bonus.py")
	selected = module.selected_distribution((1, 1), (1, 1), 2)
	assert selected == {
		(0, 2): fractions.Fraction(1, 6),
		(1, 1): fractions.Fraction(2, 3),
		(2, 0): fractions.Fraction(1, 6),
	}
	terms = module.answer_terms((1, 1), (1, 1), 2, (0, 0), 0)
	assert module.plantprobabilitylib.calculation_value(terms) == fractions.Fraction(1, 6)


def test_regular_adds_disjoint_phenotypes_after_multiplying_gene_probabilities() -> None:
	module = lib_test_utils.import_from_repo_path(
		"problems/inheritance-problems/two_gene_dominance_probability.py")
	# First gene: homozygote OR heterozygote; second gene: heterozygote.
	terms = module.answer_terms((1, 1), (1, 0), ((2, 1), (1, 1)))
	assert module.plantprobabilitylib.calculation_value(terms) == fractions.Fraction(3, 8)
