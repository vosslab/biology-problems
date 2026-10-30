# Standard Library
import ast
import re

# PIP3 modules
import pytest

# local repo modules
import file_utils


STANDALONE_PREVIEWS = {
	"problems/biochemistry-problems/PUBCHEM/AMINO_ACIDS/generate_alpha_amino_acid_review_html.py",
	"problems/inheritance-problems/phylogenetic_trees/make_all_gene_trees.py",
}
MARKUP_RULES = (
	(re.compile(r"<\s*[a-z][^>]*?(?<![\w:-])class\s*=", re.IGNORECASE), 'class="..."'),
	(re.compile(r"<\s*style\b", re.IGNORECASE), "<style> block"),
	(re.compile(r"<\s*link\b(?=[^>]*\brel\s*=\s*['\"]?stylesheet\b)[^>]*>", re.IGNORECASE), "stylesheet <link>"),
)


#============================================
def is_blackboard_source(rel: str) -> bool:
	"""Select Blackboard-bound question sources, not PGML or local previews."""
	if not rel.startswith("problems/") or not rel.endswith((".py", ".yaml", ".yml")):
		return False
	# PGML supports classes; its converter is outside Blackboard Ultra's HTML contract.
	if rel.endswith("_to_pgml.py"):
		return False
	# These files render standalone/local previews rather than Blackboard question HTML.
	if "/visual_sampler/" in rel or rel in STANDALONE_PREVIEWS:
		return False
	return True


FILES = file_utils.discover_files(
	extensions=(".py", ".yaml", ".yml"),
	extra_filter=is_blackboard_source,
	test_key="blackboard_inline_styles",
)


#============================================
def markup_violations(text: str, first_line: int = 1) -> list[tuple[int, str]]:
	"""Return forbidden Blackboard markup with source-relative line numbers."""
	violations = []
	for pattern, label in MARKUP_RULES:
		for match in pattern.finditer(text):
			line_no = first_line + text.count("\n", 0, match.start())
			violations.append((line_no, label))
	return violations


#============================================
def tree_violations(tree: ast.Module) -> list[tuple[int, str]]:
	"""Scan decoded Python strings and ElementTree class assignments."""
	violations = []
	for node in ast.walk(tree):
		if isinstance(node, ast.Constant) and isinstance(node.value, str):
			violations.extend(markup_violations(node.value, node.lineno))
		if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
			continue
		if node.func.attr.lower() != "set" or not node.args:
			continue
		attribute = node.args[0]
		if isinstance(attribute, ast.Constant) and isinstance(attribute.value, str):
			if attribute.value.lower() == "class":
				violations.append((node.lineno, ".set('class', ...)"))
	return sorted(set(violations))


#============================================
def python_violations(path: str) -> list[tuple[int, str]]:
	"""Parse one Python source file before applying the AST scanner."""
	tree, error = file_utils.parse_source(path)
	assert error is None, f"{path}: cannot scan invalid Python: {error}"
	return tree_violations(tree)


#============================================
def source_violations(path: str) -> list[tuple[int, str]]:
	"""Dispatch between AST-decoded Python and raw YAML source scanning."""
	if path.endswith(".py"):
		return python_violations(path)
	return markup_violations(file_utils.read_source(path))


#============================================
@pytest.mark.parametrize(
	("source", "expected"),
	[
		('<td style="color: #246;">+</td>', []),
		('<td data-class="marker">pythonclass</td>', []),
		('<svg CLASS=marker></svg>', [(1, 'class="..."')]),
		('<style>td { color: red; }</style>', [(1, "<style> block")]),
		('<link rel="stylesheet" href="quiz.css">', [(1, "stylesheet <link>")]),
	],
)
def test_markup_violations(source: str, expected: list[tuple[int, str]]) -> None:
	"""Keep the small classifier aligned with Blackboard's inline-style rule."""
	assert markup_violations(source) == expected


#============================================
def test_tree_violations_detects_elementtree_class() -> None:
	"""Catch SVG/HTML builders that assign class through ElementTree."""
	assert tree_violations(ast.parse("node.set('class', 'marker')")) == [
		(1, ".set('class', ...)")
	]
	assert tree_violations(ast.parse('value = f"<td class={kind}>"')) == [
		(1, 'class="..."')
	]


#============================================
def test_pgml_sources_are_exempt() -> None:
	"""PGML's permitted CSS must not inherit the Blackboard-only restriction."""
	assert not is_blackboard_source("problems/matching_sets/yaml_match_to_pgml.py")
	assert is_blackboard_source("problems/matching_sets/yaml_match_to_bbq.py")


#============================================
@pytest.mark.parametrize("path", FILES, ids=file_utils.rel_to_root)
def test_blackboard_sources_use_inline_styles(path: str) -> None:
	"""Reject CSS classes and stylesheet machinery in Blackboard-bound sources."""
	rel = file_utils.rel_to_root(path)
	issues = source_violations(path)
	message = "\n".join(
		f"{rel}:{line_no}: {label}; use style=\"...\" on the element instead. "
		"Fix the generator, rather than hiding the output."
		for line_no, label in issues
	)
	assert not issues, message
