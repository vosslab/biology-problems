"""Remove Rust `#[cfg(test)]` symbols from a Graphify graph before clustering.

Graphify's Rust extractor indexes the contents of `#[cfg(test)] mod tests` as
production symbols: its `walk()` reaches `mod_item` through a generic fallback
and never inspects an `attribute_item`. Rust convention puts unit tests inline
in the same `src/*.rs` file as the code they exercise, so no `.graphifyignore`
rule can exclude them without dropping that production code too.

Left in place they distort everything downstream: community detection, hub
degree ranking, and cross-community connector spread. Filtering them at print
time hides the symptom while the graph stays wrong, so this module removes them
from `graph.json` between extraction and clustering instead.

Spans are found with tree-sitter rather than regex or brace counting, because a
brace scan has to reason about strings, comments, and nested modules to be
correct, and the Rust grammar already does.
"""

# Standard Library
import re
import json
import pathlib

# PIP3 modules
import tree_sitter
import tree_sitter_rust


RUST_FILE_SUFFIX = ".rs"
SOURCE_LOCATION_PATTERN = re.compile(r"^L(\d+)")
CFG_TEST_ATTRIBUTE = "cfg(test)"
TEST_ATTRIBUTE_SUFFIX = "test"
ATTRIBUTE_NODE_TYPE = "attribute_item"
MODULE_NODE_TYPE = "mod_item"
FUNCTION_NODE_TYPE = "function_item"
GRAPH_EDGES_FIELD = "edges"


#============================================


def build_rust_parser() -> tree_sitter.Parser:
	"""Return a parser for the Rust grammar Graphify already depends on."""
	language = tree_sitter.Language(tree_sitter_rust.language())
	parser = tree_sitter.Parser(language)
	return parser


#============================================


def attribute_marks_test(attribute_text: str) -> bool:
	"""Return whether an attribute marks the item after it as test-only.

	Matches `#[cfg(test)]` on modules and `#[test]` on functions. The suffix
	check also covers namespaced runners such as `#[tokio::test]`.
	"""
	collapsed_text = "".join(attribute_text.split())
	if CFG_TEST_ATTRIBUTE in collapsed_text:
		return True
	inner_text = collapsed_text.strip("#[]")
	marks_test = inner_text.endswith(TEST_ATTRIBUTE_SUFFIX)
	return marks_test


#============================================


def preceding_attribute_texts(node: tree_sitter.Node, source: bytes) -> list[str]:
	"""Return the text of every attribute immediately preceding one item."""
	attribute_texts = []
	sibling = node.prev_named_sibling
	while sibling is not None and sibling.type == ATTRIBUTE_NODE_TYPE:
		attribute_texts.append(source[sibling.start_byte:sibling.end_byte].decode("utf-8"))
		sibling = sibling.prev_named_sibling
	return attribute_texts


#============================================


def test_spans_in_source(source: bytes, parser: tree_sitter.Parser) -> list[tuple[int, int]]:
	"""Return inclusive one-based line spans covering test-only Rust items.

	Args:
		source: Raw bytes of one Rust source file.
		parser: A parser built for the Rust grammar.

	Returns:
		Line spans for `#[cfg(test)]` modules and `#[test]` functions.
	"""
	tree = parser.parse(source)
	spans = []
	pending = [tree.root_node]
	while pending:
		node = pending.pop()
		if node.type in (MODULE_NODE_TYPE, FUNCTION_NODE_TYPE):
			attribute_texts = preceding_attribute_texts(node, source)
			if any(attribute_marks_test(text) for text in attribute_texts):
				# tree-sitter points are zero-based; graph locations are one-based.
				spans.append((node.start_point[0] + 1, node.end_point[0] + 1))
				# The whole item is excluded, so its children need no visit.
				continue
		pending.extend(node.named_children)
	return spans


#============================================


def node_source_line(node: dict) -> int | None:
	"""Return the one-based line a graph node was extracted from."""
	source_location = node.get("source_location")
	if not isinstance(source_location, str):
		return None
	match = SOURCE_LOCATION_PATTERN.match(source_location)
	if match is None:
		return None
	return int(match.group(1))


#============================================


def rust_source_files(graph_data: dict) -> list[str]:
	"""Return the distinct Rust files the graph drew symbols from."""
	source_files = set()
	for node in graph_data["nodes"]:
		source_file = node.get("source_file")
		if isinstance(source_file, str) and source_file.endswith(RUST_FILE_SUFFIX):
			source_files.add(source_file)
	return sorted(source_files)


#============================================


def collect_test_spans(
	graph_data: dict,
	repo_root: pathlib.Path,
) -> dict[str, list[tuple[int, int]]]:
	"""Map each Rust source file to the line spans holding test-only items."""
	parser = build_rust_parser()
	spans_by_file = {}
	for source_file in rust_source_files(graph_data):
		# ASVS 5.3.2: paths come from the graph and resolve beneath the repo root.
		source_path = repo_root / source_file
		if not source_path.is_file():
			continue
		spans = test_spans_in_source(source_path.read_bytes(), parser)
		if spans:
			spans_by_file[source_file] = spans
	return spans_by_file


#============================================


def node_is_test_only(node: dict, spans_by_file: dict[str, list[tuple[int, int]]]) -> bool:
	"""Return whether one graph node was extracted from a test-only span."""
	source_file = node.get("source_file")
	if not isinstance(source_file, str) or source_file not in spans_by_file:
		return False
	line = node_source_line(node)
	if line is None:
		return False
	for start_line, end_line in spans_by_file[source_file]:
		if start_line <= line <= end_line:
			return True
	return False


#============================================


def prune_graph_data(graph_data: dict, repo_root: pathlib.Path) -> dict:
	"""Drop test-only nodes and any link that touched them.

	Nodes with an empty source file are kept deliberately: those are the
	sourceless cross-file stubs the extractor emits so the corpus-level rewire
	can collapse them onto real definitions.

	Args:
		graph_data: Parsed Graphify node-link graph, modified in place.
		repo_root: Repository root the graph's source paths resolve against.

	Returns:
		Counts of the nodes and links removed.
	"""
	spans_by_file = collect_test_spans(graph_data, repo_root)
	if not spans_by_file:
		return {"removed_nodes": 0, "removed_links": 0}

	kept_nodes = []
	removed_ids = set()
	for node in graph_data["nodes"]:
		if node_is_test_only(node, spans_by_file):
			removed_ids.add(node["id"])
			continue
		kept_nodes.append(node)

	kept_links = []
	for link in graph_data[GRAPH_EDGES_FIELD]:
		if link["source"] in removed_ids or link["target"] in removed_ids:
			continue
		kept_links.append(link)

	summary = {
		"removed_nodes": len(graph_data["nodes"]) - len(kept_nodes),
		"removed_links": len(graph_data[GRAPH_EDGES_FIELD]) - len(kept_links),
	}
	graph_data["nodes"] = kept_nodes
	graph_data[GRAPH_EDGES_FIELD] = kept_links
	return summary


#============================================


def prune_graph_file(graph_path: pathlib.Path, repo_root: pathlib.Path) -> dict:
	"""Prune test symbols from a graph file in place and report the counts."""
	# ASVS 5.3.2: the graph path is fixed beneath the generated output directory.
	graph_data = json.loads(graph_path.read_text(encoding="utf-8"))
	summary = prune_graph_data(graph_data, repo_root)
	if summary["removed_nodes"] or summary["removed_links"]:
		graph_path.write_text(json.dumps(graph_data), encoding="utf-8")
	return summary
