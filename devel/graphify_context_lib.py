"""Shared loaders and formatters for Graphify manager orientation.

Backs devel/graphify_map_repo.py the way changelog_lib.py backs the changelog
tools. This module owns every Graphify artifact path, the sidecar loaders and
their validation, and the deterministic orientation text. The companion script
owns the command line, the Graphify subprocess lifecycle, and main().
"""

# Standard Library
import re
import json
import pathlib
import datetime


OUTPUT_DIR_NAME = "graphify-out"
ANALYSIS_FILE_NAME = ".graphify_analysis.json"
LABELS_FILE_NAME = ".graphify_labels.json"
GRAPH_FILE_NAME = "graph.json"
REPORT_FILE_NAME = "GRAPH_REPORT.md"
MANAGER_CONTEXT_FILE_NAME = "MANAGER_CONTEXT.md"
NEEDS_UPDATE_FILE_NAME = "needs_update"
LESSONS_FILE_PATH = "reflections/LESSONS.md"
MAX_COMMUNITIES = 8
MAX_BRIDGE_SYMBOLS = 4
MAX_CONNECTOR_COMMUNITIES = 8
MAX_RELATIONSHIPS = 3
MAX_GOD_NODES = 5

# A symbol wired into a large share of the map is a utility type, not a
# navigational bridge. The ratio rejects those; the floor keeps a small map from
# rejecting every connector it has.
MAX_CONNECTOR_SPREAD_RATIO = 0.25
MIN_CONNECTOR_SPREAD = 3

# Universally uninformative call targets. Keep this short and language-neutral:
# a growing per-language standard-library blocklist belongs in Graphify's own
# extractors, not in a wrapper that must serve every repository type.
TRIVIAL_SYMBOL_NAMES = frozenset({
	"time", "len", "print", "str", "new", "clone", "default",
})

# Test evidence carried by symbol names and by Graphify's recorded source files.
TEST_NAME_SEGMENTS = ("::tests::", "::test::", ".tests.", ".test.")
TEST_PATH_SEGMENTS = ("tests/", "test/", "spec/")
TEST_FILE_SUFFIXES = (
	"_test.py", "_test.go", "_test.rs", "_test.rb",
	".test.ts", ".test.js", ".spec.ts", ".spec.js",
)


#============================================


def normalize_symbol_name(value: str) -> str:
	"""Return a bare symbol name from a Graphify display label."""
	normalized = clean_graph_text(value).lstrip(".")
	if normalized.endswith("()"):
		normalized = normalized[:-2]
	return normalized


#============================================


def is_test_symbol(name: str, source_files: tuple[str, ...] = ()) -> bool:
	"""Return whether a symbol is test scaffolding rather than production code.

	Graphify records each surprise endpoint's originating file, so both the
	symbol name and its path are available as evidence. This complements
	.graphifyignore rather than duplicating it: the ignore file excludes whole
	directories, while inline test modules living beside production code in the
	same file can only be recognized here.

	Args:
		name: Graphify display label, for example "test_login()" or ".helper()".
		source_files: Recorded source paths for the symbol, when available.

	Returns:
		True when the symbol carries test evidence.
	"""
	normalized = normalize_symbol_name(name)
	lowered = normalized.lower()
	if lowered.startswith("test_") or lowered.endswith("_test"):
		return True
	if any(segment in lowered for segment in TEST_NAME_SEGMENTS):
		return True
	for source_file in source_files:
		path_text = clean_graph_text(source_file).replace("\\", "/").lower()
		if not path_text:
			continue
		if any(path_text.endswith(suffix) for suffix in TEST_FILE_SUFFIXES):
			return True
		if any(path_text.startswith(segment) for segment in TEST_PATH_SEGMENTS):
			return True
		if any(f"/{segment}" in path_text for segment in TEST_PATH_SEGMENTS):
			return True
	return False


#============================================


def is_trivial_symbol(name: str) -> bool:
	"""Return whether a symbol name carries no architectural meaning."""
	normalized = normalize_symbol_name(name).lower()
	is_trivial = normalized in TRIVIAL_SYMBOL_NAMES
	return is_trivial


#============================================


def connector_spread_ceiling(total_communities: int) -> int:
	"""Return the largest community spread a real cross-area connector may have."""
	scaled_ceiling = int(total_communities * MAX_CONNECTOR_SPREAD_RATIO)
	ceiling = max(MIN_CONNECTOR_SPREAD, scaled_ceiling)
	return ceiling


#============================================


def filter_bridges(
	bridges: list[tuple[str, tuple[str, ...]]],
	total_communities: int,
) -> list[tuple[str, tuple[str, ...]]]:
	"""Drop utility types and test scaffolding from Graphify's bridge evidence.

	Both the analysis sidecar and the report fallback route through this one
	helper so the two paths cannot drift apart.

	Args:
		bridges: Connector label paired with the communities it spans.
		total_communities: Count of communities known for this map.

	Returns:
		The surviving bridges in Graphify's original order.
	"""
	ceiling = connector_spread_ceiling(total_communities)
	kept_bridges = []
	for label, community_names in bridges:
		if len(community_names) > ceiling:
			continue
		if is_test_symbol(label) or is_trivial_symbol(label):
			continue
		kept_bridges.append((label, community_names))
	return kept_bridges


#============================================


def clean_graph_text(value: str) -> str:
	"""Return graph-derived text as one printable terminal line."""
	printable_characters = [character if character.isprintable() else " " for character in value]
	printable_text = "".join(printable_characters)
	cleaned_text = " ".join(printable_text.split())
	return cleaned_text


#============================================


def read_json_object(path: pathlib.Path) -> dict:
	"""Read one fixed Graphify sidecar and require a JSON object."""
	# ASVS 1.5.2 and 2.2.1: decode safe JSON primitives and validate the outer shape.
	data = json.loads(path.read_text(encoding="utf-8"))
	if not isinstance(data, dict):
		raise RuntimeError(f"Graphify data must be a JSON object: {path}")
	return data


#============================================


def load_graph_data(repo_root: pathlib.Path) -> dict:
	"""Load and validate the fixed Graphify node-link JSON artifact."""
	# ASVS 5.3.2: every input path is fixed beneath the active repository root.
	graph_path = repo_root / OUTPUT_DIR_NAME / GRAPH_FILE_NAME
	graph_data = read_json_object(graph_path)
	if "nodes" not in graph_data or not isinstance(graph_data["nodes"], list):
		raise RuntimeError(f"Graphify graph data has no nodes list: {graph_path}")
	if "links" not in graph_data or not isinstance(graph_data["links"], list):
		raise RuntimeError(f"Graphify graph data has no links list: {graph_path}")

	node_ids = set()
	for node in graph_data["nodes"]:
		if not isinstance(node, dict):
			raise RuntimeError(f"Graphify nodes must be JSON objects: {graph_path}")
		if not isinstance(node.get("id"), str) or not isinstance(node.get("label"), str):
			raise RuntimeError(f"Graphify nodes require string id and label values: {graph_path}")
		node_ids.add(node["id"])

	for link in graph_data["links"]:
		if not isinstance(link, dict):
			raise RuntimeError(f"Graphify links must be JSON objects: {graph_path}")
		if not isinstance(link.get("source"), str) or not isinstance(link.get("target"), str):
			raise RuntimeError(f"Graphify links require string endpoints: {graph_path}")
		if link["source"] not in node_ids or link["target"] not in node_ids:
			raise RuntimeError(f"Graphify links must reference known nodes: {graph_path}")

	return graph_data


#============================================


def load_analysis_data(repo_root: pathlib.Path) -> dict | None:
	"""Load Graphify's optional structured analysis sidecar."""
	analysis_path = repo_root / OUTPUT_DIR_NAME / ANALYSIS_FILE_NAME
	if not analysis_path.is_file():
		return None
	analysis_data = read_json_object(analysis_path)
	communities = analysis_data.get("communities")
	if not isinstance(communities, dict):
		raise RuntimeError(f"Graphify analysis has no communities object: {analysis_path}")
	for community_id, node_ids in communities.items():
		if not isinstance(community_id, str) or not isinstance(node_ids, list):
			raise RuntimeError(f"Graphify analysis communities are invalid: {analysis_path}")
		if not all(isinstance(node_id, str) for node_id in node_ids):
			raise RuntimeError(f"Graphify analysis node ids must be text: {analysis_path}")
	for field_name in ("questions", "surprises", "gods"):
		field_value = analysis_data.get(field_name, [])
		if not isinstance(field_value, list):
			raise RuntimeError(f"Graphify analysis {field_name} must be a list: {analysis_path}")
		if not all(isinstance(item, dict) for item in field_value):
			raise RuntimeError(f"Graphify analysis {field_name} entries are invalid: {analysis_path}")
	return analysis_data


#============================================


def load_labels_data(repo_root: pathlib.Path) -> dict | None:
	"""Load Graphify's optional stable community-label sidecar."""
	labels_path = repo_root / OUTPUT_DIR_NAME / LABELS_FILE_NAME
	if not labels_path.is_file():
		return None
	labels_data = read_json_object(labels_path)
	if not all(isinstance(key, str) and isinstance(value, str)
			for key, value in labels_data.items()):
		raise RuntimeError(f"Graphify labels must map text ids to names: {labels_path}")
	return labels_data


#============================================


def graph_community_name(node: dict, labels_data: dict | None) -> str | None:
	"""Return one node's stable community name when available."""
	community_name = node.get("community_name")
	if isinstance(community_name, str) and community_name.strip():
		return clean_graph_text(community_name)
	community_id = node.get("community")
	if isinstance(community_id, (str, int)):
		community_key = str(community_id)
		if labels_data is not None and community_key in labels_data:
			return clean_graph_text(labels_data[community_key])
		return f"Community {community_key}"
	return None


#============================================


def analysis_bridge_questions(analysis_data: dict | None) -> list[tuple[str, tuple[str, ...]]]:
	"""Return structured bridge-node evidence in Graphify's deterministic order."""
	if analysis_data is None:
		return []
	bridges = []
	for item in analysis_data.get("questions", []):
		if item.get("type") != "bridge_node":
			continue
		question = item.get("question")
		if not isinstance(question, str):
			continue
		quoted_values = [clean_graph_text(value) for value in re.findall(r"`([^`]+)`", question)]
		if len(quoted_values) < 3:
			continue
		bridges.append((quoted_values[0], tuple(sorted(set(quoted_values[1:])))))
	return bridges


#============================================


def report_fallback_data(repo_root: pathlib.Path) -> dict | None:
	"""Extract bounded structural facts from the report when sidecars are unavailable."""
	report_path = repo_root / OUTPUT_DIR_NAME / REPORT_FILE_NAME
	if not report_path.is_file():
		return None
	lines = report_path.read_text(encoding="utf-8").splitlines()
	community_hubs = []
	community_headings = []
	bridges = []
	relationships = []
	in_hubs = False
	for line in lines:
		if line == "## Community Hubs (Navigation)":
			in_hubs = True
			continue
		if in_hubs and line.startswith("## "):
			in_hubs = False
		if in_hubs and line.startswith("- "):
			community_hubs.append(clean_graph_text(line[2:]))
		community_match = re.match(r'^### Community \S+ - "(.+)"$', line)
		if community_match is not None:
			community_headings.append(clean_graph_text(community_match.group(1)))
		if line.startswith("- **Why does ") and " connect " in line:
			quoted_values = [
				clean_graph_text(value) for value in re.findall(r"`([^`]+)`", line)
			]
			if len(quoted_values) >= 3:
				bridges.append((quoted_values[0], tuple(sorted(set(quoted_values[1:])))))
		relationship_match = re.match(
			r"^- `([^`]+)` --([a-zA-Z_]+)--> `([^`]+)`", line
		)
		if relationship_match is not None:
			source, relation, target = relationship_match.groups()
			relationships.append(
				f"{clean_graph_text(source)} {clean_graph_text(relation)} "
				f"{clean_graph_text(target)}."
			)
	communities = community_hubs if community_hubs else community_headings
	communities = list(dict.fromkeys(communities))
	if not communities and not bridges and not relationships:
		return None
	return {
		"communities": communities,
		"bridges": bridges,
		"relationships": relationships,
	}


#============================================


def human_join(values: tuple[str, ...]) -> str:
	"""Join a short tuple of names for one factual manager-context line."""
	if len(values) == 2:
		return f"{values[0]} and {values[1]}"
	return f"{', '.join(values[:-1])}, and {values[-1]}"


#============================================


def format_connector_communities(community_names: tuple[str, ...]) -> str:
	"""Bound one connector's community list while preserving Graphify's order."""
	visible_names = community_names[:MAX_CONNECTOR_COMMUNITIES]
	omitted_count = len(community_names) - len(visible_names)
	if omitted_count == 0:
		return human_join(visible_names)
	return f"{', '.join(visible_names)}, and {omitted_count} more"


#============================================


def analysis_community_names(
	analysis_data: dict,
	labels_data: dict | None,
	graph_data: dict | None,
	report_data: dict | None,
) -> list[str]:
	"""Extract Graphify's community order and resolve its generated labels."""
	graph_nodes = {} if graph_data is None else {
		node["id"]: node for node in graph_data["nodes"]
	}
	report_names = [] if report_data is None else report_data["communities"]
	community_names = []
	for index, (community_id, node_ids) in enumerate(analysis_data["communities"].items()):
		community_name = None
		if labels_data is not None and community_id in labels_data:
			community_name = clean_graph_text(labels_data[community_id])
		if community_name is None:
			for node_id in node_ids:
				if node_id in graph_nodes:
					community_name = graph_community_name(graph_nodes[node_id], labels_data)
					if community_name is not None:
						break
		if community_name is None and index < len(report_names):
			community_name = report_names[index]
		if community_name is None:
			community_name = f"Community {clean_graph_text(community_id)}"
		if community_name not in community_names:
			community_names.append(community_name)
	return community_names[:MAX_COMMUNITIES]


#============================================


def graph_community_names(
	graph_data: dict | None,
	labels_data: dict | None,
) -> list[str]:
	"""Extract unique community names in Graphify's graph order as a minimal fallback."""
	if graph_data is None:
		return []
	community_names = []
	for node in graph_data["nodes"]:
		community_name = graph_community_name(node, labels_data)
		if community_name is not None and community_name not in community_names:
			community_names.append(community_name)
	return community_names[:MAX_COMMUNITIES]


#============================================


def surprise_source_files(surprise: dict) -> tuple[str, ...]:
	"""Return the recorded endpoint source paths for one surprise record."""
	source_files = surprise.get("source_files", [])
	if not isinstance(source_files, list):
		return ()
	return tuple(value for value in source_files if isinstance(value, str))


#============================================


def analysis_relationships(analysis_data: dict | None) -> list[str]:
	"""Format Graphify's own surprising-connection records without rescoring them.

	Graphify's ordering is preserved. Test scaffolding and uninformative call
	targets are dropped first, so the section reports architecture rather than
	the test suite. The whole sidecar list is scanned before truncating, because
	filtering otherwise empties the section on a test-heavy repository.
	"""
	if analysis_data is None:
		return []
	relationships = []
	for surprise in analysis_data.get("surprises", []):
		source = surprise.get("source")
		target = surprise.get("target")
		relation = surprise.get("relation")
		if not all(isinstance(value, str) for value in (source, target, relation)):
			continue
		source_files = surprise_source_files(surprise)
		if is_test_symbol(source, source_files) or is_test_symbol(target, source_files):
			continue
		if is_trivial_symbol(target):
			continue
		relationships.append(
			f"{clean_graph_text(source)} {clean_graph_text(relation)} "
			f"{clean_graph_text(target)}."
		)
		if len(relationships) == MAX_RELATIONSHIPS:
			break
	return relationships


#============================================


def analysis_god_nodes(
	analysis_data: dict | None,
	graph_data: dict | None,
) -> list[str]:
	"""Name Graphify's most-connected symbols and their source paths.

	Graphify already excludes file and concept nodes when it computes these, so
	its order is kept as-is. Each hub's source file is resolved through the graph
	so test scaffolding can be recognized and managers get a concrete starting
	point in the current source.
	"""
	if analysis_data is None:
		return []
	node_sources = {}
	if graph_data is not None:
		for node in graph_data["nodes"]:
			source_file = node.get("source_file", "")
			if isinstance(source_file, str):
				node_sources[node["id"]] = source_file
	hub_names = []
	for god in analysis_data.get("gods", []):
		label = god.get("label")
		if not isinstance(label, str):
			continue
		node_id = god.get("id")
		source_files = ()
		if isinstance(node_id, str) and node_id in node_sources:
			source_files = (node_sources[node_id],)
		if is_test_symbol(label, source_files) or is_trivial_symbol(label):
			continue
		hub_name = clean_graph_text(label)
		if source_files:
			hub_name = f"{hub_name} ({source_files[0]})"
		if hub_name not in hub_names:
			hub_names.append(hub_name)
		if len(hub_names) == MAX_GOD_NODES:
			break
	return hub_names


#============================================


def format_graph_scale(graph_data: dict | None) -> str | None:
	"""Return one line stating how large the map is, or None without a graph."""
	if graph_data is None:
		return None
	node_count = len(graph_data["nodes"])
	link_count = len(graph_data["links"])
	scale_text = f"Map size: {node_count} nodes, {link_count} edges"
	return scale_text


#============================================


def graph_mapped_at(repo_root: pathlib.Path) -> datetime.datetime | None:
	"""Return the local modification time of the primary usable graph artifact."""
	# ASVS 5.3.2: inspect only fixed Graphify artifact paths beneath the repo root.
	artifact_names = (GRAPH_FILE_NAME, ANALYSIS_FILE_NAME, REPORT_FILE_NAME)
	for artifact_name in artifact_names:
		artifact_path = repo_root / OUTPUT_DIR_NAME / artifact_name
		if artifact_path.is_file():
			mapped_at = datetime.datetime.fromtimestamp(
				artifact_path.stat().st_mtime
			).astimezone()
			return mapped_at
	return None


#============================================


def format_mapped_at(mapped_at: datetime.datetime) -> str:
	"""Format one timezone-aware map time for concise manager context."""
	if mapped_at.tzinfo is None or mapped_at.utcoffset() is None:
		raise ValueError("Graphify mapping time must include a timezone")
	timezone_name = mapped_at.tzname()
	if timezone_name is None:
		raise ValueError("Graphify mapping time must name its timezone")
	hour = mapped_at.strftime("%I").lstrip("0")
	mapped_text = (
		f"{hour}:{mapped_at:%M %p} {timezone_name} "
		f"{mapped_at:%b} {mapped_at.day} {mapped_at:%Y}"
	)
	return mapped_text


#============================================


def format_orientation(
	mapped_at: datetime.datetime,
	graph_data: dict | None,
	analysis_data: dict | None = None,
	labels_data: dict | None = None,
	report_data: dict | None = None,
	lessons_relative_path: str | None = None,
) -> str:
	"""Return concise repository-specific Graphify context for agent managers."""
	if analysis_data is not None:
		major_areas = analysis_community_names(
			analysis_data, labels_data, graph_data, report_data
		)
		total_communities = len(analysis_data["communities"])
		bridges = filter_bridges(
			analysis_bridge_questions(analysis_data), total_communities
		)[:MAX_BRIDGE_SYMBOLS]
		relationships = analysis_relationships(analysis_data)
	elif report_data is not None:
		major_areas = report_data["communities"][:MAX_COMMUNITIES]
		total_communities = len(report_data["communities"])
		bridges = filter_bridges(
			report_data["bridges"], total_communities
		)[:MAX_BRIDGE_SYMBOLS]
		relationships = report_data["relationships"][:MAX_RELATIONSHIPS]
	else:
		major_areas = graph_community_names(graph_data, labels_data)
		bridges = []
		relationships = []
	if not major_areas:
		major_areas = graph_community_names(graph_data, labels_data)
	architectural_hubs = analysis_god_nodes(analysis_data, graph_data)
	scale_text = format_graph_scale(graph_data)

	lines = ["GRAPHIFY CONTEXT", f"Graph mapped at {format_mapped_at(mapped_at)}"]
	if scale_text is not None:
		lines.append(scale_text)
	if major_areas:
		lines.append("Major repository areas:")
		lines.extend(f"- {community_name}" for community_name in major_areas)
	if architectural_hubs:
		lines.append("Architectural hubs:")
		lines.extend(f"- {hub_name}" for hub_name in architectural_hubs)
	if bridges:
		lines.append("Cross-area connectors:")
		for label, community_names in bridges:
			community_text = format_connector_communities(community_names)
			lines.append(f"- {label} - connects {community_text}")
	if relationships:
		lines.append("Notable relationships:")
		lines.extend(f"- {relationship}" for relationship in relationships)
	lines.extend(
		[
			"For task-specific investigation:",
			'  graphify query "<question>" --budget 1500',
			'  graphify explain "<symbol_or_path>"',
			'  graphify affected "<symbol_or_path>" --depth 2',
			'  graphify path "<A>" "<B>"',
			"Use Graphify before broad repository exploration. "
			"Verify conclusions in current source and tests.",
		]
	)
	if lessons_relative_path is not None:
		lines.append(f"Prior query outcomes: {lessons_relative_path}")
	return "\n".join(lines)


#============================================


def load_orientation_data(
	repo_root: pathlib.Path,
) -> tuple[dict | None, dict | None, dict | None, dict | None]:
	"""Load preferred structured inputs and the last-resort report fallback."""
	output_dir = repo_root / OUTPUT_DIR_NAME
	analysis_data = load_analysis_data(repo_root)
	labels_data = load_labels_data(repo_root)
	graph_data = None
	if (output_dir / GRAPH_FILE_NAME).is_file():
		graph_data = load_graph_data(repo_root)
	report_data = None
	if analysis_data is None or labels_data is None:
		report_data = report_fallback_data(repo_root)
	return graph_data, analysis_data, labels_data, report_data


#============================================


def manager_context(repo_root: pathlib.Path) -> str | None:
	"""Return existing manager context, or None when no usable map exists."""
	graph_data, analysis_data, labels_data, report_data = load_orientation_data(repo_root)
	if graph_data is None and analysis_data is None and report_data is None:
		return None
	mapped_at = graph_mapped_at(repo_root)
	if mapped_at is None:
		raise RuntimeError("Graphify context has data but no timestamped source artifact")
	found_lessons_path = lessons_path(repo_root)
	lessons_relative_path = None
	if found_lessons_path is not None:
		lessons_relative_path = str(found_lessons_path.relative_to(repo_root))
	context = format_orientation(
		mapped_at,
		graph_data,
		analysis_data=analysis_data,
		labels_data=labels_data,
		report_data=report_data,
		lessons_relative_path=lessons_relative_path,
	)
	return context


#============================================


def graph_needs_update(repo_root: pathlib.Path) -> bool:
	"""Return whether Graphify flagged pending non-code changes for this map.

	Graphify's own `check-update` subcommand only tests for this flag file and
	always exits zero, so the flag is read directly. That keeps --context true to
	its documented promise of printing orientation without running Graphify.
	"""
	# ASVS 5.3.2: inspect one fixed artifact path beneath the repository root.
	flag_path = repo_root / OUTPUT_DIR_NAME / NEEDS_UPDATE_FILE_NAME
	needs_update = flag_path.is_file()
	return needs_update


#============================================


def lessons_path(repo_root: pathlib.Path) -> pathlib.Path | None:
	"""Return the aggregated Graphify lessons file when one has been produced."""
	# ASVS 5.3.2: the reflections path is fixed beneath the generated output dir.
	candidate_path = repo_root / OUTPUT_DIR_NAME / LESSONS_FILE_PATH
	if not candidate_path.is_file():
		return None
	return candidate_path


#============================================


def write_manager_context(repo_root: pathlib.Path, context: str) -> pathlib.Path:
	"""Write the deterministic manager summary beside Graphify's own artifacts."""
	# ASVS 5.3.2: write only to the fixed generated-output path for this checkout.
	context_path = repo_root / OUTPUT_DIR_NAME / MANAGER_CONTEXT_FILE_NAME
	context_path.write_text(f"{context}\n", encoding="utf-8")
	return context_path
