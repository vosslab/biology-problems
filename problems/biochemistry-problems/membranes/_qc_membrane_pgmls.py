#!/usr/bin/env python3
"""Automated QC across the three membrane-transporter PGMLs.

For each file, render at a broad sweep of seeds and verify:
  - renderer error_flag is zero
  - exactly 1 <svg> tag in body
  - no double-escaped HTML entities
  - expected text artifacts appear in the SVG (waist-line dasharray, no pore slot)
  - scenario / class branches are exercised across seeds
  - correct answer string is one of the rendered choices (anti-self-defeat)
  - substrate labels render at least once (tspan visible)
"""

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

LINT = Path.home() / ".claude/skills/webwork-writer/references/scripts/lint_pg_via_renderer_api.py"
MEMBRANES = Path(__file__).parent

FILES = [
	MEMBRANES / "identify_transporter_type.pgml",
	MEMBRANES / "driving_force_from_gradient.pgml",
	MEMBRANES / "coupled_transport_perturbation.pgml",
]

SEEDS = list(range(1, 25)) + [42, 100, 256, 1024, 4096, 9999]


def render(path: Path, seed: int) -> dict:
	proc = subprocess.run(
		["python3", str(LINT), "-i", str(path), "-s", str(seed), "--json"],
		capture_output=True, text=True, check=False,
	)
	if not proc.stdout.strip():
		return {"_err": "empty stdout", "_stderr": proc.stderr[:400]}
	try:
		return json.loads(proc.stdout)
	except json.JSONDecodeError as exc:
		return {"_err": f"json decode: {exc}", "_raw": proc.stdout[:400]}


def correct_answers_from_response(resp: dict) -> dict:
	"""Extract {answer_name: correct_value} from the renderer response."""
	out = {}
	answers = resp.get("answers") or {}
	for name, info in answers.items():
		if not isinstance(info, dict):
			continue
		val = info.get("correct_value") or info.get("correct_ans")
		if val is not None:
			out[name] = val
	return out


def radio_choice_labels(html: str, name: str) -> list:
	"""Extract radio-button label texts for a given answer name."""
	# The rendered labels look like: <label>...<INPUT TYPE=RADIO NAME="AnSwErNNNN" ...VALUE="B0" >...</label>
	# We pull all <label>...</label> that contain an INPUT with NAME=name.
	labels = []
	for m in re.finditer(r"<label>(.*?)</label>", html, re.DOTALL | re.IGNORECASE):
		inner = m.group(1)
		if re.search(rf'NAME="{re.escape(name)}"', inner, re.IGNORECASE):
			# strip HTML tags to get text
			text = re.sub(r"<[^>]+>", "", inner)
			text = re.sub(r"\s+", " ", text).strip()
			labels.append(text)
	return labels


def popup_options(html: str, name: str) -> list:
	"""Extract <select><option>...</option></select> options for a popup."""
	m = re.search(
		rf'<select[^>]*name="{re.escape(name)}"[^>]*>(.*?)</select>',
		html, re.DOTALL | re.IGNORECASE,
	)
	if not m:
		return []
	return re.findall(r"<option[^>]*>([^<]*)</option>", m.group(1))


def audit_file(path: Path, level: int) -> dict:
	print(f"\n=== {path.name} (Level {level}) ===")
	results = {
		"errors": 0,
		"svg_mismatch": 0,
		"double_escape": 0,
		"waist_missing": 0,
		"pore_slot_present": 0,
		"tspan_missing": 0,
		"correct_not_in_choices": 0,
		"class_coverage": Counter(),
		"scenario_coverage": Counter(),
		"variant_coverage": Counter(),
	}
	for seed in SEEDS:
		resp = render(path, seed)
		if resp.get("_err"):
			print(f"  seed {seed}: FAIL ({resp['_err']})")
			results["errors"] += 1
			continue
		flags = resp.get("flags") or {}
		debug = resp.get("debug") or {}
		if flags.get("error_flag"):
			print(f"  seed {seed}: error_flag set; internal={debug.get('internal')}")
			results["errors"] += 1
			continue
		html = resp.get("renderedHTML") or ""

		svg_count = len(re.findall(r"<svg", html))
		if svg_count != 1:
			print(f"  seed {seed}: SVG count = {svg_count}")
			results["svg_mismatch"] += 1
		for pat in (r"&amp;#215;", r"&amp;lt;tspan", r"&amp;sup", r"&amp;alpha",
		            r"&amp;beta", r"&amp;times", r"&amp;amp;"):
			if re.search(pat, html):
				print(f"  seed {seed}: double-escape: {pat}")
				results["double_escape"] += 1
				break
		if 'stroke-dasharray="4,3"' not in html:
			results["waist_missing"] += 1
		if re.search(r'<rect\s+x="202"\s+y="78"', html):
			results["pore_slot_present"] += 1
		# tspan for sub/superscripts should appear at least once across seeds
		if "<tspan" not in html:
			results["tspan_missing"] += 1

		correct = correct_answers_from_response(resp)

		if level == 1:
			# Level 1 has PopUp (AnSwEr0001) + RadioButtons (AnSwEr0002).
			popup_name = "AnSwEr0001"
			popup_correct = correct.get(popup_name)
			popup_opts = popup_options(html, popup_name)
			if popup_correct and popup_correct not in popup_opts:
				print(f"  seed {seed}: popup correct '{popup_correct}' not in options {popup_opts}")
				results["correct_not_in_choices"] += 1
			if popup_correct:
				results["class_coverage"][popup_correct] += 1
			radio_name = "AnSwEr0002"
			radio_correct = correct.get(radio_name)
			radio_labels = radio_choice_labels(html, radio_name)
			if radio_correct is not None:
				# correct can be 'B0','B1','B2','B3' mapping to radio index
				if isinstance(radio_correct, str) and re.match(r"^B\d+$", radio_correct):
					idx = int(radio_correct[1:])
					if idx >= len(radio_labels):
						print(f"  seed {seed}: radio correct {radio_correct} out of range (labels: {len(radio_labels)})")
						results["correct_not_in_choices"] += 1
		elif level == 2:
			radio_name = "AnSwEr0001"
			radio_correct = correct.get(radio_name)
			radio_labels = radio_choice_labels(html, radio_name)
			if radio_correct is not None:
				if isinstance(radio_correct, str) and re.match(r"^B\d+$", radio_correct):
					idx = int(radio_correct[1:])
					if idx >= len(radio_labels):
						print(f"  seed {seed}: radio correct {radio_correct} out of range")
						results["correct_not_in_choices"] += 1
			# Detect scenario by substrate-pair fingerprint in the question body
			# (SVG text_attributes are hard to recover; use substrate plain labels
			# embedded in the PGML body).
			# Scenarios 0..3: Na+/glucose (sym), Na+/Ca2+ (anti), H+/lactose (sym), Na+/H+ (anti)
			lower = html.lower()
			# Tag by substrate pair visible in the body.
			body_frag = html
			if "glucose" in body_frag.lower() and "na+" in radio_labels_text(radio_labels).lower():
				results["scenario_coverage"]["sym-Na/glucose"] += 1
			if "lactose" in body_frag.lower():
				results["scenario_coverage"]["sym-H/lactose"] += 1
			# antiporter pairs: identify by the "against its own gradient" solute text
			# (sub1 appears in variant 2 prompt). Fallback: look at radio choices for
			# Ca2+ or H+.
			for lbl in radio_labels:
				if "Ca2+" in lbl:
					results["scenario_coverage"]["anti-Na/Ca"] += 1
					break
				if lbl.strip() == "H+":
					# could be either sym-H or anti-Na/H; discriminate by presence of lactose
					if "lactose" in body_frag.lower():
						pass
					else:
						results["scenario_coverage"]["anti-Na/H"] += 1
					break
			# Variant (prompt phrasing): look for distinctive strings
			if "moving <b>down</b>" in html:
				results["variant_coverage"]["down"] += 1
			elif "provides the driving force" in html:
				results["variant_coverage"]["driver"] += 1
			elif "its own concentration gradient" in html:
				results["variant_coverage"]["own-gradient"] += 1
		elif level == 3:
			radio_name = "AnSwEr0001"
			radio_correct = correct.get(radio_name)
			radio_labels = radio_choice_labels(html, radio_name)
			if radio_correct is not None:
				if isinstance(radio_correct, str) and re.match(r"^B\d+$", radio_correct):
					idx = int(radio_correct[1:])
					if idx >= len(radio_labels):
						print(f"  seed {seed}: radio correct {radio_correct} out of range")
						results["correct_not_in_choices"] += 1
			if "ouabain" in html.lower():
				results["scenario_coverage"]["A-ouabain"] += 1
			elif "net electrical charge" in html.lower():
				results["scenario_coverage"]["B-netcharge"] += 1
			elif "ischemia" in html.lower() or "run in <b>reverse" in html.lower():
				results["scenario_coverage"]["C-reverse"] += 1
			elif "convert it into an <b>antiporter" in html.lower() or "what-change" in html.lower():
				results["scenario_coverage"]["D-whatchange"] += 1

	print(f"  errors: {results['errors']}")
	print(f"  svg_mismatch: {results['svg_mismatch']}")
	print(f"  double_escape: {results['double_escape']}")
	print(f"  waist_missing: {results['waist_missing']}")
	print(f"  pore_slot_present: {results['pore_slot_present']}")
	print(f"  tspan_missing: {results['tspan_missing']}")
	print(f"  correct_not_in_choices: {results['correct_not_in_choices']}")
	if results["class_coverage"]:
		print(f"  class coverage: {dict(results['class_coverage'])}")
	if results["scenario_coverage"]:
		print(f"  scenario coverage: {dict(results['scenario_coverage'])}")
	if results["variant_coverage"]:
		print(f"  variant coverage: {dict(results['variant_coverage'])}")
	return results


def radio_labels_text(labels):
	return " ".join(labels)


def main():
	summary = {}
	for i, path in enumerate(FILES):
		summary[path.name] = audit_file(path, level=i + 1)
	bad = 0
	for name, r in summary.items():
		if (r["errors"] or r["svg_mismatch"] or r["double_escape"]
				or r["waist_missing"] or r["pore_slot_present"]
				or r["correct_not_in_choices"]):
			bad += 1
	print(f"\n==== OVERALL ====")
	print(f"Files audited: {len(FILES)}, files with issues: {bad}")
	sys.exit(0 if bad == 0 else 1)


if __name__ == "__main__":
	main()
