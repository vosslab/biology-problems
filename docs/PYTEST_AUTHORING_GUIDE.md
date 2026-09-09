# Pytest authoring guide

> This file is vendored. Local changes can and will be overwritten by propagation.

Use this guide after the [PYTEST_STYLE.md](PYTEST_STYLE.md#is-this-a-good-pytest) checklist.
`PYTEST_STYLE.md` decides which behavior earns a permanent pytest and defines pytest policy. This
guide shows how to construct that pytest with this repository family's shared conventions.

## Use repo conventions

Name a fast test `test_<topic>.py`, name its test functions `test_*`, use tabs and complete type
annotations, and organize imports as standard library, PIP, then local modules.

## Use the hygiene harness

Use [tests/file_utils.py](../tests/file_utils.py) for a repository-wide hygiene test. It provides
discovery, report naming, report lifecycle, parametrize IDs, and failure formatting.

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
	assert rel not in VIOLATIONS_BY_FILE, file_utils.format_violation_assert_message(
		rel, VIOLATIONS_BY_FILE.get(rel, []), REPORT_NAME
	)
```

`FILES` holds sorted absolute paths; the checker receives a repository-relative POSIX path. Use
`collect_python_violations` for AST checks and `collect_file_violations` for content checks. Give
each hygiene test its matching `test_key`.

## Produce reports

`file_utils.report_name(__file__)` derives `report_<test-stem>.txt`. The autouse fixture clears
stale reports, writes a complete report for every discovered violation, and leaves clean runs free
of report output.

## Verify a test

Run the focused test, then the complete fast lane:

```bash
source source_me.sh && python3 -m pytest tests/test_<topic>.py -q
source source_me.sh && python3 -m pytest tests/ -q
```

## Record durable changes

Update [CHANGELOG.md](CHANGELOG.md) for template changes. Record human preferences in
[HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md) and settled repository policies in
[DESIGN_DECISIONS.md](DESIGN_DECISIONS.md).
