#!/usr/bin/env python3
"""CLI for synchronizing version metadata across a repository."""

# Standard Library
import sys
import argparse

# local repo modules
import version_lib
import version_files


ACTION_BUMPS = {
	"patch": "patch",
	"M": "major",
	"m": "minor",
	"p": "patch",
	"a": "alpha",
	"b": "beta",
	"r": "rc",
}
ADVANCED_HELP = argparse.SUPPRESS


def parse_args() -> argparse.Namespace:
	"""Parse command line arguments.

	Returns:
		argparse.Namespace: Parsed arguments.
	"""
	show_advanced = "--help-advanced" in sys.argv[1:]
	parser = argparse.ArgumentParser(
		description=(
			"Prepare one version change across common version files. "
			"The command shows a preview first."
		),
	)
	parser.add_argument(
		"--help-advanced",
		action="help",
		help="Show advanced options and exit.",
	)

	parser.add_argument(
		"-b", "--base-dir",
		dest="base_dir",
		default=".",
		help=advanced_help(show_advanced, "Base directory to scan."),
	)
	parser.add_argument(
		"-s", "--source",
		dest="source",
		default="",
		help=advanced_help(show_advanced, "Source file to anchor version selection."),
	)
	parser.add_argument(
		"-m", "--max-depth",
		dest="max_depth",
		type=int,
		default=4,
		help=advanced_help(show_advanced, "Max directory depth to scan."),
	)

	parser.add_argument(
		"action",
		nargs="?",
		default="",
		help="Enter a version such as 26.08.1, or type 'patch' to increase the last number.",
	)
	parser.add_argument(
		"--bump",
		dest="bump",
		default="",
		choices=["major", "minor", "patch", "alpha", "beta", "rc"],
		help=advanced_help(show_advanced, "Choose how to increase the current version."),
	)
	parser.add_argument(
		"-v", "--set-version",
		dest="set_version",
		default="",
		help="Use an exact version, such as 26.08.1.",
	)
	parser.add_argument(
		"-c", "--calver",
		dest="calver",
		action="store_true",
		help="Use the current year and month, such as 26.08.",
	)

	parser.add_argument(
		"-A", "--apply",
		dest="apply",
		action="store_true",
		help="Save the planned changes.",
	)
	parser.add_argument(
		"-n", "--dry-run",
		dest="apply",
		action="store_false",
		help=advanced_help(show_advanced, "Preview the changes."),
	)
	parser.set_defaults(apply=False)

	parser.add_argument(
		"-u", "--update-all",
		dest="update_all",
		action="store_true",
		help=advanced_help(show_advanced, "Set every discovered version to the same value."),
	)
	parser.add_argument(
		"--pre-style",
		dest="pre_style",
		choices=["pep440", "dash"],
		default="pep440",
		help=advanced_help(show_advanced, "Prerelease style when adding alpha/beta/rc."),
	)
	parser.add_argument(
		"--no-enforce-yy-mm",
		dest="enforce_yy_mm",
		action="store_false",
		help=advanced_help(show_advanced, "Accept any supported version format."),
	)
	parser.set_defaults(enforce_yy_mm=True)

	args = parser.parse_args()
	if args.calver and args.set_version:
		parser.error("Choose one version entry: --calver or --set-version.")
	if args.action:
		if args.action in ACTION_BUMPS:
			if args.bump:
				parser.error("Choose one way to increase the version.")
			if args.set_version or args.calver:
				parser.error(
					"Choose either an increase or an exact version."
				)
			args.bump = ACTION_BUMPS[args.action]
		else:
			if args.set_version or args.calver:
				parser.error("Choose one exact version entry.")
			args.set_version = args.action
	if args.calver:
		args.set_version = version_lib.current_calver_month()
	if not args.bump and not args.set_version:
		args.set_version = version_lib.current_calver_month()
	return args

#============================================

def advanced_help(show_advanced: bool, help_text: str) -> str:
	"""Return help text only when advanced help was requested.

	Args:
		show_advanced (bool): Whether advanced help is visible.
		help_text (str): Help text for the argument.

	Returns:
		str: Help text or argparse suppression marker.
	"""
	if show_advanced:
		return help_text
	return ADVANCED_HELP

#============================================


#============================================

def main() -> None:
	args = parse_args()
	base_dir = version_files.normalize_base_dir(args.base_dir)
	entries = version_files.parse_versions(base_dir, args.max_depth)

	base_version_override = ""
	explicit_version = ""
	if args.bump and args.set_version:
		base_version_override = version_lib.normalize_base_version_override(args.set_version)
		if not base_version_override:
			raise SystemExit("Enter a version after --set-version.")
	elif args.set_version:
		explicit_version = args.set_version.strip()
		if not explicit_version:
			raise SystemExit("Enter a version after --set-version.")

	if explicit_version:
		entries = version_files.ensure_version_file_entry(entries, base_dir)

	if not entries:
		raise SystemExit("No current version was found. Enter a version such as 26.08.1.")

	print("Current version files:")
	for entry in entries:
		entry_label = version_files.format_entry_label(entry, base_dir)
		version_display = entry["version"] if entry["version"] else "(empty)"
		if entry.get("create"):
			version_display = "(missing)"
		print(f"- {entry_label}: {version_display}")

	base_version_display = ""
	if base_version_override:
		base_version = base_version_override
		base_version_display = base_version
	elif explicit_version:
		versions = sorted(set(entry["version"] for entry in entries))
		if len(versions) == 1:
			base_version = versions[0]
			base_version_display = base_version
		else:
			base_version = ""
			base_version_display = "several versions"
	else:
		base_version = version_files.choose_base_version(entries, args.source)
		base_version_display = base_version

	if base_version_override and not args.update_all:
		version_found = any(
			version_lib.versions_match(entry["version"], base_version)
			for entry in entries
		)
		if not version_found:
			raise SystemExit(
				f"Version {base_version} was not found. Choose one of the listed versions."
			)

	if args.enforce_yy_mm and base_version:
		version_lib.validate_yy_mm_patch(base_version)
	if explicit_version:
		new_version = explicit_version
	else:
		new_version = version_lib.bump_version(base_version, args.bump, args.pre_style)
	if args.enforce_yy_mm:
		version_lib.validate_yy_mm_patch(new_version)

	print(f"Current version: {base_version_display}")
	print(f"Next version: {new_version}")

	if explicit_version or args.update_all:
		if all(version_lib.entry_matches_target(entry, new_version) for entry in entries):
			print("The version is already current. Nothing to change.")
			return
	else:
		if base_version == new_version:
			print("The version is already current. Nothing to change.")
			return

	if explicit_version or args.update_all:
		# Entries already at the target need no rewrite and stay out of the plan.
		selected = [entry for entry in entries if not version_lib.entry_matches_target(entry, new_version)]
		skipped = []
	else:
		selected = [
			entry for entry in entries
			if version_lib.versions_match(entry["version"], base_version)
		]
		skipped = [
			entry for entry in entries
			if not version_lib.versions_match(entry["version"], base_version)
		]

	if skipped:
		print("Keeping files with a different version:")
		for entry in skipped:
			entry_label = version_files.format_entry_label(entry, base_dir)
			print(f"- {entry_label}: {entry['version']}")

	print("Files to update:")
	for entry in selected:
		entry_label = version_files.format_entry_label(entry, base_dir)
		print(f"- {entry_label}")

	# Count distinct files: one Cargo.lock holds many package stanzas.
	changed_paths = set()
	for entry in selected:
		result = version_files.update_entry(entry, new_version, args.apply)
		if result["changed"]:
			changed_paths.add(result["path"])

	if args.apply:
		changed_count = len(changed_paths)
		file_word = "file" if changed_count == 1 else "files"
		print(f"Updated {changed_count} {file_word}.")
	else:
		print("Preview complete. Use --apply to save these changes.")


if __name__ == "__main__":
	main()
