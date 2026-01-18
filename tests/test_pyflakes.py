import os
import subprocess


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKIP_ENV = "SKIP_REPO_HYGIENE"


#============================================
def run_command(label: str, command: list[str], capture_output: bool = True) -> None:
	"""
	Run a command and raise with captured output on failure.

	Args:
		label: Short label for the command.
		command: Command list to run.
	"""
	if capture_output:
		result = subprocess.run(
			command,
			capture_output=True,
			text=True,
			cwd=REPO_ROOT,
		)
	else:
		result = subprocess.run(
			command,
			cwd=REPO_ROOT,
		)
	if result.returncode == 0:
		return
	stdout = ""
	stderr = ""
	if capture_output:
		stdout = result.stdout.strip()
		stderr = result.stderr.strip()
	message = [f"{label} failed with exit code {result.returncode}."]
	if stdout:
		message.append("stdout:")
		message.append(stdout)
	if stderr:
		message.append("stderr:")
		message.append(stderr)
	raise AssertionError("\n".join(message))


#============================================
def test_pyflakes() -> None:
	"""
	Run pyflakes script as a pytest gate.
	"""
	if os.environ.get(SKIP_ENV) == "1":
		return
	pyflakes_script = os.path.join(REPO_ROOT, "tests", "run_pyflakes.sh")
	run_command("pyflakes", ["bash", pyflakes_script])
