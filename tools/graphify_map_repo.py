#!/usr/bin/env python3
"""Build or update a Graphify repository map and print concise agent guidance."""

# Standard Library
import os
import re
import sys
import json
import shutil
import pathlib
import argparse
import subprocess


CLAUDE_LABEL_MODEL = "sonnet"
OLLAMA_MODEL = "qwen2.5-coder:7b-instruct"
GRAPHIFY_PACKAGE = "graphifyy[ollama,sql,terraform]"
LABEL_BACKEND = "claude-cli"
OLLAMA_BACKEND = "ollama"
OUTPUT_DIR_NAME = "graphify-out"
ANALYSIS_FILE_NAME = ".graphify_analysis.json"
LABELS_FILE_NAME = ".graphify_labels.json"
GRAPH_FILE_NAME = "graph.json"
REPORT_FILE_NAME = "GRAPH_REPORT.md"
MANAGER_CONTEXT_FILE_NAME = "MANAGER_CONTEXT.md"
MODE_AUTO = "auto"
MODE_FRESH = "fresh"
MODE_UPDATE = "update"
MODE_CONTEXT = "context"
MAX_COMMUNITIES = 8
MAX_BRIDGE_SYMBOLS = 4
MAX_CONNECTOR_COMMUNITIES = 8
MAX_RELATIONSHIPS = 3


#============================================


def build_parser() -> argparse.ArgumentParser:
	"""Build the documented Graphify command-line parser."""
	help_epilog = (
		"How it works:\n"
		"  With no mode, update graphify-out/graph.json when it exists; otherwise extract a\n"
		"  fresh graph. Updates use Graphify's code-only fast path by default. Adding\n"
		"  --include-docs to --update incrementally extracts changed code and semantic inputs,\n"
		"  then refreshes community labels. Fresh builds upgrade Graphify, force extraction,\n"
		"  fully label, and benchmark. --include-docs includes nonignored document, paper, and\n"
		f"  image inputs. Claude CLI uses {CLAUDE_LABEL_MODEL}; --ollama selects the model for\n"
		"  extraction and labels. Context prints orientation without running\n"
		"  Graphify. Before the first map exists, context prints this help instead.\n"
		"\n"
		"Examples:\n"
		"  %(prog)s              # automatically choose fresh or update\n"
		"  %(prog)s --fresh      # upgrade, extract, fully label, and benchmark\n"
		"  %(prog)s --fresh --include-docs  # include nonignored semantic inputs\n"
		"  %(prog)s --update     # update, or run the fresh path when no graph exists\n"
		"  %(prog)s --update --include-docs  # incrementally refresh semantic inputs\n"
		"  %(prog)s --fresh --ollama  # use Ollama instead of Claude CLI\n"
		"  %(prog)s --context    # print orientation without rebuilding\n"
		"\n"
		f"Fresh-build setup: pip upgrades {GRAPHIFY_PACKAGE}.\n"
		f"Label backend: Claude CLI with {CLAUDE_LABEL_MODEL}; --ollama pulls {OLLAMA_MODEL}.\n"
		"Run graphify benchmark directly for measurements outside a fresh build.\n"
		f"Manager context: {OUTPUT_DIR_NAME}/{MANAGER_CONTEXT_FILE_NAME}"
	)
	# ASVS 2.1.1 and 2.2.1: document the accepted modes and validate against an allowlist.
	parser = argparse.ArgumentParser(
		description=(
			"Build or update a Graphify repository map, then print concise agent "
			"orientation."
		),
		epilog=help_epilog,
		formatter_class=argparse.RawDescriptionHelpFormatter,
	)
	mode_group = parser.add_mutually_exclusive_group()
	mode_group.add_argument(
		"-F", "--fresh",
		dest="mode",
		action="store_const",
		const=MODE_FRESH,
		help="force a fresh graphify extract, even when a graph already exists",
	)
	mode_group.add_argument(
		"-U", "--update",
		dest="mode",
		action="store_const",
		const=MODE_UPDATE,
		help="update an existing graph, or extract fresh when no graph exists",
	)
	mode_group.add_argument(
		"-C", "--context",
		dest="mode",
		action="store_const",
		const=MODE_CONTEXT,
		help="print existing-map orientation, or help when no map exists",
	)
	parser.add_argument(
		"-O", "--ollama",
		dest="label_backend",
		action="store_const",
		const=OLLAMA_BACKEND,
		help=f"use local Ollama model {OLLAMA_MODEL} for extraction and labels",
	)
	parser.add_argument(
		"-D", "--include-docs",
		dest="include_docs",
		action="store_true",
		help="include nonignored document, paper, and image inputs in fresh or update builds",
	)
	parser.set_defaults(
		mode=MODE_AUTO,
		label_backend=LABEL_BACKEND,
		include_docs=False,
	)
	return parser


#============================================


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
	"""Parse automatic or explicitly selected Graphify lifecycle modes."""
	parser = build_parser()
	args = parser.parse_args(argv)
	# ASVS 2.1.1 and 2.2.1: semantic extraction requires an explicit lifecycle mode.
	if args.include_docs and args.mode not in (MODE_FRESH, MODE_UPDATE):
		parser.error("--include-docs requires --fresh or --update")
	return args


#============================================


def get_repo_root() -> pathlib.Path:
	"""Return the Git repository root for the current working directory."""
	# ASVS 1.2.5: pass arguments directly without a shell interpreter.
	result = subprocess.run(
		["git", "rev-parse", "--show-toplevel"],
		check=True,
		capture_output=True,
		text=True,
	)
	repo_root = pathlib.Path(result.stdout.strip()).resolve()
	return repo_root


#============================================


def require_repo_root(repo_root: pathlib.Path) -> None:
	"""Require the tool to run from the active repository root."""
	current_dir = pathlib.Path.cwd().resolve()
	if current_dir != repo_root:
		raise RuntimeError(f"Run this tool from the repository root: {repo_root}")


#============================================


def require_command(command_name: str) -> str:
	"""Return the resolved executable path or raise a setup error."""
	executable = shutil.which(command_name)
	if executable is None:
		raise RuntimeError(
			f"Required command '{command_name}' is unavailable. "
			"Install the repository's declared development dependencies first."
		)
	return executable


#============================================


def print_step(label: str) -> None:
	"""Print one prominent runtime phase label."""
	print()
	print(f"============ {label} ============")


#============================================


def run_command(
	command: list[str],
	repo_root: pathlib.Path,
	environment: dict[str, str] | None = None,
) -> None:
	"""Run one trusted Graphify lifecycle command from the repository root."""
	# ASVS 1.2.5: subprocesses use an argv list and never invoke a shell.
	subprocess.run(command, cwd=repo_root, check=True, env=environment)


#============================================


def upgrade_graphify(repo_root: pathlib.Path) -> None:
	"""Upgrade the declared Graphify package for a fresh extraction."""
	print_step("UPDATING GRAPHIFY PYTHON PACKAGE")
	# ASVS 1.2.5: fixed package input is passed as argv to the active interpreter.
	run_command(
		[
			sys.executable,
			"-m",
			"pip",
			"install",
			"--upgrade",
			"--quiet",
			"--no-cache-dir",
			GRAPHIFY_PACKAGE,
		],
		repo_root,
	)


#============================================


def prepare_label_backend(repo_root: pathlib.Path, label_backend: str) -> None:
	"""Require the selected label backend and prepare its local model when needed."""
	# ASVS 2.2.1: select the required executable from the supported backend allowlist.
	if label_backend not in (LABEL_BACKEND, OLLAMA_BACKEND):
		raise ValueError(f"Unsupported Graphify label backend: {label_backend}")
	backend_executable = require_command(
		"ollama" if label_backend == OLLAMA_BACKEND else "claude"
	)
	if label_backend == OLLAMA_BACKEND:
		print_step(f"PULLING OLLAMA MODEL: {OLLAMA_MODEL}")
		run_command([backend_executable, "pull", OLLAMA_MODEL], repo_root)


#============================================


def graph_build_is_fresh(repo_root: pathlib.Path, mode: str) -> bool:
	"""Return whether one automatic, fresh, or update build extracts a fresh graph."""
	if mode not in (MODE_AUTO, MODE_FRESH, MODE_UPDATE):
		raise ValueError(f"Unsupported Graphify mode: {mode}")
	graph_path = repo_root / OUTPUT_DIR_NAME / GRAPH_FILE_NAME
	graph_exists = graph_path.is_file()
	is_fresh = mode == MODE_FRESH or not graph_exists
	return is_fresh


#============================================


def graph_build_command(
	graphify_executable: str,
	repo_root: pathlib.Path,
	mode: str,
	include_docs: bool,
	label_backend: str,
) -> tuple[str, list[str], bool]:
	"""Return the graph operation and whether it performs a fresh extraction."""
	# ASVS 2.2.1: accept only the two fixed Graphify semantic backends.
	if label_backend not in (LABEL_BACKEND, OLLAMA_BACKEND):
		raise ValueError(f"Unsupported Graphify label backend: {label_backend}")
	is_fresh = graph_build_is_fresh(repo_root, mode)
	if is_fresh or include_docs:
		map_scope = "CODE AND SEMANTIC MAP" if include_docs else "CODE MAP"
		if is_fresh and mode == MODE_UPDATE:
			operation = f"NO EXISTING GRAPH; EXTRACTING FRESH GRAPHIFY {map_scope}"
		elif is_fresh:
			operation = f"EXTRACTING GRAPHIFY {map_scope}"
		else:
			operation = f"UPDATING GRAPHIFY {map_scope}"
		command = [graphify_executable, "extract", "."]
		if include_docs:
			extraction_model = (
				OLLAMA_MODEL if label_backend == OLLAMA_BACKEND else CLAUDE_LABEL_MODEL
			)
			command.extend(
				[
					f"--backend={label_backend}",
					f"--model={extraction_model}",
				]
			)
			if is_fresh:
				command.append("--force")
		else:
			command.append("--code-only")
		if (repo_root / "Cargo.toml").is_file():
			command.append("--cargo")
	else:
		operation = "UPDATING GRAPHIFY CODE MAP"
		command = [graphify_executable, "update", "."]
	return operation, command, is_fresh


#============================================


def graph_build_environment(
	include_docs: bool,
	label_backend: str,
) -> dict[str, str] | None:
	"""Pin the Claude CLI extraction model while preserving the parent environment."""
	if not include_docs or label_backend != LABEL_BACKEND:
		return None
	# ASVS 1.2.5 and 2.2.1: the environment key and model value are fixed constants.
	environment = os.environ.copy()
	environment["GRAPHIFY_CLAUDE_CLI_MODEL"] = CLAUDE_LABEL_MODEL
	return environment


#============================================


def label_graph(
	graphify_executable: str,
	repo_root: pathlib.Path,
	label_backend: str,
) -> None:
	"""Fully refresh Graphify community labels with the selected backend."""
	# ASVS 2.2.1: accept only the two documented label backends.
	if label_backend not in (LABEL_BACKEND, OLLAMA_BACKEND):
		raise ValueError(f"Unsupported Graphify label backend: {label_backend}")
	label_model = (
		OLLAMA_MODEL if label_backend == OLLAMA_BACKEND else CLAUDE_LABEL_MODEL
	)
	# ASVS 1.2.5: fixed backend and model values remain isolated in the argv list.
	command = [
		graphify_executable,
		"label",
		".",
		f"--backend={label_backend}",
		f"--model={label_model}",
	]
	run_command(command, repo_root)


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

	built_at_commit = graph_data.get("built_at_commit")
	if built_at_commit is not None and not isinstance(built_at_commit, str):
		raise RuntimeError(f"Graphify built_at_commit must be text: {graph_path}")
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
	commit = None
	community_hubs = []
	community_headings = []
	bridges = []
	relationships = []
	in_hubs = False
	for line in lines:
		commit_match = re.match(r"^- Built from commit: `([^`]+)`$", line)
		if commit_match is not None:
			commit = clean_graph_text(commit_match.group(1))
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
	if commit is None and not communities and not bridges and not relationships:
		return None
	return {
		"commit": commit,
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


def analysis_relationships(analysis_data: dict | None) -> list[str]:
	"""Format Graphify's own surprising-connection records without rescoring them."""
	if analysis_data is None:
		return []
	relationships = []
	for surprise in analysis_data.get("surprises", []):
		source = surprise.get("source")
		target = surprise.get("target")
		relation = surprise.get("relation")
		if not all(isinstance(value, str) for value in (source, target, relation)):
			continue
		relationships.append(
			f"{clean_graph_text(source)} {clean_graph_text(relation)} "
			f"{clean_graph_text(target)}."
		)
		if len(relationships) == MAX_RELATIONSHIPS:
			break
	return relationships


#============================================


def format_orientation(
	repo_root: pathlib.Path,
	graph_data: dict | None,
	analysis_data: dict | None = None,
	labels_data: dict | None = None,
	report_data: dict | None = None,
) -> str:
	"""Return concise repository-specific Graphify context for agent managers."""
	if analysis_data is not None:
		major_areas = analysis_community_names(
			analysis_data, labels_data, graph_data, report_data
		)
		bridges = analysis_bridge_questions(analysis_data)[:MAX_BRIDGE_SYMBOLS]
		relationships = analysis_relationships(analysis_data)
	elif report_data is not None:
		major_areas = report_data["communities"][:MAX_COMMUNITIES]
		bridges = report_data["bridges"][:MAX_BRIDGE_SYMBOLS]
		relationships = report_data["relationships"][:MAX_RELATIONSHIPS]
	else:
		major_areas = graph_community_names(graph_data, labels_data)
		bridges = []
		relationships = []
	if not major_areas:
		major_areas = graph_community_names(graph_data, labels_data)
	commit = None
	if graph_data is not None:
		built_at_commit = graph_data.get("built_at_commit")
		if isinstance(built_at_commit, str) and built_at_commit:
			commit = clean_graph_text(built_at_commit)
	if commit is None and report_data is not None:
		commit = report_data["commit"]

	lines = ["GRAPHIFY CONTEXT"]
	if commit is not None:
		lines.append(f"Graph mapped at commit {commit[:12]}.")
	else:
		lines.append(f"Graph mapped for {clean_graph_text(repo_root.name)}.")
	if major_areas:
		lines.append("Major repository areas:")
		lines.extend(f"- {community_name}" for community_name in major_areas)
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
	return "\n".join(lines)


#============================================


def validate_core_artifacts(repo_root: pathlib.Path) -> None:
	"""Require the graph needed for targeted Graphify traversal."""
	graph_path = repo_root / OUTPUT_DIR_NAME / GRAPH_FILE_NAME
	if not graph_path.is_file():
		raise RuntimeError(f"Required Graphify artifact is missing: {graph_path}")


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
	context = format_orientation(
		repo_root,
		graph_data,
		analysis_data=analysis_data,
		labels_data=labels_data,
		report_data=report_data,
	)
	return context


#============================================


def write_manager_context(repo_root: pathlib.Path, context: str) -> pathlib.Path:
	"""Write the deterministic manager summary beside Graphify's own artifacts."""
	# ASVS 5.3.2: write only to the fixed generated-output path for this checkout.
	context_path = repo_root / OUTPUT_DIR_NAME / MANAGER_CONTEXT_FILE_NAME
	context_path.write_text(f"{context}\n", encoding="utf-8")
	return context_path


#============================================


def print_context(repo_root: pathlib.Path) -> None:
	"""Print existing-map orientation or CLI help before the first build."""
	context = manager_context(repo_root)
	if context is None:
		print(f"No Graphify map exists in {OUTPUT_DIR_NAME}/ yet.")
		print("Run without a mode, with --fresh, or with --update to build the first map.")
		print()
		build_parser().print_help()
		return
	print(context)


#============================================


def main() -> None:
	"""Run the selected Graphify lifecycle or print artifact-driven orientation."""
	args = parse_args()
	repo_root = get_repo_root()
	require_repo_root(repo_root)
	if args.mode == MODE_CONTEXT:
		print_context(repo_root)
		return

	is_fresh = graph_build_is_fresh(repo_root, args.mode)
	needs_labeling = is_fresh or args.include_docs
	if not needs_labeling and args.label_backend == OLLAMA_BACKEND:
		raise ValueError("--ollama applies only to fresh or --include-docs builds")
	if is_fresh:
		upgrade_graphify(repo_root)
	if needs_labeling:
		prepare_label_backend(repo_root, args.label_backend)
	graphify_executable = require_command("graphify")
	operation, build_command, is_fresh = graph_build_command(
		graphify_executable,
		repo_root,
		args.mode,
		args.include_docs,
		args.label_backend,
	)
	print_step(operation)
	build_environment = graph_build_environment(
		args.include_docs,
		args.label_backend,
	)
	run_command(build_command, repo_root, build_environment)
	if needs_labeling:
		print_step("LABELING GRAPHIFY COMMUNITIES")
		label_graph(graphify_executable, repo_root, args.label_backend)
	if is_fresh:
		map_scope = "CODE AND SEMANTIC MAP" if args.include_docs else "CODE MAP"
		print_step(f"BENCHMARKING GRAPHIFY {map_scope}")
		run_command([graphify_executable, "benchmark"], repo_root)

	validate_core_artifacts(repo_root)
	context = manager_context(repo_root)
	if context is None:
		raise RuntimeError("Graphify output did not contain usable manager context data")
	context_path = write_manager_context(repo_root, context)

	print()
	print("======================================================================")
	print("GRAPHIFY READY")
	print("======================================================================")
	print()
	print(context)
	print()
	print(f"Manager context written to {context_path.relative_to(repo_root)}")


if __name__ == "__main__":
	main()
