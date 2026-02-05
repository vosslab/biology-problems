import random

from lib_test_utils import import_from_repo_path


def test_yaml_which_one_mc_to_bbq_builds_questions():
	mod = import_from_repo_path("problems/matching_sets/yaml_which_one_mc_to_bbq.py")

	def fake_format(N, question_text, choices_list, answer_text):
		return f"MC\t{N}\t{answer_text}\t{len(choices_list)}\t{question_text}\n"

	mod.bptools.formatBB_MC_Question = fake_format
	random.seed(0)

	yaml_data = {
		"matching pairs": {
			"enzyme": ["catalyst", "protein"],
			"substrate": ["reactant"],
		},
		"keys description": "terms",
		"values description": "definitions",
		"key description": "term",
		"value description": "definition",
	}

	questions = mod.makeQuestions2(yaml_data, num_choices=2, flip=False)
	assert len(questions) > 0
	assert questions[0].startswith("MC\t")
	assert "Which one of the following" in questions[0]
