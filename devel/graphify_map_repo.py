#!/usr/bin/env python3
"""Build or update a Graphify repository map and print concise agent guidance.

Orientation loading and formatting live in devel/graphify_context_lib.py; this
script owns the command line, the Graphify subprocess lifecycle, and main().
"""

# Standard Library
import sys
import json
import shutil
import pathlib
import argparse
import subprocess

# local repo modules
import graphify_docs_lib
import graphify_context_lib
import graphify_prune_tests


CLAUDE_LABEL_MODEL = "sonnet"
OLLAMA_MODEL = "qwen2.5-coder:7b-instruct"
GRAPHIFY_PACKAGE = "graphifyy[ollama,sql,terraform]"
LABEL_BACKEND = "claude-cli"
OLLAMA_BACKEND = "ollama"
MODE_AUTO = "auto"
MODE_FRESH = "fresh"
MODE_UPDATE = "update"
MODE_CONTEXT = "context"
COLLAPSED_EDGE_FIELD = "directed_same_endpoint_collapsed_edges"


#============================================


def build_parser() -> argparse.ArgumentParser:
	"""Build the documented Graphify command-line parser."""
	help_epilog = (
		"With no flag, update the existing code map or build it when absent. "
		"Fresh builds relabel communities and benchmark; add --ollama when the Claude "
		"allowance is exhausted. Add --svg to fresh or update to publish documentation in "
		"the same run, or use --svg alone to publish the existing map."
	)
	# ASVS 2.1.1 and 2.2.1: expose and document only the fixed action allowlist.
	parser = argparse.ArgumentParser(
		description=(
			"Update a Graphify map, rebuild it, inspect context, or publish its docs."
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
		help="rebuild the code map, relabel communities, and benchmark",
	)
	mode_group.add_argument(
		"-U", "--update",
		dest="mode",
		action="store_const",
		const=MODE_UPDATE,
		help="update the code map, or build fresh when no map exists",
	)
	mode_group.add_argument(
		"-C", "--context",
		dest="mode",
		action="store_const",
		const=MODE_CONTEXT,
		help="print existing-map orientation without rebuilding",
	)
	parser.add_argument(
		"-S", "--svg",
		dest="write_svg",
		action="store_true",
		help="publish docs/GRAPHIFY.md and its compact community SVG",
	)
	parser.add_argument(
		"-O", "--ollama",
		dest="label_backend",
		action="store_const",
		const=OLLAMA_BACKEND,
		help=f"with --fresh, label locally with {OLLAMA_MODEL}",
	)
	parser.set_defaults(mode=MODE_AUTO, label_backend=LABEL_BACKEND, write_svg=False)
	return parser


#============================================


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
	"""Parse automatic or explicitly selected Graphify lifecycle modes."""
	parser = build_parser()
	args = parser.parse_args(argv)
	# ASVS 2.2.1: Ollama has a defined fresh-build purpose, not an implicit fallback.
	if args.label_backend == OLLAMA_BACKEND and args.mode != MODE_FRESH:
		parser.error("--ollama requires --fresh")
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
	"""Require the fresh-build label backend and prepare Ollama when selected."""
	# ASVS 2.2.1: choose only the two documented fresh-build label backends.
	if label_backend not in (LABEL_BACKEND, OLLAMA_BACKEND):
		raise ValueError(f"Unsupported Graphify label backend: {label_backend}")
	backend_executable = require_command(
		"ollama" if label_backend == OLLAMA_BACKEND else "claude"
	)
	if label_backend == OLLAMA_BACKEND:
		print_step(f"PULLING OLLAMA MODEL: {OLLAMA_MODEL}")
		run_command([backend_executable, "pull", OLLAMA_MODEL], repo_root)


#============================================


def repo_has_cargo(repo_root: pathlib.Path) -> bool:
	"""Return whether this repository is a Cargo workspace."""
	# ASVS 5.3.2: one fixed marker path beneath the repository root.
	has_cargo = (repo_root / "Cargo.toml").is_file()
	return has_cargo


#============================================


def prunes_rust_tests(repo_root: pathlib.Path, is_fresh: bool) -> bool:
	"""Return whether this build prunes Rust test symbols before clustering.

	Gated on the same repository evidence that already selects --cargo, so a
	repository with no Rust keeps the original pipeline exactly. Limited to
	fresh builds: re-clustering renumbers communities, and a fresh build is the
	one path that always relabels afterward, so stored labels cannot go stale.
	"""
	prunes = is_fresh and repo_has_cargo(repo_root)
	return prunes


#============================================


def graph_build_is_fresh(repo_root: pathlib.Path, mode: str) -> bool:
	"""Return whether one automatic, fresh, or update build extracts a fresh graph."""
	if mode not in (MODE_AUTO, MODE_FRESH, MODE_UPDATE):
		raise ValueError(f"Unsupported Graphify mode: {mode}")
	graph_path = (
		repo_root
		/ graphify_context_lib.OUTPUT_DIR_NAME
		/ graphify_context_lib.GRAPH_FILE_NAME
	)
	graph_exists = graph_path.is_file()
	is_fresh = mode == MODE_FRESH or not graph_exists
	return is_fresh


#============================================


def graph_build_command(
	graphify_executable: str,
	repo_root: pathlib.Path,
	mode: str,
) -> tuple[str, list[str], bool]:
	"""Return the graph operation and whether it performs a fresh extraction."""
	is_fresh = graph_build_is_fresh(repo_root, mode)
	if is_fresh:
		if is_fresh and mode == MODE_UPDATE:
			operation = "NO EXISTING GRAPH; EXTRACTING FRESH GRAPHIFY CODE MAP"
		else:
			operation = "EXTRACTING GRAPHIFY CODE MAP"
		command = [graphify_executable, "extract", ".", "--code-only"]
		if repo_has_cargo(repo_root):
			command.append("--cargo")
		# Clustering is deferred so it never sees the Rust test symbols that
		# the prune step is about to remove.
		if prunes_rust_tests(repo_root, is_fresh):
			command.append("--no-cluster")
	else:
		operation = "UPDATING GRAPHIFY CODE MAP"
		command = [graphify_executable, "update", "."]
	return operation, command, is_fresh


#============================================


def label_graph(
	graphify_executable: str,
	repo_root: pathlib.Path,
	label_backend: str,
) -> None:
	"""Label a fresh Graphify map with the selected, validated backend."""
	if label_backend not in (LABEL_BACKEND, OLLAMA_BACKEND):
		raise ValueError(f"Unsupported Graphify label backend: {label_backend}")
	label_model = OLLAMA_MODEL if label_backend == OLLAMA_BACKEND else CLAUDE_LABEL_MODEL
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


def prune_rust_tests_then_cluster(
	graphify_executable: str,
	repo_root: pathlib.Path,
) -> None:
	"""Remove Rust test symbols from the graph, then cluster what remains.

	Extraction ran with --no-cluster, so this is the only clustering pass and it
	never sees the test symbols. Labeling stays with the caller's configured
	backend, so cluster-only is told not to name communities itself.
	"""
	print_step("PRUNING RUST TEST SYMBOLS")
	graph_path = (
		repo_root
		/ graphify_context_lib.OUTPUT_DIR_NAME
		/ graphify_context_lib.GRAPH_FILE_NAME
	)
	summary = graphify_prune_tests.prune_graph_file(graph_path, repo_root)
	# Never silent: a build that changes the graph reports what it removed.
	print(
		f"Removed {summary['removed_nodes']} test nodes "
		f"and {summary['removed_links']} links."
	)
	print_step("CLUSTERING PRUNED GRAPHIFY CODE MAP")
	run_command([graphify_executable, "cluster-only", ".", "--no-label"], repo_root)


#============================================


def report_graph_diagnostics(
	graphify_executable: str,
	repo_root: pathlib.Path,
) -> None:
	"""Report same-endpoint edge collapse without failing the build.

	Graphify documents no reliable threshold for this measure, and repeated
	endpoint pairs are legitimate in some codebases, so this stays advisory. A
	diagnostic that could abort the run would make the tool unusable on exactly
	the unusual repositories it is meant to describe.
	"""
	# ASVS 1.2.5: fixed argv, no shell, and failures are reported rather than raised.
	result = subprocess.run(
		[graphify_executable, "diagnose", "multigraph", "--json"],
		cwd=repo_root,
		capture_output=True,
		text=True,
		check=False,
	)
	if result.returncode != 0:
		print("Graph diagnostics unavailable; skipping edge-collapse report.")
		return
	summary = json.loads(result.stdout)
	collapsed_edges = summary.get(COLLAPSED_EDGE_FIELD, 0)
	if not isinstance(collapsed_edges, int) or collapsed_edges <= 0:
		print("No same-endpoint edge collapse detected.")
		return
	print(f"Same-endpoint edge collapse: {collapsed_edges} edges merged.")
	print("Distinct relationships between the same two symbols share one edge.")


def validate_core_artifacts(repo_root: pathlib.Path) -> None:
	"""Require the graph needed for targeted Graphify traversal."""
	graph_path = (
		repo_root
		/ graphify_context_lib.OUTPUT_DIR_NAME
		/ graphify_context_lib.GRAPH_FILE_NAME
	)
	if not graph_path.is_file():
		raise RuntimeError(f"Required Graphify artifact is missing: {graph_path}")


#============================================


def print_context(repo_root: pathlib.Path) -> None:
	"""Print existing-map orientation or CLI help before the first build."""
	context = graphify_context_lib.manager_context(repo_root)
	if context is None:
		print(f"No Graphify map exists in {graphify_context_lib.OUTPUT_DIR_NAME}/ yet.")
		print("Run without a mode, with --fresh, or with --update to build the first map.")
		print()
		build_parser().print_help()
		return
	print(context)
	# Advisory only: orientation is the point of this mode, so a stale map still
	# prints in full and the warning is appended to it.
	if graphify_context_lib.graph_needs_update(repo_root):
		print("Map is stale: non-code changes are pending.")
		print("Refresh it with --update.")


#============================================


def write_graphify_docs(repo_root: pathlib.Path) -> None:
	"""Write the Graphify page and compact SVG from an existing graph."""
	if graphify_context_lib.manager_context(repo_root) is None:
		print(f"No Graphify map exists in {graphify_context_lib.OUTPUT_DIR_NAME}/ yet.")
		print("Run without a mode, with --fresh, or with --update to build the first map.")
		return
	print_step("PUBLISHING GRAPHIFY DOCUMENTATION")
	# ASVS 5.3.2: the writer owns two fixed paths beneath repository docs/.
	page_path, figure_path = graphify_docs_lib.write_docs(repo_root)
	print(f"Graphify page written to {page_path.relative_to(repo_root)}")
	print(f"Compact SVG written to {figure_path.relative_to(repo_root)}")


#============================================


def main() -> None:
	"""Run the selected Graphify lifecycle or print artifact-driven orientation."""
	args = parse_args()
	repo_root = get_repo_root()
	require_repo_root(repo_root)
	if args.mode == MODE_CONTEXT:
		print_context(repo_root)
		if args.write_svg:
			write_graphify_docs(repo_root)
		return
	# Bare --svg publishes the existing graph without implicitly updating it.
	if args.mode == MODE_AUTO and args.write_svg:
		write_graphify_docs(repo_root)
		return

	is_fresh = graph_build_is_fresh(repo_root, args.mode)
	if is_fresh:
		upgrade_graphify(repo_root)
		prepare_label_backend(repo_root, args.label_backend)
	graphify_executable = require_command("graphify")
	operation, build_command, is_fresh = graph_build_command(
		graphify_executable,
		repo_root,
		args.mode,
	)
	print_step(operation)
	run_command(build_command, repo_root)
	if prunes_rust_tests(repo_root, is_fresh):
		prune_rust_tests_then_cluster(graphify_executable, repo_root)
	if is_fresh:
		print_step("LABELING GRAPHIFY COMMUNITIES")
		label_graph(graphify_executable, repo_root, args.label_backend)
	if is_fresh:
		print_step("BENCHMARKING GRAPHIFY CODE MAP")
		run_command([graphify_executable, "benchmark"], repo_root)
		print_step("CHECKING GRAPHIFY EDGE FIDELITY")
		report_graph_diagnostics(graphify_executable, repo_root)

	validate_core_artifacts(repo_root)
	context = graphify_context_lib.manager_context(repo_root)
	if context is None:
		raise RuntimeError("Graphify output did not contain usable manager context data")
	context_path = graphify_context_lib.write_manager_context(repo_root, context)

	print()
	print("======================================================================")
	print("GRAPHIFY READY")
	print("======================================================================")
	print()
	print(context)
	print()
	print(f"Manager context written to {context_path.relative_to(repo_root)}")
	if args.write_svg:
		write_graphify_docs(repo_root)


if __name__ == "__main__":
	main()
