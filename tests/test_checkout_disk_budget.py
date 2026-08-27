# Standard Library
import subprocess

# Local
import file_utils


MAX_CHECKOUT_SIZE_KIB = 20 * 1024 * 1024


#============================================
def checkout_size_kib(repo_root: str) -> int:
	"""Return the physical checkout usage in KiB, matching ``du -sh`` scope."""
	result = subprocess.run(
		["du", "-sk", repo_root],
		check=True,
		capture_output=True,
		text=True,
	)
	return int(result.stdout.split(maxsplit=1)[0])


#============================================
def test_checkout_disk_usage_stays_under_20_gib() -> None:
	"""Keep generated build data from consuming the developer volume."""
	repo_root = file_utils.get_repo_root()
	actual_kib = checkout_size_kib(repo_root)
	assert actual_kib <= MAX_CHECKOUT_SIZE_KIB, (
		"checkout disk usage is "
		f"{actual_kib / (1024 * 1024):.1f} GiB; the budget is 20.0 GiB. "
		"Remove stale generated build outputs before continuing."
	)
# Vendored pytest file. Local changes can and will be overwritten.
