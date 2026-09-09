# tools scripts

> This file is vendored. Local changes can and will be overwritten by propagation.

`tools/` holds optional standalone utilities for people working with the application's domain.
A user supplies domain input and receives a useful domain result. The canonical placement policy
is [docs/REPO_STYLE.md](../docs/REPO_STYLE.md#scripts-and-executables).

## Utility shape

A tool may be one self-contained script or one self-contained directory. A substantial utility can
keep its own helpers inside its directory and use standard-library modules and installed
dependencies declared by the repository. Keep the complete utility runnable independently of the
repository's local packages.

Typical tools convert, validate, inspect, or transform user-supplied data and produce a report,
document, image, or other useful artifact.

## Placement classifier

- Use `tools/` for an optional standalone user utility whose domain input produces a domain result.
- Use [devel/DEVEL_README.md](../devel/DEVEL_README.md) for maintainer and
  repository-engineering commands.
- Use the application CLI or package for primary workflows and reusable application behavior.
- Use an optional local `launchers/` directory for thin compatibility or convenience delegates
  into the application.

For example, HTML-to-PDF conversion and playlist validation are tools. A repository map,
dependency refresh, source generation, screenshot evidence, benchmark, or release command is
maintainer work.

## Import boundary

Use `tools/`, `devel/`, `tests/`, and `launchers/` as support locations rather than
repository-level import packages. A standalone tool remains independent of repository-local
packages. It may use its own nested helpers, standard-library modules, and declared installed
dependencies. Repository-local package imports belong in the application or an application-facing
launcher. The support-directory gate preserves this boundary, `devel/` flat sibling helpers, and
test-local helpers.

## Running scripts

For Python scripts, use the repo bootstrap environment:

```bash
source source_me.sh && python3 tools/<script>.py
```

Run individual scripts with `--help` for current options. Keep command details
in script help output instead of duplicating them here.
