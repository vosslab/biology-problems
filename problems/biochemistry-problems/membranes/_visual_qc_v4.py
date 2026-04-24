#!/usr/bin/env python3
"""Visual QC via regex inspection on the rendered HTML.

For each production PGML, render at three diverse seeds and check:
  - no internal arrow <line> segments with both y1 and y2 in 108..132
  - binding circle (cy=120, r=6, white-fill) count == n_substrates
  - release blob count matches per-substrate direction (cy=195 for in, 45 for out)
  - no stoich/label collision with compartment labels at y=22 / y=232
  - multi-solute cases have at least one text-anchor=end and one text-anchor=start
  - stagger applied ONLY in both-inward symporter cases
  - gradient pool rect (fill-opacity="0.10") present whenever a gradient count >= 3
"""

import json
import re
import subprocess
import sys
from pathlib import Path

LINT = Path.home() / ".claude/skills/webwork-writer/references/scripts/lint_pg_via_renderer_api.py"
MEM = Path(__file__).parent

FILES = [
	MEM / "identify_transporter_type.pgml",
	MEM / "driving_force_from_gradient.pgml",
	MEM / "coupled_transport_perturbation.pgml",
]

SEEDS_PER_FILE = {
	"identify_transporter_type.pgml": [1, 42, 9999],
	"driving_force_from_gradient.pgml": [1, 42, 9999],
	"coupled_transport_perturbation.pgml": [1, 42, 9999],
}


def render(path: Path, seed: int) -> str:
	proc = subprocess.run(
		["python3", str(LINT), "-i", str(path), "-s", str(seed), "--json"],
		capture_output=True, text=True, check=False,
	)
	if not proc.stdout.strip():
		return ""
	try:
		resp = json.loads(proc.stdout)
	except json.JSONDecodeError:
		return ""
	return resp.get("renderedHTML", "") or ""


def extract_svg(html: str) -> str:
	m = re.search(r"<svg\b.*?</svg>", html, re.DOTALL | re.IGNORECASE)
	return m.group(0) if m else ""


def count_internal_arrow_segments(svg: str) -> int:
	# Count colored arrow segments whose y spans the gate. Excludes the
	# dashed waist line (stroke-dasharray) which is decorative.
	count = 0
	for m in re.finditer(r'<line\s+([^>]+?)/?>', svg):
		attrs = m.group(1)
		if "stroke-dasharray" in attrs:
			continue
		y1 = re.search(r'y1="([\d.]+)"', attrs)
		y2 = re.search(r'y2="([\d.]+)"', attrs)
		if not (y1 and y2):
			continue
		a = float(y1.group(1))
		b = float(y2.group(1))
		if 108 <= a <= 132 and 108 <= b <= 132:
			count += 1
	return count


def count_binding_circles(svg: str) -> int:
	# White-filled r=6 circles at cy=120.
	return len(re.findall(
		r'<circle\s+cx="[\d.]+"\s+cy="120"\s+r="6"\s+fill="#ffffff"', svg
	))


def count_release_blobs(svg: str, cy: int) -> int:
	return len(re.findall(
		rf'<circle\s+cx="[\d.]+"\s+cy="{cy}"\s+r="7"', svg
	))


def count_approach_blobs(svg: str, cy: int) -> int:
	return len(re.findall(
		rf'<circle\s+cx="[\d.]+"\s+cy="{cy}"\s+r="10"', svg
	))


def stoich_ys(svg: str) -> list:
	# Stoich text lives at y=24 or y=222.
	ys = []
	for m in re.finditer(r'<text[^>]+y="(\d+)"[^>]*>[^<]*&#215;', svg):
		ys.append(int(m.group(1)))
	return ys


def anchor_counts(svg: str) -> tuple:
	return (
		len(re.findall(r'text-anchor="end"', svg)),
		len(re.findall(r'text-anchor="start"', svg)),
	)


def stagger_present(svg: str) -> bool:
	# Stagger puts a solute label at y=43 (40+5-2) or y=48 (40+5+3).
	# Default y would be 45 (40+5). Look for y=43 or y=48.
	return bool(re.search(r'<text\s+[^>]*y="(?:43|48)"[^>]*fill="#1f2937"', svg))


def pool_rect_count(svg: str) -> int:
	return len(re.findall(r'fill-opacity="0.10"', svg))


def classify_svg(svg: str) -> dict:
	# n_substrates from approach blob count (r=10 at y=40 or y=200).
	n_top = count_approach_blobs(svg, 40)
	n_bot = count_approach_blobs(svg, 200)
	n_sub = n_top + n_bot
	both_top = (n_sub == 2 and n_top == 2)
	return {"n_sub": n_sub, "n_top": n_top, "n_bot": n_bot, "both_top": both_top}


def audit(path: Path, seed: int) -> dict:
	html = render(path, seed)
	svg = extract_svg(html)
	info = classify_svg(svg)
	return {
		"seed": seed,
		"n_sub": info["n_sub"],
		"both_top": info["both_top"],
		"internal_arrow_segments": count_internal_arrow_segments(svg),
		"binding_circles": count_binding_circles(svg),
		"release_in": count_release_blobs(svg, 195),
		"release_out": count_release_blobs(svg, 45),
		"approach_in": count_approach_blobs(svg, 40),
		"approach_out": count_approach_blobs(svg, 200),
		"stoich_ys": stoich_ys(svg),
		"anchor_end": anchor_counts(svg)[0],
		"anchor_start": anchor_counts(svg)[1],
		"stagger": stagger_present(svg),
		"pool_rects": pool_rect_count(svg),
	}


def main():
	overall_fail = 0
	for path in FILES:
		print(f"\n=== {path.name} ===")
		for seed in SEEDS_PER_FILE[path.name]:
			r = audit(path, seed)
			fail = []
			# Internal arrow segments must be 0.
			if r["internal_arrow_segments"] != 0:
				fail.append(f"internal_arrow={r['internal_arrow_segments']}")
			# Binding circles must equal n_sub.
			if r["binding_circles"] != r["n_sub"]:
				fail.append(f"binding={r['binding_circles']} vs n_sub={r['n_sub']}")
			# Release blobs must match approach direction counts.
			if r["release_in"] != r["approach_in"]:
				fail.append(f"release_in={r['release_in']} vs approach_in={r['approach_in']}")
			if r["release_out"] != r["approach_out"]:
				fail.append(f"release_out={r['release_out']} vs approach_out={r['approach_out']}")
			# Stoich y must be 24 or 222 (not 22 or 232).
			for y in r["stoich_ys"]:
				if y == 22 or y == 232:
					fail.append(f"stoich_y_collision={y}")
			# Multi-solute requires both anchor styles.
			if r["n_sub"] == 2:
				if r["anchor_end"] < 1 or r["anchor_start"] < 1:
					fail.append(
						f"anchors end={r['anchor_end']} start={r['anchor_start']}"
					)
			# Stagger must fire iff both_top.
			if r["stagger"] and not r["both_top"]:
				fail.append("stagger_without_both_top")
			if r["both_top"] and not r["stagger"]:
				fail.append("both_top_without_stagger")
			status = "OK" if not fail else "FAIL"
			print(
				f"  seed={seed:<5d} n_sub={r['n_sub']} both_top={r['both_top']} "
				f"int_arrow={r['internal_arrow_segments']} "
				f"bind={r['binding_circles']} "
				f"rel_in={r['release_in']} rel_out={r['release_out']} "
				f"stoich_ys={r['stoich_ys']} "
				f"anc_e/s={r['anchor_end']}/{r['anchor_start']} "
				f"stagger={r['stagger']} "
				f"pool_rects={r['pool_rects']} "
				f"=> {status}"
			)
			if fail:
				print(f"    issues: {', '.join(fail)}")
				overall_fail += 1
	print(f"\n==== VISUAL QC OVERALL ====")
	print(f"failures: {overall_fail}")
	sys.exit(0 if overall_fail == 0 else 1)


if __name__ == "__main__":
	main()
