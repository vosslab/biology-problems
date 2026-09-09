"""Render compact Graphify documentation from repository graph data.

The generated SVG is intentionally a community-level illustration rather than
a second full graph export. Markdown owns the names and detail, while the SVG
shows the relative scale and coupling of the twelve largest communities.
"""

# Standard Library
import html
import math
import pathlib
import re

# local repo modules
import graphify_context_lib


PAGE_FILE_NAME = "GRAPHIFY.md"
FIGURE_FILE_NAME = "GRAPHIFY_map.svg"
MAX_MAJOR_COMMUNITIES = 12
SVG_WIDTH = 960
SVG_HEIGHT = 540
SVG_CENTER_X = SVG_WIDTH / 2
SVG_CENTER_Y = SVG_HEIGHT / 2
SVG_PALETTE = (
	"#2563EB", "#7C3AED", "#DB2777", "#DC2626",
	"#EA580C", "#CA8A04", "#16A34A", "#059669",
	"#0891B2", "#4F46E5", "#9333EA", "#475569",
)

HTML_TAG_PATTERN = re.compile(r"<[^>]*>")
UNSAFE_LABEL_PATTERN = re.compile(r"[^A-Za-z0-9 _.,'()/+:=\-]")
UNSAFE_PATH_PATTERN = re.compile(r"[^A-Za-z0-9_./\-]")
WHITESPACE_PATTERN = re.compile(r"\s+")


#============================================


def ascii_only(value: str) -> str:
	"""Return text safe for this repository's ASCII-only documentation rule."""
	cleaned = graphify_context_lib.clean_graph_text(value)
	ascii_text = cleaned.encode("ascii", "ignore").decode("ascii")
	return ascii_text


#============================================


def safe_community_name(value: str) -> str:
	"""Return an ASCII display name safe in Markdown prose and tables."""
	decoded_text = html.unescape(ascii_only(value))
	plain_text = HTML_TAG_PATTERN.sub(" ", decoded_text)
	plain_text = plain_text.replace("&", " and ")
	safe_text = UNSAFE_LABEL_PATTERN.sub(" ", plain_text)
	safe_name = WHITESPACE_PATTERN.sub(" ", safe_text).strip()
	return safe_name


#============================================


def safe_path(value: str) -> str:
	"""Return a source path that cannot break a Markdown code span or table."""
	ascii_text = ascii_only(value)
	safe_text = UNSAFE_PATH_PATTERN.sub("_", ascii_text)
	return safe_text


#============================================


def community_key(node: dict) -> str | None:
	"""Return one node's community identifier as text, when it has one."""
	community_id = node.get("community")
	if isinstance(community_id, (str, int)):
		return str(community_id)
	return None


#============================================


def community_names(graph_data: dict, labels_data: dict | None) -> dict[str, str]:
	"""Map each community identifier to its display name."""
	names = {}
	for node in graph_data["nodes"]:
		key = community_key(node)
		if key is None or key in names:
			continue
		name = graphify_context_lib.graph_community_name(node, labels_data)
		if name is None:
			continue
		safe_name = safe_community_name(name)
		if safe_name:
			names[key] = safe_name
	return names


#============================================


def community_node_counts(graph_data: dict) -> dict[str, int]:
	"""Count how many symbols each community holds."""
	counts: dict[str, int] = {}
	for node in graph_data["nodes"]:
		key = community_key(node)
		if key is None:
			continue
		counts[key] = counts.get(key, 0) + 1
	return counts


#============================================


def node_communities(graph_data: dict) -> dict[str, str]:
	"""Map each node id to its community identifier."""
	assignments = {}
	for node in graph_data["nodes"]:
		key = community_key(node)
		if key is not None:
			assignments[node["id"]] = key
	return assignments


#============================================


def community_edge_weights(graph_data: dict) -> dict[tuple[str, str], int]:
	"""Count relationships running between two different communities."""
	assignments = node_communities(graph_data)
	weights: dict[tuple[str, str], int] = {}
	for link in graph_data["links"]:
		source_key = assignments.get(link["source"])
		target_key = assignments.get(link["target"])
		if source_key is None or target_key is None or source_key == target_key:
			continue
		pair = tuple(sorted((source_key, target_key)))
		weights[pair] = weights.get(pair, 0) + 1
	return weights


#============================================


def node_degrees(graph_data: dict) -> dict[str, int]:
	"""Count how many relationships touch each node."""
	degrees: dict[str, int] = {}
	for link in graph_data["links"]:
		for endpoint in (link["source"], link["target"]):
			degrees[endpoint] = degrees.get(endpoint, 0) + 1
	return degrees


#============================================


def ranked_communities(
	graph_data: dict,
	labels_data: dict | None,
) -> list[tuple[str, str, int]]:
	"""Return communities as (key, name, size), largest first."""
	counts = community_node_counts(graph_data)
	names = community_names(graph_data, labels_data)
	ranked = []
	for key, size in counts.items():
		name = names.get(key, f"Community {key}")
		ranked.append((key, name, size))
	ranked.sort(key=lambda entry: (-entry[2], entry[0]))
	return ranked


#============================================


def source_group(source_file: str) -> str:
	"""Return the repository group containing a source file."""
	safe_source = safe_path(source_file)
	parts = pathlib.PurePosixPath(safe_source).parts
	if len(parts) < 2:
		return "Repository root"
	return parts[0]


#============================================


def repository_groups(graph_data: dict) -> list[tuple[str, int, int, int]]:
	"""Return repository groups as name, symbols, files, and communities."""
	groups: dict[str, dict[str, object]] = {}
	for node in graph_data["nodes"]:
		source_file = node.get("source_file")
		if not isinstance(source_file, str) or not source_file:
			continue
		group_name = source_group(source_file)
		if group_name not in groups:
			groups[group_name] = {"symbols": 0, "files": set(), "communities": set()}
		group = groups[group_name]
		group["symbols"] += 1
		group["files"].add(safe_path(source_file))
		key = community_key(node)
		if key is not None:
			group["communities"].add(key)

	rows = []
	for name, group in groups.items():
		rows.append((
			name,
			group["symbols"],
			len(group["files"]),
			len(group["communities"]),
		))
	rows.sort(key=lambda entry: (-entry[1], entry[0]))
	return rows


#============================================


def community_members(graph_data: dict, target_key: str) -> list[dict]:
	"""Return production-facing members assigned to one community."""
	members = []
	for node in graph_data["nodes"]:
		if community_key(node) != target_key:
			continue
		label = node.get("label")
		if not isinstance(label, str):
			continue
		source_file = node.get("source_file")
		source_files = (source_file,) if isinstance(source_file, str) else ()
		if graphify_context_lib.is_test_symbol(label, source_files):
			continue
		members.append(node)
	return members


#============================================


def representative_files(graph_data: dict, target_key: str) -> list[str]:
	"""Return up to two source files most represented in one community."""
	counts: dict[str, int] = {}
	for node in community_members(graph_data, target_key):
		source_file = node.get("source_file")
		if not isinstance(source_file, str) or not source_file:
			continue
		safe_source = safe_path(source_file)
		counts[safe_source] = counts.get(safe_source, 0) + 1
	ranked = sorted(counts.items(), key=lambda entry: (-entry[1], entry[0]))
	return [path for path, _count in ranked[:2]]


#============================================


def representative_symbols(
	graph_data: dict,
	target_key: str,
	degrees: dict[str, int],
) -> list[str]:
	"""Return up to three well-connected production symbols in one community."""
	members = []
	for node in community_members(graph_data, target_key):
		label = safe_community_name(node["label"])
		if label:
			members.append((degrees.get(node["id"], 0), label))
	members.sort(key=lambda entry: (-entry[0], entry[1]))
	return [label for _degree, label in members[:3]]


#============================================


def format_repository_groups(graph_data: dict) -> list[str]:
	"""Return a compact table describing the repository's source groups."""
	lines = [
		"| Group | Symbols | Files | Communities |",
		"| --- | ---: | ---: | ---: |",
	]
	for name, symbols, files, communities in repository_groups(graph_data):
		lines.append(f"| `{name}` | {symbols} | {files} | {communities} |")
	return lines


#============================================


def format_major_communities(graph_data: dict, labels_data: dict | None) -> list[str]:
	"""Return a table for the largest communities and representative members."""
	degrees = node_degrees(graph_data)
	lines = [
		"| Community | Symbols | Representative files | Connected symbols |",
		"| --- | ---: | --- | --- |",
	]
	for key, name, size in ranked_communities(
		graph_data, labels_data,
	)[:MAX_MAJOR_COMMUNITIES]:
		files = ", ".join(f"`{path}`" for path in representative_files(graph_data, key))
		symbols = ", ".join(
			f"`{symbol}`" for symbol in representative_symbols(graph_data, key, degrees)
		)
		lines.append(f"| {name} | {size} | {files} | {symbols} |")
	return lines


#============================================


def format_observations(graph_data: dict, labels_data: dict | None) -> list[str]:
	"""Return repository-derived observations about grouping and coupling."""
	lines = []
	ranked = ranked_communities(graph_data, labels_data)
	groups = repository_groups(graph_data)
	if groups:
		name, symbols, files, communities = groups[0]
		lines.append(
			f"- `{name}` is the largest source group: {symbols} symbols across "
			f"{files} files and {communities} communities."
		)
	if ranked:
		_key, name, size = ranked[0]
		share = 100 * size / len(graph_data["nodes"])
		lines.append(
			f"- {name} is the largest community with {size} symbols "
			f"({share:.1f}% of the map)."
		)
	weights = community_edge_weights(graph_data)
	if weights:
		names = community_names(graph_data, labels_data)
		pair, weight = min(weights.items(), key=lambda entry: (-entry[1], entry[0]))
		source_name = names.get(pair[0], f"Community {pair[0]}")
		target_name = names.get(pair[1], f"Community {pair[1]}")
		lines.append(
			f"- The strongest cross-community connection is {source_name} to "
			f"{target_name}, with {weight} relationships."
		)
		lines.append(
			f"- The graph contains {len(weights)} connected community pairs, "
			"showing where responsibilities meet across area boundaries."
		)
	return lines


#============================================


def community_positions(
	ranked: list[tuple[str, str, int]],
) -> dict[str, tuple[float, float]]:
	"""Place the largest community centrally and the remainder on an ellipse."""
	positions = {}
	if not ranked:
		return positions
	positions[ranked[0][0]] = (SVG_CENTER_X, SVG_CENTER_Y)
	outer_count = len(ranked) - 1
	for index, (key, _name, _size) in enumerate(ranked[1:]):
		angle = (-math.pi / 2) + (2 * math.pi * index / outer_count)
		x = SVG_CENTER_X + 350 * math.cos(angle)
		y = SVG_CENTER_Y + 205 * math.sin(angle)
		positions[key] = (x, y)
	return positions


#============================================


def community_radius(size: int, largest_size: int) -> float:
	"""Scale a community circle by the square root of its membership."""
	if largest_size <= 0:
		return 20.0
	radius = 20 + 42 * math.sqrt(size / largest_size)
	return radius


#============================================


def format_number(value: float) -> str:
	"""Return compact, deterministic SVG numeric text."""
	text = f"{value:.1f}".rstrip("0").rstrip(".")
	return text


#============================================


def format_community_svg(graph_data: dict, labels_data: dict | None) -> str:
	"""Return a self-contained, unlabeled community-level SVG illustration."""
	ranked = ranked_communities(graph_data, labels_data)[:MAX_MAJOR_COMMUNITIES]
	positions = community_positions(ranked)
	shown_keys = set(positions)
	weights = community_edge_weights(graph_data)
	shown_edges = [
		(pair, weight)
		for pair, weight in sorted(weights.items())
		if pair[0] in shown_keys and pair[1] in shown_keys
	]
	max_weight = max((weight for _pair, weight in shown_edges), default=1)

	lines = [
		f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" ',
		'role="img" aria-labelledby="title desc">',
		"<title id=\"title\">Repository community map</title>",
		"<desc id=\"desc\">The twelve largest code communities, sized by membership and ",
		"connected by weighted intercommunity relationships.</desc>",
		"<g fill=\"none\" stroke=\"#64748B\" stroke-linecap=\"round\">",
	]
	for pair, weight in shown_edges:
		x1, y1 = positions[pair[0]]
		x2, y2 = positions[pair[1]]
		stroke_width = 1 + 7 * weight / max_weight
		lines.append(
			f'<line x1="{format_number(x1)}" y1="{format_number(y1)}" '
			f'x2="{format_number(x2)}" y2="{format_number(y2)}" '
			f'stroke-width="{format_number(stroke_width)}" opacity="0.42"/>'
		)
	lines.append("</g>")
	largest_size = ranked[0][2] if ranked else 0
	for index, (key, _name, size) in enumerate(ranked):
		x, y = positions[key]
		radius = community_radius(size, largest_size)
		color = SVG_PALETTE[index]
		lines.append(
			f'<circle cx="{format_number(x)}" cy="{format_number(y)}" '
			f'r="{format_number(radius)}" fill="{color}" fill-opacity="0.88" '
			'stroke="#FFFFFF" stroke-width="4"/>'
		)
	lines.extend(["</svg>", ""])
	svg_text = "".join(lines)
	return svg_text


#============================================


def format_page(graph_data: dict, labels_data: dict | None) -> str:
	"""Assemble the complete repository-map page."""
	ranked = ranked_communities(graph_data, labels_data)
	lines = [
		"# Repository map",
		"",
		f"![Community-level repository graph]({FIGURE_FILE_NAME})",
		"",
		f"This Graphify snapshot maps {len(graph_data['nodes'])} symbols and "
		f"{len(graph_data['links'])} relationships into {len(ranked)} communities. "
		"The illustration keeps the largest 12 communities, scales each circle by "
		"membership, and weights each line by cross-community relationships.",
		"",
		"## Repository groups",
		"",
		"Source paths reveal the main implementation and support areas.",
		"",
	]
	lines.extend(format_repository_groups(graph_data))
	lines.extend([
		"",
		"## Major communities",
		"",
		"The largest communities show where related symbols concentrate. Representative files and",
		"well-connected symbols provide useful starting points for source inspection.",
		"",
	])
	lines.extend(format_major_communities(graph_data, labels_data))
	lines.extend(["", "## Graph observations", ""])
	lines.extend(format_observations(graph_data, labels_data))
	lines.extend([
		"",
		"## Reading the map",
		"",
		"The SVG is decorative and deliberately unlabeled. Community names and code-level detail live",
		"in the tables, where they remain readable, searchable, and accessible. Graphify is navigation",
		"evidence; confirm architectural conclusions in the current source and tests.",
		"",
		"Regenerate the page and figure with",
		"[devel/graphify_map_repo.py](../devel/graphify_map_repo.py) `--svg` after the map changes.",
	])
	page_text = "\n".join(lines)
	return page_text


#============================================


def write_docs(repo_root: pathlib.Path) -> tuple[pathlib.Path, pathlib.Path]:
	"""Write the fixed Graphify page and compact figure beneath repository docs."""
	graph_data = graphify_context_lib.load_graph_data(repo_root)
	labels_data = graphify_context_lib.load_labels_data(repo_root)
	figure_text = format_community_svg(graph_data, labels_data)
	page_text = format_page(graph_data, labels_data)
	# ASVS 5.3.2: both generated paths are fixed beneath the repository root.
	figure_path = repo_root / "docs" / FIGURE_FILE_NAME
	page_path = repo_root / "docs" / PAGE_FILE_NAME
	figure_path.write_text(figure_text, encoding="ascii")
	page_path.write_text(f"{page_text}\n", encoding="ascii")
	return page_path, figure_path
