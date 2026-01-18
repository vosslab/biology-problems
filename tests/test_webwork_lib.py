#!/usr/bin/env python3

import importlib.util
import pathlib


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
LIB_PATH = REPO_ROOT / "webwork_lib.py"
spec = importlib.util.spec_from_file_location("webwork_lib", LIB_PATH)
webwork_lib = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(webwork_lib)


#============================================
def test_escape_perl_string():
	"""
	Ensure single-quote escaping works for Perl strings.
	"""
	text = "alpha'beta\\gamma\ndelta"
	escaped = webwork_lib.escape_perl_string(text)
	assert escaped == "alpha\\'beta\\\\gamma\\ndelta"


#============================================
def test_escape_perl_string_noop():
	"""
	Ensure strings with no special characters are unchanged.
	"""
	text = "simple text"
	assert webwork_lib.escape_perl_string(text) == "simple text"


#============================================
def test_escape_perl_string_backslash():
	"""
	Ensure backslashes are escaped.
	"""
	text = "path\\to\\file"
	assert webwork_lib.escape_perl_string(text) == "path\\\\to\\\\file"


#============================================
def test_escape_perl_string_quote():
	"""
	Ensure single quotes are escaped.
	"""
	text = "Bob's enzyme"
	assert webwork_lib.escape_perl_string(text) == "Bob\\'s enzyme"


#============================================
def test_escape_perl_string_newlines():
	"""
	Ensure newlines are normalized and escaped.
	"""
	text = "line1\r\nline2\rline3\nline4"
	assert webwork_lib.escape_perl_string(text) == "line1\\nline2\\nline3\\nline4"


#============================================
def test_escape_perl_string_combined():
	"""
	Ensure combined escapes are handled together.
	"""
	text = "a\\b's\r\nc"
	assert webwork_lib.escape_perl_string(text) == "a\\\\b\\'s\\nc"


#============================================
def test_perl_array_nested():
	"""
	Ensure nested arrays render as Perl array refs.
	"""
	data = [["alpha", "beta"], ["gamma"]]
	perl_text = webwork_lib.perl_array("items", data)
	assert perl_text.startswith("@items = (")
	assert "'alpha'" in perl_text
	assert "'beta'" in perl_text
	assert "'gamma'" in perl_text
	assert "[" in perl_text


#============================================
def test_perl_hash_nested():
	"""
	Ensure nested hashes render as Perl hash refs.
	"""
	data = {
		"alpha": ["one", "two"],
		"beta": {"inner": "yes"},
	}
	perl_text = webwork_lib.perl_hash("stuff", data)
	assert perl_text.startswith("%stuff = (")
	assert "'alpha' => [" in perl_text
	assert "'beta' => {" in perl_text
	assert "'inner' => 'yes'" in perl_text
