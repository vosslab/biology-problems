from lib_test_utils import import_from_repo_path


def test_curated_crosses_have_correct_and_inferable_offspring_profiles():
	horse_question = import_from_repo_path(
		"problems/inheritance-problems/horse_coat_pattern_inference.py"
	)
	expected_profiles = (
		{"lethal": 4, "fewspot": 3, "both": 4, "frame": 2, "leopard": 2, "solid": 1},
		{"lethal": 4, "fewspot": 0, "both": 4, "frame": 4, "leopard": 2, "solid": 2},
		{"lethal": 4, "fewspot": 6, "both": 4, "frame": 0, "leopard": 2, "solid": 0},
		{"lethal": 0, "fewspot": 4, "both": 4, "frame": 2, "leopard": 4, "solid": 2},
		{"lethal": 0, "fewspot": 8, "both": 4, "frame": 0, "leopard": 4, "solid": 0},
		{"lethal": 0, "fewspot": 8, "both": 4, "frame": 0, "leopard": 4, "solid": 0},
	)
	assert len(horse_question.SCENARIOS) == len(expected_profiles)

	for scenario, expected_profile in zip(
		horse_question.SCENARIOS, expected_profiles
	):
		known_parent, correct_unknown_parent = scenario
		profile = horse_question.offspring_profile(*scenario)
		matching_parents = [
			candidate
			for candidate in horse_question.PARENT_GENOTYPES
			if horse_question.offspring_profile(known_parent, candidate) == profile
		]
		assert profile == expected_profile
		assert sum(profile.values()) == 16
		assert matching_parents == [correct_unknown_parent]
