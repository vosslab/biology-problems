"""Shared version parsing, normalization, and text-update behavior."""

# Standard Library
import os
import re
import datetime

BASE_VERSION_PATTERN = re.compile(r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)$")
PEP440_PATTERN = re.compile(
	r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?P<tag>a|b|rc)(?P<num>\d+)$"
)
SHORT_PEP440_PATTERN = re.compile(
	r"^(?P<major>\d+)\.(?P<minor>\d+)(?P<tag>a|b|rc)(?P<num>\d+)$"
)
DASH_PATTERN = re.compile(
	r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)-(?P<tag>alpha|beta|rc)"
	r"(?:[\\.-]?(?P<num>\d+))?$"
)
YY_MM_PATCH_PATTERN = re.compile(
	r"^(?P<major>\d{2})\.(?P<minor>\d{2})\.(?P<patch>\d+)"
	r"(?:(?P<tag>a|b|rc)(?P<num>\d+))?$"
)
YY_MM_SHORT_PATTERN = re.compile(
	r"^(?P<major>\d{2})\.(?P<minor>\d{2})(?P<tag>a|b|rc)(?P<num>\d+)$"
)
YY_MM_BARE_PATTERN = re.compile(r"^(?P<major>\d{2})\.(?P<minor>\d{2})$")
SIMPLE_VERSION_PATTERN = re.compile(r"\d+\.\d+\.\d+(?:[A-Za-z0-9\.-]+)?")
ASSIGNMENT_PATTERN = re.compile(
	r"^(?P<indent>\s*)(?P<name>__version__|VERSION|version)\s*=\s*"
	r"(?P<quote>['\"])(?P<version>[^'\"]+)(?P=quote)(?P<rest>.*)$"
)
SECTION_HEADER_PATTERN = re.compile(r"^\[(?P<section>[^\]]+)\]\s*$")
VERSION_LINE_PATTERN = re.compile(
	r"^(?P<indent>\s*)version\s*=\s*(?P<quote>['\"])(?P<version>[^'\"]+)(?P=quote)(?P<rest>.*)$"
)
CARGO_PACKAGE_HEADER_PATTERN = re.compile(r"^\[\[package\]\]\s*$")
# Prerelease tag vocabularies, one per direction. Previously rebuilt inside
# parse_version_details (twice), format_version, and normalize_cargo_version.
# PRE_TAG_NAMES: PEP 440 short tag as written -> internal long name.
PRE_TAG_NAMES = {
	"a": "alpha",
	"b": "beta",
	"rc": "rc",
}
# PRE_TAG_SHORT: internal long name -> PEP 440 short tag (the inverse).
PRE_TAG_SHORT = {
	"alpha": "a",
	"beta": "b",
	"rc": "rc",
}
# CARGO_PRE_TAG_NAMES: Cargo emits long names and accepts either spelling,
# since parse_version_details keeps dash-style tags in their source form.
CARGO_PRE_TAG_NAMES = {
	"a": "alpha",
	"alpha": "alpha",
	"b": "beta",
	"beta": "beta",
	"rc": "rc",
}
#============================================

def current_calver_month() -> str:
	"""Return the current month in repo CalVer format.

	Kept local rather than imported from devel/changelog_lib.py: that module
	pulls in rich, and this tool stays stdlib-only.

	Returns:
		str: Current YY.MM value.
	"""
	today = datetime.date.today()
	return f"{today.year % 100:02d}.{today.month:02d}"

#============================================

def calver_month_prefix(version: str) -> str:
	"""Extract the leading numeric year/month pair from a CalVer version."""
	version_parts = version.split(".")
	if len(version_parts) < 2:
		raise RuntimeError(f"Malformed CalVer version: {version!r}")
	year_part, month_part = version_parts[:2]
	if not (year_part.isdigit() and month_part.isdigit()):
		raise RuntimeError(f"Malformed CalVer version: {version!r}")
	return f"{year_part}.{month_part}"

#============================================

def read_version_file(project_dir: str) -> str:
	"""Read the root VERSION file and return its stripped value."""
	version_path = os.path.join(project_dir, "VERSION")
	if not os.path.isfile(version_path):
		raise RuntimeError(f"VERSION file not found at repo root: {version_path}")
	with open(version_path, "r") as version_file:
		return version_file.read().strip()

#============================================

def verify_version_sync(metadata_version: str, file_version: str) -> None:
	"""Require a metadata version and root VERSION value to match."""
	if metadata_version != file_version:
		raise RuntimeError(
			"VERSION does not match project metadata: "
			f"{file_version} != {metadata_version}"
		)

#============================================

def normalize_base_version_override(value: str) -> str:
	"""Normalize a base version override string.

	Args:
		value (str): Base version override.

	Returns:
		str: Normalized base version.
	"""
	candidate = value.strip()
	if re.fullmatch(r"\d{2}\.\d{2}", candidate):
		return f"{candidate}.0"
	return candidate

#============================================


#============================================

def is_version_candidate(text: str) -> bool:
	"""Check whether a string looks like a version.

	Args:
		text (str): Version candidate.

	Returns:
		bool: True if it looks like a version.
	"""
	value = text.strip()
	if not value:
		return False
	try:
		parse_version_details(value)
		return True
	except ValueError:
		pass
	if SIMPLE_VERSION_PATTERN.fullmatch(value):
		return True
	return False

#============================================

def bump_version(version: str, bump: str, pre_style: str) -> str:
	"""Bump a semantic version.

	Args:
		version (str): Current version string.
		bump (str): major, minor, patch, alpha, beta, or rc.
		pre_style (str): pep440 or dash.

	Returns:
		str: New version string.
	"""
	details = parse_version_details(version)
	if bump in ("major", "minor", "patch"):
		if details["pre_tag"] or details["pre_num"] is not None:
			raise ValueError(f"Remove prerelease suffix before bumping: {version}")
		if bump == "major":
			details["major"] += 1
			details["minor"] = 0
			details["patch"] = 0
		elif bump == "minor":
			details["minor"] += 1
			details["patch"] = 0
		else:
			details["patch"] += 1
		details["pre_tag"] = None
		details["pre_num"] = None
		return format_version(details)

	if bump in ("alpha", "beta", "rc"):
		return bump_prerelease(details, bump, pre_style)

	raise ValueError(f"Unsupported bump mode: {bump}")

#============================================

def version_number_parts(
	major_text: str,
	minor_text: str,
	patch_text: str | None=None,
) -> dict:
	"""Convert version segment text into numeric values plus original widths.

	The width fields are the zero-padding filter: they record that "08" was
	two characters so 26.08 can be rebuilt as 26.08 rather than 26.8, while
	the numeric fields drive arithmetic and the unpadded Cargo form. A version
	with no patch segment reports patch 0 at width 1.

	Args:
		major_text (str): Major segment as written.
		minor_text (str): Minor segment as written.
		patch_text (str | None): Patch segment as written, or None when absent.

	Returns:
		dict: Numeric major/minor/patch and their source widths.
	"""
	parts = {
		"major": int(major_text),
		"minor": int(minor_text),
		"patch": int(patch_text) if patch_text is not None else 0,
		"major_width": len(major_text),
		"minor_width": len(minor_text),
		"patch_width": len(patch_text) if patch_text is not None else 1,
	}
	return parts

#============================================

def parse_version_details(version: str) -> dict:
	"""Parse a version string into parts.

	Args:
		version (str): Version string.

	Returns:
		dict: Parsed version parts.
	"""
	match = PEP440_PATTERN.match(version)
	if match:
		details = version_number_parts(
			match.group("major"),
			match.group("minor"),
			match.group("patch"),
		)
		details.update({
			"pre_tag": PRE_TAG_NAMES[match.group("tag")],
			"pre_num": int(match.group("num")),
			"style": "pep440",
		})
		return details

	match = SHORT_PEP440_PATTERN.match(version)
	if match:
		details = version_number_parts(match.group("major"), match.group("minor"))
		details.update({
			"pre_tag": PRE_TAG_NAMES[match.group("tag")],
			"pre_num": int(match.group("num")),
			"style": "pep440",
			"patch_optional": True,
		})
		return details

	match = DASH_PATTERN.match(version)
	if match:
		num_text = match.group("num")
		details = version_number_parts(
			match.group("major"),
			match.group("minor"),
			match.group("patch"),
		)
		details.update({
			"pre_tag": match.group("tag"),
			"pre_num": int(num_text) if num_text else 0,
			"style": "dash",
		})
		return details

	match = YY_MM_PATCH_PATTERN.match(version)
	if match:
		num_text = match.group("num")
		details = version_number_parts(
			match.group("major"),
			match.group("minor"),
			match.group("patch"),
		)
		details.update({
			"pre_tag": match.group("tag"),
			"pre_num": int(num_text) if num_text else None,
			"style": "pep440",
			"patch_optional": False,
		})
		return details

	match = YY_MM_SHORT_PATTERN.match(version)
	if match:
		details = version_number_parts(match.group("major"), match.group("minor"))
		details.update({
			"pre_tag": match.group("tag"),
			"pre_num": int(match.group("num")),
			"style": "pep440",
			"patch_optional": True,
		})
		return details

	match = YY_MM_BARE_PATTERN.match(version)
	if match:
		details = version_number_parts(match.group("major"), match.group("minor"))
		details.update({
			"pre_tag": None,
			"pre_num": None,
			"style": "pep440",
			"patch_optional": True,
		})
		return details

	match = BASE_VERSION_PATTERN.match(version)
	if match:
		details = version_number_parts(
			match.group("major"),
			match.group("minor"),
			match.group("patch"),
		)
		details.update({
			"pre_tag": None,
			"pre_num": None,
			"style": "none",
			"patch_optional": False,
		})
		return details

	raise ValueError(f"Unsupported version format: {version}")

#============================================

def version_identity(version: str) -> tuple[int, int, int, str | None, int | None]:
	"""Return the release identity without file-specific number formatting."""
	details = parse_version_details(version)
	identity = (
		details["major"],
		details["minor"],
		details["patch"],
		details["pre_tag"],
		details["pre_num"],
	)
	return identity

#============================================

def versions_match(first: str, second: str) -> bool:
	"""Check whether two file representations describe the same release."""
	matches = version_identity(first) == version_identity(second)
	return matches

#============================================

def is_repo_calver(version: str) -> bool:
	"""Check whether a version uses the repository's padded year and month."""
	matches = (
		YY_MM_PATCH_PATTERN.match(version)
		or YY_MM_SHORT_PATTERN.match(version)
		or YY_MM_BARE_PATTERN.match(version)
	)
	return bool(matches)

#============================================

def validate_yy_mm_patch(version: str) -> None:
	"""Validate YY.MM.PATCH format with optional PEP 440 prerelease suffix.

	Args:
		version (str): Version string.
	"""
	match = YY_MM_PATCH_PATTERN.match(version)
	match_short = YY_MM_SHORT_PATTERN.match(version)
	match_bare = YY_MM_BARE_PATTERN.match(version)
	if not match and not match_short and not match_bare:
		raise ValueError(
			f"Version must be YY.MM, YY.MM.PATCH, or YY.MM prerelease: {version}"
		)

	month_text = (match or match_short or match_bare).group("minor")
	month = int(month_text)
	if month < 1 or month > 12:
		raise ValueError(f"Invalid month in version: {version}")

#============================================

def format_version(details: dict) -> str:
	"""Format a version string from parts.

	Args:
		details (dict): Version parts.

	Returns:
		str: Formatted version.
	"""
	major = format_number(details["major"], details.get("major_width"))
	minor = format_number(details["minor"], details.get("minor_width"))
	patch = format_number(details["patch"], details.get("patch_width"))
	base = f"{major}.{minor}.{patch}"
	if not details["pre_tag"]:
		return base

	pre_num = details["pre_num"] if details["pre_num"] is not None else 1
	if details["style"] == "pep440":
		return f"{base}{PRE_TAG_SHORT[details['pre_tag']]}{pre_num}"

	return f"{base}-{details['pre_tag']}.{pre_num}"

#============================================

def format_number(value: int, width: int | None) -> str:
	"""Format a number with optional zero padding.

	Args:
		value (int): Numeric value.
		width (int | None): Minimum width to preserve.

	Returns:
		str: Formatted number.
	"""
	text = str(value)
	if width and len(text) < width:
		return text.zfill(width)
	return text

#============================================
def bump_prerelease(details: dict, tag: str, pre_style: str) -> str:
	"""Bump or add a prerelease suffix.

	Args:
		details (dict): Parsed version details.
		tag (str): alpha, beta, or rc.
		pre_style (str): pep440 or dash.

	Returns:
		str: Updated version.
	"""
	style = details["style"]
	if style == "none":
		style = pre_style
	details = dict(details)
	details["style"] = style
	if details["pre_tag"] == tag:
		if details["pre_num"] is None:
			details["pre_num"] = 1
		else:
			details["pre_num"] += 1
	else:
		details["pre_tag"] = tag
		details["pre_num"] = 1
	return format_version(details)

#============================================

def update_pyproject(text: str, sections: list[str], new_version: str) -> tuple[str, bool]:
	"""Update version lines in a pyproject.toml string.

	Args:
		text (str): File contents.
		sections (list[str]): Sections to update.
		new_version (str): New version.

	Returns:
		tuple[str, bool]: Updated text and changed flag.
	"""
	lines = text.splitlines(keepends=True)
	changed = False

	active_section = None
	for index, line in enumerate(lines):
		match = SECTION_HEADER_PATTERN.match(line.strip())
		if match:
			active_section = match.group("section")
			continue

		if active_section not in sections:
			continue

		match = VERSION_LINE_PATTERN.match(line)
		if not match:
			continue

		indent = match.group("indent")
		quote = match.group("quote")
		rest = match.group("rest")
		newline = "\n" if line.endswith("\n") else ""
		lines[index] = f"{indent}version = {quote}{new_version}{quote}{rest}{newline}"
		changed = True

	return "".join(lines), changed

#============================================

def normalize_cargo_version(version: str) -> str:
	"""Convert a supported repo version to Cargo's SemVer representation.

	Args:
		version (str): Repo version string.

	Returns:
		str: Three-part SemVer without leading zeroes.
	"""
	details = parse_version_details(version)
	base = f"{details['major']}.{details['minor']}.{details['patch']}"
	if not details["pre_tag"]:
		return base

	tag = CARGO_PRE_TAG_NAMES[details["pre_tag"]]
	pre_num = details["pre_num"] if details["pre_num"] is not None else 0
	cargo_version = f"{base}-{tag}.{pre_num}"
	return cargo_version

#============================================

def normalize_target_version(entry: dict, new_version: str) -> str:
	"""Normalize the target version for entries without a patch segment.

	Args:
		entry (dict): Version entry metadata.
		new_version (str): Target version.

	Returns:
		str: Adjusted version string.
	"""
	if entry["kind"] in ("cargo_toml", "cargo_lock"):
		return normalize_cargo_version(new_version)
	if entry.get("patch_optional") and new_version.endswith(".0"):
		short_version = new_version.replace(".0", "", 1)
		if SHORT_PEP440_PATTERN.match(short_version):
			return short_version
	return new_version

#============================================

def entry_matches_target(entry: dict, new_version: str) -> bool:
	"""Check whether an entry already contains its normalized target version.

	Args:
		entry (dict): Version entry metadata.
		new_version (str): Repo target version.

	Returns:
		bool: True when no update is needed.
	"""
	target_version = normalize_target_version(entry, new_version)
	matches = entry["version"] == target_version
	return matches

#============================================

def update_simple_version(text: str, new_version: str, force_update: bool=False) -> tuple[str, bool]:
	"""Update a simple version file.

	Args:
		text (str): File contents.
		new_version (str): New version.
		force_update (bool): Update first non-empty line even if not a version.

	Returns:
		tuple[str, bool]: Updated text and changed flag.
	"""
	lines = text.splitlines(keepends=True)
	for index, line in enumerate(lines):
		strip_line = line.strip()
		if not strip_line or strip_line.startswith("#"):
			continue
		if not is_version_candidate(strip_line) and not force_update:
			break
		newline = "\n" if line.endswith("\n") else ""
		lines[index] = f"{new_version}{newline}"
		return "".join(lines), True

	if force_update:
		return f"{new_version}\n", True

	return text, False

#============================================

def update_version_py(text: str, new_version: str) -> tuple[str, bool]:
	"""Update version assignments in version.py.

	Args:
		text (str): File contents.
		new_version (str): New version.

	Returns:
		tuple[str, bool]: Updated text and changed flag.
	"""
	lines = text.splitlines(keepends=True)
	changed = False
	for index, line in enumerate(lines):
		match = ASSIGNMENT_PATTERN.match(line)
		if not match:
			continue
		indent = match.group("indent")
		name = match.group("name")
		quote = match.group("quote")
		rest = match.group("rest")
		newline = "\n" if line.endswith("\n") else ""
		lines[index] = f"{indent}{name} = {quote}{new_version}{quote}{rest}{newline}"
		changed = True

	return "".join(lines), changed

#============================================

def update_cargo_lock(text: str, package_index: int, new_version: str) -> tuple[str, bool]:
	"""Update one local package version in Cargo.lock.

	Args:
		text (str): File contents.
		package_index (int): Zero-based index of the package stanza to update.
		new_version (str): New version.

	Returns:
		tuple[str, bool]: Updated text and changed flag.
	"""
	lines = text.splitlines(keepends=True)
	current_package_index = -1
	for index, line in enumerate(lines):
		if CARGO_PACKAGE_HEADER_PATTERN.match(line.strip()):
			current_package_index += 1
			continue
		if current_package_index != package_index:
			continue
		match = VERSION_LINE_PATTERN.match(line)
		if not match:
			continue
		indent = match.group("indent")
		quote = match.group("quote")
		rest = match.group("rest")
		newline = "\n" if line.endswith("\n") else ""
		lines[index] = f"{indent}version = {quote}{new_version}{quote}{rest}{newline}"
		return "".join(lines), True

	return text, False

#============================================
