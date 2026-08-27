# devel scripts

`devel/` holds maintainer-only tools for developing, validating, and releasing
this repository. These files are not product code and are not part of the fast
pytest lane.

Use this folder for scripts that help maintainers do repo-level work:

- Version and release preparation.
- Changelog querying, commit-message drafting, and changelog rotation.
- Documentation repair and repo hygiene cleanup.
- Build-output cleanup that is useful across repo types.
- Developer helpers shared across repos through propagation.

Do not put reusable library code, runtime application code, or permanent tests
here. Shared test helpers belong in `tests/`; runtime files belong in the
appropriate repo root or package.

## Current root scripts

| File | Kind of work |
| --- | --- |
| [bump_version.py](bump_version.py) | Preview and save repo version changes; enter `patch` for the next patch release. |
| [version_lib.py](version_lib.py) | Shared version parsing and normalization behavior. |
| [version_files.py](version_files.py) | Discover and update files that carry version metadata. |
| [changelog_lib.py](changelog_lib.py) | Shared parser and helpers for changelog tools. |
| [commit_changelog.py](commit_changelog.py) | Draft a commit message from new changelog entries. |
| [query_changelog.py](query_changelog.py) | Search active and archived changelog entries. |
| [rotate_changelog.py](rotate_changelog.py) | Move old changelog day blocks into archive files. |
| [flatten_broken_md_links.py](flatten_broken_md_links.py) | Repair or flatten broken Markdown links. |
| [dist_clean.sh](dist_clean.sh) | Remove build artifacts, caches, and dependency installs. |

## Propagated devel scripts

Some developer tools arrive by propagation and appear in `devel/` when this repo's
`REPO_TYPE` calls for them.

`devel/make_release.py` ships to the `scripted`, `compiled`, and `other` families, including
their descendants (`python`, `pypi`, `rust`, and `swift`). It prepares a GitHub source release:
CalVer freshness check, free-tag check, committed `LICENSE.<SPDX>` verification,
zip and tgz archive build with byte-level checks of every license, LLM-prompt generation for
the release description, optional `docs/RELEASE_HISTORY.md` and `docs/NEWS.md` updates,
and printed `git tag` + `gh release create` commands. Use `--dry-run` to preview or
`--write` to update doc files. See [docs/REPO_STYLE.md](../docs/REPO_STYLE.md) versioning
section for the full flow.

Other propagated devel tools are type-specific, so a repo receives only the ones
matching its `REPO_TYPE`. Examples include Python release publishing helpers and
TypeScript setup/rendering helpers.

## Running scripts

For Python scripts, use the repo bootstrap environment:

```bash
source source_me.sh && python3 devel/<script>.py
```

Run individual scripts with `--help` for current options. Keep command details
in script help output instead of duplicating them here.
