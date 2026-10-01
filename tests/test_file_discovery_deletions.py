"""Deleted tracked files must not break content-based hygiene discovery."""

import pathlib

import pytest

import file_utils


def test_deleted_files_do_not_reach_content_filters(tmp_path: pathlib.Path,
		monkeypatch: pytest.MonkeyPatch) -> None:
	present = tmp_path / 'present.md'
	present.write_text('content')
	deleted = tmp_path / 'deleted.md'

	def tracked_paths(repo_root: str) -> list[str]:
		return [str(deleted), str(present)]

	def content_filter(relative: str) -> bool:
		return (tmp_path / relative).read_text() == 'content'

	monkeypatch.setattr(file_utils, '_gather_all_paths', tracked_paths)
	files = file_utils.discover_files(extensions=('.md',), extra_filter=content_filter,
		repo_root=str(tmp_path))
	assert files == [str(present)]
