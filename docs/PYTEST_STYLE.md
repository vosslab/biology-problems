# PYTEST_STYLE.md

Language Model guide to Neil pytest usage.

## Test structure

* Prefer pytest for automated tests when a repo has more than a few simple asserts.
* `tests/` (including `tests/playwright/` and `tests/e2e/`) is the only place `assert` statements should appear in this repo. Plain scripts and library modules must not contain `assert`. See [PYTHON_STYLE.md](PYTHON_STYLE.md#assert) for the rationale (module-level asserts slow script startup).
* Pytest is the fast lane: keep tests deterministic and quick. Slow end-to-end tests live in `tests/playwright/` (browser-driven) and `tests/e2e/` (shell/Python) and run outside pytest (excluded via `collect_ignore = ["e2e", "playwright"]` in `tests/conftest.py`); see [E2E_TESTS.md](E2E_TESTS.md).
* Store tests in `tests/` with files named `test_*.py`.
* Use `tests/conftest.py` for pytest configuration, fixtures, collection hooks, and shared pytest setup.
* Test functions should be named `test_*` and should use plain `assert`.
* Keep tests small and deterministic.
* Avoid network calls, random behavior, and time based logic unless mocked.
* Prefer fixtures for setup and shared resources.
* Use built in fixtures like `tmp_path` instead of custom temp directories.
* Avoid complex logic inside tests.
* If test logic needs comments, move the logic into helper functions and test those helpers.
* Before writing any test, ask: "will this test still pass next week without code changes?"
* If a test will not stay stable without code changes, do not write it.
* One or two assertions per function is enough.
* Five assertions for a simple function is overkill.
* Do not test trivial behavior or thin wrappers around standard library calls.
* Do not create permanent pytest files for temporary or scratch code.
* Do not write tests for `_temp.*` files, ad-hoc debugging scripts, or any code intended to be deleted shortly after use.
* Tests in `tests/` are reserved for code that will remain in the repo.

## Runtime budget

* Every pytest under `tests/` should finish in well under one second. `pytest tests/` is the
  fast lane; slow tests poison it and discourage running the suite during development.
* If a check needs sleeps, real subprocess calls, real network, large file trees beyond
  `tmp_path`, model loads, or a multi-step CLI run, it is not a pytest. Move it to
  `tests/playwright/` (browser-driven) or `tests/e2e/` (shell/Python) per [E2E_TESTS.md](E2E_TESTS.md).
* Prefer deleting a slow or fragile pytest over rewriting it. Less is more.

## Good tests

Tests should verify logic that could plausibly be wrong, using assertions that remain stable
when unrelated code changes. Good tests survive refactors, renamed fields, added config keys,
and tuned constants.

* **Pure function correctness**: fixed inputs produce expected outputs, such as math, parsing,
  or encoding.
* **Round-trip invariants**: encode then decode, serialize then deserialize, or convert then
  convert back.
* **Behavioral properties**: `score A > score B`, output is sorted, or result is within a range.
* **Error detection**: invalid input produces errors or warnings.
* **Boundary enforcement**: architectural rules like core code must not import PySide6.

```python
# Good: tests logic with fixed inputs
assert parse_title_year("The.Matrix.1999.BluRay.mkv") == ("The Matrix", "1999")

# Good: round-trip invariant
scene_x, scene_y = transform.pixel_to_scene(frame, px, py)
px_rt, py_rt = transform.scene_to_pixel(frame, scene_x, scene_y)
assert numpy.isclose(px_rt, px, atol=0.5)

# Good: behavioral property, not a hardcoded value
assert 0.0 <= score <= 1.0
assert score_exact_match > score_different_title
```

## Brittle tests

Avoid tests that assert on dates, collection sizes, lists of required keys, hardcoded defaults,
tunable constants, or dataclass storage. These break when unrelated code changes and provide no
real value. When in doubt, delete. A missing pytest is cheaper than a fragile one. This is the
design-first philosophy applied to tests: see [REPO_STYLE.md](REPO_STYLE.md#core-philosophies).

## Basic commands

Use this as the default test command:

```bash
pytest tests/
```

For targeted runs:

```bash
pytest tests/test_example.py
pytest tests/ -k name
pytest tests/ -x
```

`tests/conftest.py` handles the pytest environment setup. Do not duplicate that setup in the
pytest command.

## Failure triage

* If you are unsure whether a failing pytest result is pre-existing or introduced by your
  current work, assume it is new first.
* Reason: we try not to commit code with known failing tests, so a fresh failure is usually
  related to current uncommitted changes.
* If uncertainty remains, inspect `git diff` and check whether the suspicious lines are part
  of current uncommitted edits.
* Never use `git stash` as a diagnostic step for this.
