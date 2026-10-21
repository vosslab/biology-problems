"""Protect probability mass and chi-square arithmetic used by quiz answer keys."""

import fractions
import itertools
import math

import lib_test_utils


def test_offspring_distribution_counts_every_order():
	module = lib_test_utils.import_from_repo_path(
		"problems/inheritance-problems/progeny_probability_practice.py")
	for number in (2, 3, 4):
		for probability in (fractions.Fraction(1, 2), fractions.Fraction(1, 4),
				fractions.Fraction(2, 3)):
			# Independent oracle: enumerate births instead of using a binomial coefficient.
			expected = [fractions.Fraction(0) for _ in range(number + 1)]
			for sequence in itertools.product((0, 1), repeat=number):
				weight = math.prod(probability if value else 1 - probability for value in sequence)
				expected[sum(sequence)] += weight
			actual = module.distribution(number, probability)
			assert actual == expected
			assert sum(actual) == 1


def test_dice_counts_and_terms_determine_the_decision():
	module = lib_test_utils.import_from_repo_path(
		"problems/inheritance-problems/chi_square/chi_square_dice.py")
	# Video example guards against copying its rounded 9.6 or using six df.
	data = module.dice_data(6, [-4, -2, 2, 3, -3, 4])
	assert data["observed"] == [2, 4, 8, 9, 3, 10]
	assert data["statistic"] == fractions.Fraction(58, 6)
	assert sum(data["observed"]) == data["total"]
	assert data["reject"] is False
	# Same total, concentrated observations: the decision must change.
	data = module.dice_data(6, [-6, 0, 0, 0, 0, 6])
	assert data["statistic"] == 12
	assert data["reject"] is True
