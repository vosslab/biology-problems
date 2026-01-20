
from lib_test_utils import import_from_repo_path


def test_deletionlib_small_helpers():
	deletionlib = import_from_repo_path("problems/inheritance-problems/deletion_mutants/deletionlib.py")
	assert deletionlib.ensure_most_alphabetical(["a", "b", "c"]) == ["a", "b", "c"]
	assert deletionlib.ensure_most_alphabetical(["c", "b", "a"]) == ["a", "b", "c"]
	assert deletionlib.insertCommas("ABCDEF", 2) == "AB,CD,EF"
	assert deletionlib.insertCommas("ABCDE", 3) == "ABC,DE"


def test_deletionlib_fib_answer_variations_smoke():
	deletionlib = import_from_repo_path("problems/inheritance-problems/deletion_mutants/deletionlib.py")
	variations = deletionlib.generate_fib_answer_variations(["a", "b", "c", "d"])
	assert "abcd" in variations
	assert "a,b,c,d" in variations
