"""Shipped libraries must import without missing dependencies or initialization errors."""

import pytest

import file_utils
from lib_test_utils import import_from_repo_path


LIB_FILES = [
	path for path in file_utils.discover_files(extensions=(".py",))
	if path.endswith("lib.py")
]


@pytest.mark.parametrize("lib_path", LIB_FILES, ids=file_utils.rel_id)
def test_import_lib_module(lib_path: str):
	import_from_repo_path(file_utils.rel_to_root(lib_path))
