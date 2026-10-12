# Pytest authoring guide

> This file is vendored. Local changes can and will be overwritten by propagation.

Use this guide after deciding that behavior earns a permanent test under
[PYTEST_STYLE.md](PYTEST_STYLE.md). Prefer fewer, stronger permanent tests, and protect behavior
worth preserving rather than incidental implementation. When in doubt, remove the test.

Temporary tests and one-time checks belong in the ignored `tests/_temp/` subtree. Pytest-suitable
`test_*.py` files participate in `pytest tests/` while work is active. Run heavier temporary checks
explicitly with their appropriate tool. Before completing the plan, promote the tests that deserve
permanent protection and remove the rest.

## Authoring checklist

- [ ] The behavior passed the permanent test checklist in [PYTEST_STYLE.md](PYTEST_STYLE.md).
- [ ] The file is `tests/test_<topic>.py` and its test functions are named `test_*`.
- [ ] The test uses plain `assert`, tabs, complete annotations, and repository import order.
- [ ] Inputs and outcomes are fixed, deterministic, and offline.
- [ ] The test finishes well under one second with a few focused assertions.
- [ ] Setup and inputs are inline and close to the assertion.
- [ ] Test-owned files use `tmp_path`.
- [ ] Assertions express public behavior, invariants, errors, or boundaries.

## Keep test structure direct

- Prefer pytest once a repository has more than a few simple assertions.
- Keep every `assert` under `tests/`; plain scripts and library modules do not use `assert`.
- Put pytest configuration, collection hooks, import paths, and shared environment setup in
  `tests/conftest.py`.
- Keep the test body free of complex logic. Move reusable mechanics into a small helper with its
  own clear contract, and test that helper.
- Use one or two focused assertions for a simple behavior. Five assertions for a simple function
  usually indicate that the test covers too much.
- Test code that will remain in the repository. Use `tests/_temp/` for scratch code, reproductions,
  and implementation proof, then promote or remove each check before completion.

## Reject brittle tests

Before retaining a permanent test, check that it:

- tests logic that could plausibly regress, rather than a trivial standard-library wrapper;
- remains valid next week without source changes and does not depend on today's date or time;
- asserts meaningful behavior rather than collection length, required-key or callable-name lists,
  tunable defaults, magic numbers, or immediate dataclass field assignment;
- runs offline without real network calls or subprocess CLI round trips;
- uses deterministic timing and fixed seeds, without sleeps or unseeded randomness;
- writes only inside `tmp_path` and finishes well under one second; and
- moves service, browser, model-loading, large-tree, or whole-system behavior to `tests/e2e/` or
  `tests/playwright/`.

A missing pytest is cheaper than a fragile one. Prefer removing a slow or brittle test over
rewriting it unless the behavior clearly earns permanent protection.

## Use fixtures deliberately

Inline setup is the default. Add a fixture only when the product contract actually depends on the
shared setup, file shape, or loader behavior; test-author convenience is insufficient. Use durable
shared fixtures for these established needs:

1. Use pytest's `tmp_path` fixture for temporary files and directories.
2. Use the `collect_report` autouse harness for repository hygiene reports.
3. Use an existing repository file when that shipped file's required shape or loader behavior is
   the contract under test.

A committed `tests/fixtures/` directory is shared infrastructure. Add one with explicit human
approval when durable shared data is clearer than inline setup.

An external test-data file is another dependency that can move, be renamed, or disappear. Loading
one at module import time can prevent the entire test module from collecting. Embed small inputs in
the test and write file-shaped inputs into `tmp_path` during the run. Put a genuinely large
round-trip check in `tests/e2e/`.

## Use the hygiene harness

Use [tests/file_utils.py](../tests/file_utils.py) for a repository-wide hygiene test. It owns file
discovery, scratch exclusions, report naming, report lifecycle, parametrization IDs, and failure
formatting. Its docstrings are the API reference.

```python
REPORT_NAME = file_utils.report_name(__file__)
FILES = file_utils.discover_files(
	extensions=(".sh",),
	test_key="topic_name",
)
VIOLATIONS_BY_FILE: dict[str, list[str]] = {}

@pytest.fixture(scope="module", autouse=True)
def collect_report() -> None:
	file_utils.clear_stale_reports()
	VIOLATIONS_BY_FILE.clear()
	VIOLATIONS_BY_FILE.update(file_utils.collect_file_violations(FILES, check_file))
	lines = file_utils.format_violation_report("Topic violations:", VIOLATIONS_BY_FILE)
	if lines:
		file_utils.write_report_lines(REPORT_NAME, lines)

@pytest.mark.parametrize("path", FILES, ids=file_utils.rel_id)
def test_topic(path: str) -> None:
	rel = file_utils.rel_to_root(path)
	message = file_utils.format_violation_assert_message(
		rel, VIOLATIONS_BY_FILE.get(rel, []), REPORT_NAME
	)
	assert rel not in VIOLATIONS_BY_FILE, message
```

Use `collect_python_violations` when the checker consumes a parsed Python AST and
`collect_file_violations` when it consumes file content. Give each hygiene test the `test_key`
matching its filename stem without `test_`.

The module-scoped fixture scans the full file set before parametrized assertions run. It writes one
complete `report_<topic>.txt` only when violations exist; a clean run removes stale reports.

## Configure hygiene discovery

- Keep universal file discovery and scratch exclusions in `tests/file_utils.py`.
- Put repository-specific exclusions in `tests/conftest.py` under `REPO_HYGIENE_FILTERS`.
- Use `extra_filter` only to select a universal subset for one test.
- Use `tests/source_file_line_limit_overrides.txt` only for individually approved external sources.
- Name the module-level discovered path list `FILES` and use `file_utils.rel_id` for readable cases.

`file_utils.discover_files` returns sorted absolute paths. Checkers and repository filters receive
repository-relative POSIX paths. Pass `repo_root=` only when a `file_utils` regression test uses a
controlled temporary repository.

Its signature is:

```python
discover_files(extensions=None, extra_filter=None, *, test_key=None, repo_root=None) -> list[str]
```

Pass lowercase suffixes such as `(".py",)`; matching is case-insensitive. `extensions=None` keeps
all extensions. `extra_filter` receives a repository-relative POSIX path and returns `True` to keep
it. Keep the module-level result in `FILES`.

Discovery applies three exclusion layers in order:

1. `tests/file_utils.py` applies universal directory, `_temp*`, and `dist_*` exclusions through
   `path_has_skip_dir`.
2. `tests/conftest.py` applies repository-owned `REPO_HYGIENE_FILTERS` entries keyed by `"all"` or
   the test filename stem without `test_`. Patterns are repository-relative POSIX globs; recursive
   directory exclusions need a trailing `/**`.
3. The vendored test's `extra_filter` selects a universal subset for that test. It does not hold
   repository-specific exclusions.

The source-file line-limit gate has one narrow approval mechanism:
`tests/source_file_line_limit_overrides.txt` lists exact repository-relative paths for individually
approved external sources. Other hygiene exclusions remain in `REPO_HYGIENE_FILTERS`.

## Use file utilities

Use the shared helpers instead of duplicating their behavior:

- `iter_imports(tree)` yields import nodes for import-policy tests.
- `rel_to_root(path, repo_root=None)` returns a repository-relative POSIX path.
- `rel_id(path)` wraps `rel_to_root` for readable parametrization IDs.
- `run_fixer_script(script_name, target)` runs a fixer and returns its exit code and standard error;
  it raises `RuntimeError` only for missing environment prerequisites.
- `collect_file_violations(files, check)` collects violations when the checker owns parsing.
- `collect_python_violations(files, check)` parses each Python file once and records syntax errors.
- `format_violation_report(header, violations_by_file)` creates complete report lines.
- `format_violation_assert_message(rel, lines, report_name)` creates the per-file failure message.
- `write_report_lines(report_name, lines)` writes a nonempty complete report.
- `clear_stale_reports()` removes old root-level `report_*.txt` files once per process.
- `report_name(test_file)` derives the canonical report name from `__file__`.

The ASCII fixer returns 0 for clean, 1 when issues remain, and 2 after fixing. The whitespace fixer
returns 0 for clean or fixed and 1 for a missing input.

## Preserve report lifecycle

Every hygiene test writes one root-level `report_<topic>.txt` only when violations exist. Call
`clear_stale_reports()` first in `collect_report`; do not call `write_report_lines` with an empty
list as a cleanup mechanism. Use plain `assert` for violations and `RuntimeError` for missing tools
or invalid environment prerequisites.

The module-scoped fixture always scans the complete file set. A `-k` expression filters assertion
cases only; it must not make the report partial or misleading.

Two permanent guard tests protect this scaffold:

- `tests/test_function_typing.py` enforces annotations and the repository's builtin-generics and
  PEP 604 union conventions.
- `tests/test_pytest_hygiene.py` keeps discovery and shared scratch filtering in `file_utils.py`.

## Verify a test

Run the focused test, then the complete fast lane:

```bash
source source_me.sh && python3 -m pytest tests/test_<topic>.py -q
source source_me.sh && python3 -m pytest tests/ -k <name>
source source_me.sh && python3 -m pytest tests/ -x
source source_me.sh && python3 -m pytest tests/ -q
```

`tests/conftest.py` supplies the pytest environment. Do not duplicate that setup in commands or
individual test modules.

Treat a fresh failure as related to the current work until the diff and failing behavior show
otherwise. Preserve the working tree while investigating.

## Record durable changes

Update the repository changelog for durable changes. Record human preferences in
[HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md) and settled repository policies in
[DESIGN_DECISIONS.md](DESIGN_DECISIONS.md).
