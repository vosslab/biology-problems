#!/usr/bin/env python3

"""Write a traceable report of baseline-to-curated task CSV changes."""

# Standard Library
import csv
import argparse
import collections

# local repo modules
import topic_classifier.validate_task_files as validator


REPORT_COLUMNS = [
	"subject", "chapter", "source", "variant", "prior_assignment",
	"final_assignment", "reason",
]


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(description="Report curated task CSV changes.")
	parser.add_argument("--baseline", required=True, help="Baseline task CSV directory.")
	parser.add_argument("--curated", required=True, help="Curated task CSV directory.")
	parser.add_argument("--output", required=True, help="Output report CSV path.")
	return parser.parse_args()


#============================================
def row_key(row: dict) -> tuple:
	"""Return the normalized concrete-variant and subject identity."""
	return (row["script"], row["flags"], row["input"], row["subject"])


#============================================
def variant_key(row: dict) -> tuple:
	"""Return the normalized concrete-variant identity without subject."""
	return (row["script"], row["flags"], row["input"])


#============================================
def variant_label(row: dict) -> str:
	"""Return a compact, reviewable concrete-variant label."""
	parts = [row["script"]]
	if row["flags"]:
		parts.append(f"flags={row['flags']}")
	if row["input"]:
		parts.append(f"input={row['input']}")
	return " | ".join(parts)


#============================================
def build_report(baseline_rows: list, curated_rows: list) -> list:
	"""Build one trace row for every additive assignment."""
	baseline_counts = collections.Counter(
		tuple(row[column] for column in validator.CSV_COLUMNS)
		for row in baseline_rows
	)
	curated_counts = collections.Counter(
		tuple(row[column] for column in validator.CSV_COLUMNS)
		for row in curated_rows
	)
	if baseline_counts - curated_counts:
		raise ValueError("Curated task files must preserve every baseline row unchanged")

	baseline_by_key = {row_key(row): row for row in baseline_rows}
	curated_by_key = {row_key(row): row for row in curated_rows}
	baseline_variants = {variant_key(row) for row in baseline_rows}
	report = []

	for key, final_row in sorted(curated_by_key.items()):
		prior_row = baseline_by_key.get(key)
		if prior_row is not None:
			continue
		if variant_key(final_row) in baseline_variants:
			reason = "prior narrow-policy omission"
			prior_assignment = "not assigned in this subject"
		else:
			reason = "previously unassigned"
			prior_assignment = "unassigned"
		report.append({
			"subject": final_row["subject"],
			"chapter": final_row["topic"],
			"source": validator.source_path(final_row) or final_row["script"],
			"variant": variant_label(final_row),
			"prior_assignment": prior_assignment,
			"final_assignment": f"{final_row['subject']}/{final_row['topic']}",
			"reason": reason,
		})

	return report


#============================================
def main() -> None:
	"""Write the requested curation report."""
	args = parse_args()
	baseline_rows, baseline_errors = validator.load_rows(args.baseline)
	curated_rows, curated_errors = validator.load_rows(args.curated)
	errors = baseline_errors + curated_errors
	if errors:
		raise ValueError("; ".join(errors))
	report = build_report(baseline_rows, curated_rows)
	with open(args.output, "w", newline="") as handle:
		writer = csv.DictWriter(handle, fieldnames=REPORT_COLUMNS)
		writer.writeheader()
		writer.writerows(report)
	print(f"Curation changes: {len(report)}")
	print(f"Report: {args.output}")


if __name__ == "__main__":
	main()
