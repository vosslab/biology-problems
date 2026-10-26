# YAML ordering audit

Six fresh independent passes completed on 2026-10-26: Plan, Test, Style, Docs, Legacy,
and Comment. Reviewed the ordering scripts, helper, template, three banks, focused tests,
related documentation, and website aliases, tasks, output discovery, and metadata.
No Git or staging commands were used for review.

## Findings and disposition

- Medium, open: `docs/YAML_QUESTION_BANK_INDEX.md` omits the ordering banks despite the
  new include root in `tools/build_yaml_question_bank_index.py`. Its generator requires
  Git history, which the user excluded. Regenerate with the existing tool when Git use
  is authorized; do not invent dates or introduce another indexing mechanism.
- Low, fixed: `docs/BIOTECH_TOPIC04.md` used paths missing `problems/` and described
  obsolete variable-length 16S validation. Corrected the command and linked current
  all-six-step evidence.
- Low, fixed: the historical January changelog called a deleted Python filename a YAML
  bank. It now links the replacement bank while preserving the original filename.
- Low, fixed: removed the redundant external-standard validation comment in orderinglib.

## Reviewer disagreement and limits

Legacy rated old generated website banks high severity; Docs treated them as deferred
publication. The coordinator retains this as a rollout limitation: the implementation
plan explicitly excluded website publication, and source registration is migrated.
Existing site_docs artifacts still represent the old generators. The established website
generation workflow must refresh them before claiming end-to-end rollout. No generated
site files were hand-edited and no live-site state was verified.

Plan flagged the root-level implementation-plan location. It remains in place because
REPO_STYLE explicitly preserves existing root-level plans absent an approved relocation
sweep. New audit evidence is filed here in the prescribed audits subdirectory.

Test and Style returned no findings. Both permanent ordering tests were judged worthwhile
under PYTEST_STYLE: they protect numeric rank/wording/replacement behavior and independently
reconstruct the MC answer from displayed labels. No new permanent test was proposed.

## Evidence

- Coordinator reran ordering, YAML-parse, and bptools checks: 180 passed.
- Coordinator reran website alias checks: 9 passed.
- Style independently ran ordering tests and pyflakes checks: 413 passed.
- Test independently ran the two ordering tests: 2 passed.
- Prior six-format browser/QTI artifacts still exist in `/private/tmp/ordering_review`;
  browser and QTI export were not repeated during this audit. No LMS import was verified.
- The prior full-suite result remains 5705 passes and five failures documented in the
  implementation plan; the full suite was not rerun for documentation/comment-only fixes.
