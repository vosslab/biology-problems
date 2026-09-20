# E2E_TESTS.md

> This file is vendored. Local changes can and will be overwritten by propagation.

End-to-end testing conventions for this repository family.

`tests/e2e/` and `tests/playwright/` contain permanent E2E tests. Prefer fewer, stronger E2E tests
that protect whole-system behavior worth preserving. Promote end-to-end verification to permanent
coverage when the whole-system behavior deserves lasting protection. Use `tests/_temp/` for
one-time whole-system checks, run them explicitly, then promote or remove them before plan
completion. When in doubt, remove the test. See [PYTEST_STYLE.md](PYTEST_STYLE.md) for the permanent
test policy.

## Two E2E homes

- `tests/e2e/` contains permanent non-browser whole-system tests: CLI workflows, builds, services,
  and multi-suite orchestration.
- `tests/playwright/` contains permanent browser-driven tests. Website and TypeScript repositories
  also receive `PLAYWRIGHT_TEST_STYLE.md` and `PLAYWRIGHT_USAGE.md`.

Both permanent E2E subtrees run outside pytest. `tests/conftest.py` excludes only `e2e` and
`playwright`. Pytest-suitable `test_*.py` files in `tests/_temp/` remain available to normal pytest
collection; heavier temporary checks run explicitly.

## Permanent E2E checklist

Use a permanent E2E test for intentionally stable, important whole-system behavior that is
plausibly subject to regression and best protected at the whole-system boundary.

- [ ] The workflow is intentionally stable and worth preserving.
- [ ] A whole-system run is necessary to test the contract.
- [ ] Smaller tests leave meaningful whole-system behavior unprotected.
- [ ] The assertions focus on meaningful outputs, boundaries, or user actions.
- [ ] The runner produces diagnostics that support a concrete response.
- [ ] A new blocking gate includes its failure plan.

Good candidates include:

- A complete CLI workflow with meaningful output and exit behavior.
- A round trip across several real components.
- An integration with an external tool where substitution would miss the contract.
- A deliberate browser journey or accessibility boundary.

Keep pure function and narrow integration behavior in the fast pytest or Node lane. Use temporary
verification when the check only proves the current implementation or rollout.

## Non-browser layout

- Name shell runners `tests/e2e/e2e_<name>.sh`.
- Name Python runners `tests/e2e/e2e_<name>.py`.
- Make each runner self-contained with clear pass, failure, and diagnostic output.
- Add `tests/e2e/run_all.sh` when a repository has several permanent runners worth executing
  together.

TypeScript repositories enforce these names through `tests/test_test_naming_conventions.py`.

## Run non-browser E2E

```bash
bash tests/e2e/e2e_<name>.sh
source source_me.sh && python3 tests/e2e/e2e_<name>.py
bash tests/e2e/run_all.sh
```

Use the repository's Playwright runner for browser tests. Run temporary non-pytest checks from
`tests/_temp/` explicitly with their native tool.

## Design failures

Assert externally meaningful results and make diagnostics identify the failed workflow. When a new
E2E check becomes a blocking CI, build, release, or repository-wide gate, define what failure means
and the decision, correction, or recovery that follows.

## Related docs

- [PYTEST_STYLE.md](PYTEST_STYLE.md) decides which behavior earns permanent protection.
- [PYTEST_AUTHORING_GUIDE.md](PYTEST_AUTHORING_GUIDE.md) explains permanent pytest construction.
- [PYTHON_STYLE.md](PYTHON_STYLE.md) defines Python and `assert` conventions.
