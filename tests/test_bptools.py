#!/usr/bin/env python3

import argparse
import os

import bptools


def test_make_outfile_includes_script_and_parts():
	outfile = bptools.make_outfile("/tmp/my_script.py", "mc", 5, None, "")
	assert outfile == "bbq-my_script-mc-5-questions.txt"


def test_prepare_question_text_validation_and_normalization(capsys):
	assert bptools._prepare_question_text(None, "x") is None

	assert bptools._prepare_question_text(123, "x") is None
	assert "non-string question skipped" in capsys.readouterr().err

	assert bptools._prepare_question_text("", "x") is None
	assert "empty question skipped" in capsys.readouterr().err

	assert bptools._prepare_question_text("a\nb", "x") is None
	assert "internal newline skipped" in capsys.readouterr().err

	assert bptools._prepare_question_text("hello", "x") == "hello\n"
	assert bptools._prepare_question_text("hello\n", "x") == "hello\n"


def test_add_hint_args_default_and_flags():
	parser = argparse.ArgumentParser()
	parser = bptools.add_hint_args(parser, hint_default=True, dest="hint")

	args = parser.parse_args([])
	assert args.hint is True

	args = parser.parse_args(["--no-hint"])
	assert args.hint is False

	args = parser.parse_args(["--hint"])
	assert args.hint is True


def test_add_question_format_args_parses_expected_formats():
	parser = argparse.ArgumentParser()
	parser = bptools.add_question_format_args(parser, types_list=["mc", "num"], required=True)

	args = parser.parse_args(["--mc"])
	assert args.question_type == "mc"

	args = parser.parse_args(["--format", "num"])
	assert args.question_type == "num"


def test_add_question_format_args_invalid_list_raises():
	parser = argparse.ArgumentParser()
	try:
		bptools.add_question_format_args(parser, types_list=["bogus"], required=True)
	except ValueError:
		return
	assert False, "expected ValueError for invalid types_list"


def test_add_question_format_args_default_when_not_required():
	parser = argparse.ArgumentParser()
	parser = bptools.add_question_format_args(parser, types_list=["mc", "num"], required=False, default="num")

	args = parser.parse_args([])
	assert args.question_type == "num"


def test_collect_questions_skips_empty_and_internal_newlines(capsys):
	args = argparse.Namespace(duplicates=3, max_questions=None)
	call_count = 0

	def writer(n, _args):
		nonlocal call_count
		call_count += 1
		if call_count == 1:
			return "hello"
		if call_count == 2:
			return ""
		return "bad\nnews"

	questions = bptools.collect_questions(writer, args, print_histogram_flag=False)
	assert questions == ["hello\n"]

	err = capsys.readouterr().err
	assert "empty question skipped" in err
	assert "internal newline skipped" in err


def test_collect_question_batches_respects_max_questions(capsys):
	args = argparse.Namespace(duplicates=1, max_questions=2)

	def batch_writer(start_num, _args):
		assert start_num == 1
		return ["one", "two", "three"]

	questions = bptools.collect_question_batches(batch_writer, args, print_histogram_flag=False)
	assert questions == ["one\n", "two\n"]
	_ = capsys.readouterr()


def test_append_clear_font_space_helpers():
	text = bptools.append_clear_font_space_to_text("ABC")
	assert "ABC" in text
	assert "font-family: sans-serif" in text

	items = bptools.append_clear_font_space_to_list(["A", "B"])
	assert len(items) == 2
	assert all("font-family: sans-serif" in item for item in items)


def test_get_repo_data_path_points_under_data_dir():
	path = bptools.get_repo_data_path("real_wordles.txt")
	assert os.path.isabs(path)
	assert path.endswith(os.path.join("data", "real_wordles.txt"))
	assert os.path.exists(path)


def test_applyReplacementRulesToText_type_checks():
	try:
		bptools.applyReplacementRulesToText(123, None)
	except TypeError:
		return
	assert False, "expected TypeError for non-string input"


def test_applyReplacementRulesToText_uses_base_rules_and_custom_rules(capsys):
	out = bptools.applyReplacementRulesToText("This is not true ", None)
	assert "NOT" in out
	assert "TRUE" in out
	_ = capsys.readouterr()

	rules = {"XYZ": "abc"}
	out2 = bptools.applyReplacementRulesToText("XYZ", rules)
	assert "<strong>abc</strong>" in out2
	assert " not " in rules


def test_applyReplacementRulesToList_replaces_and_validates():
	original = [" not true ", " false ", "hello"]
	out = bptools.applyReplacementRulesToList(list(original), None)
	assert original == [" not true ", " false ", "hello"]
	assert any("NOT" in item for item in out)
	assert any("FALSE" in item for item in out)

	try:
		bptools.applyReplacementRulesToList(["ok", 123], None)
	except TypeError:
		return
	assert False, "expected TypeError for non-string list element"
