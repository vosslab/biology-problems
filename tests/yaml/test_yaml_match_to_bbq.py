import random

from lib_test_utils import import_from_repo_path


def test_yaml_match_to_bbq_builds_questions():
	mod = import_from_repo_path("problems/matching_sets/yaml_match_to_bbq.py")

	def fake_format(N, question_text, answers_list, matching_list):
		return f"MAT\t{N}\t{question_text}\t{len(answers_list)}\t{len(matching_list)}\n"

	mod.bptools.formatBB_MAT_Question = fake_format
	random.seed(0)

	yaml_data = {
		"matching pairs": {
			"A": "alpha",
			"B": "beta",
			"C": "gamma",
		},
		"keys description": "letters",
		"values description": "names",
	}

	questions = mod.permuteMatchingPairs(yaml_data, num_choices=2, max_questions=3)
	assert len(questions) > 0
	assert questions[0].startswith("MAT\t")
	assert "Match each of the following" in questions[0]
