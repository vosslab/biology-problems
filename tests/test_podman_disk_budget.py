# This file is vendored. Local changes can and will be overwritten by propagation.

"""Keep the mandatory Podman disk budget in pytest's base lane.

Run this guard with ``source source_me.sh && python3 -m pytest tests/``.
Podman storage is shared across repositories, so every normal test run checks it.
Continuous development must use the developer volume responsibly, so this is
not an optional or E2E-only check. If it fails, inspect the detailed usage and
deliberately remove stale resources before continuing development.
"""

# Standard Library
import json
import subprocess


MAX_PODMAN_SIZE_BYTES = 20 * 1000 * 1000 * 1000


#============================================
def podman_storage_size_bytes() -> int:
	"""Return total image, container, and volume bytes for the active connection."""
	result = subprocess.run(
		["podman", "system", "df", "--format", "json"],
		check=False,
		capture_output=True,
		text=True,
	)
	if result.returncode != 0:
		raise RuntimeError(f"podman system df failed: {result.stderr.strip()}")
	usage_rows = json.loads(result.stdout)
	total_bytes = sum(row["RawSize"] for row in usage_rows)
	return total_bytes


#============================================
def test_podman_disk_usage_stays_under_20_gb() -> None:
	"""Keep Podman-managed images, containers, and volumes within budget."""
	actual_bytes = podman_storage_size_bytes()
	assert actual_bytes <= MAX_PODMAN_SIZE_BYTES, (
		"Podman disk usage is "
		f"{actual_bytes / (1000 * 1000 * 1000):.2f} GB; the budget is 20.00 GB. "
		"Inspect `podman system df -v` and deliberately remove stale Podman resources."
	)
