# Claude hook usage guide

_Last updated: 2026-05-29 02:20 UTC. Source of truth: `claude-code-permissions-hook`
repo. Mirrors in sibling repos (e.g. `starter-repo-template`) are copies; do not
edit mirrors directly._

Timestamp format: `YYYY-MM-DD HH:MM UTC` (ISO 8601 date + 24-hour clock, UTC).
Regenerate on every audit; derive from the latest `## YYYY-MM-DD` heading in
`docs/CHANGELOG.md` plus current commit time.

Best practices for AI agents in repos using the `claude-code-permissions-hook`:
what is allowed, denied, and passed through, with preferred alternatives for denied
patterns. Claude-specific (not Codex). Repo style conventions live in
[docs/REPO_STYLE.md](REPO_STYLE.md) and [docs/PYTHON_STYLE.md](PYTHON_STYLE.md).

## Trust model

The hook optimizes for high task completion with bounded blast radius: allow routine local work, deny/steer on machine-changing actions, prompt on high-impact operations.

## Overview

The permissions hook intercepts every Claude Code tool call and evaluates it against TOML config rules. Each call gets one of three outcomes:

| Outcome | Meaning |
| --- | --- |
| **Allow** | Tool call proceeds automatically |
| **Deny** | Tool call is blocked with an error message |
| **Passthrough** | Falls back to Claude Code's default permission flow (user prompt) |

### Command decomposition

The hook decomposes compound commands (`&&`, `||`, `;`, pipes) into leaf sub-commands:

- **Deny** if ANY leaf matches a deny rule
- **Allow** if ALL leaves match allow rules
- **Passthrough** if any leaf has no matching rule (and none denied)

A compound command fails as a whole even if only one leaf is illegal. If `find ... ; ls ...` is denied, the `ls ...` half would have run on its own -- drop the denied leaf and re-run rather than rewriting both.

Unwraps `bash -c "..."` and extracts `$(...)`. Strips environment-variable prefixes (`NODE_PATH=/foo node script.js` -> `node script.js`).

### Max chain length

Commands with more than **5** chained sub-commands are denied automatically.

### Bash-side reference for redirected commands

`Read`, `Edit`, and `Write` are first-class Claude Code tool calls. The Grep/Glob tools are not exposed in this agent context, so Bash `grep`/`rg` is the primary file-search path. `grep`/`rg` against a file path is **allowed in safe zones** (CWD-relative, workspace, `/tmp`, narrow `~/.claude` subtrees) and denied only when the path escapes them (out-of-zone absolute, bare `~`, `..`). `find` is likewise allowed read-only in those safe zones. The columns below show denied Bash forms, preferred recovery paths, and Bash forms that remain allowed.

| Denied Bash form | Preferred recovery | Allowed Bash forms |
| --- | --- | --- |
| `cat /path/to/file`, `head -20 /path`, `tail -20 /path` | Read tool with `file_path`, `offset`, `limit` | `... \| cat`, `... \| head -5`, `... \| tail -5` (pipeline, no file arg) |
| `grep root /etc/passwd`, `rg pat /usr/...` (out-of-zone), `/usr/bin/grep ...` (abs binary), `egrep`/`fgrep` | read a known file with the Read tool, or narrow to a relative/workspace path | `grep -n pat src/file`, `rg pat docs/`, `grep foo /tmp/x`, `grep -n foo ~/<workspace>/repo/x`, `... \| grep pat` |
| `find /etc -name '*.conf'`, `find . -delete`, `find /Users` (unsafe shapes) | Use bounded read-only `find` in a safe path zone (`.`, `/tmp`, `~/<workspace>/...`, `/Users/<me>/<workspace>/...`). For repo content, `git ls-files <pathspec>` is still preferred. | `find . -name '*.py'`, `find /tmp -type f`, `find ~/<workspace>/repo -type f` |
| `sed -n '10,20p' file.txt` | Read tool with `offset=10`, `limit=11` | `... \| sed -n '10,20p'` (pipeline) |

The deny rules cover all binary variants (alternate names, absolute paths like
`/usr/bin/grep` or `/opt/homebrew/.../grep`, `rg`). The fastest path through a
deny is the preferred recovery in column two; column three covers cases where
Bash is still the right shape.

## Allowed commands

### Python

```bash
source source_me.sh && python3 script.py
python3 -m pytest tests/test_foo.py
pytest tests/test_foo.py -k test_name
pyflakes script.py
```

Always use `source source_me.sh && python3` for running Python. Direct `python3`
invocations also work. Command substitution (`` ` `` or `$(...)`) is blocked in
Python commands.

### Git

Allowed git subcommands:

`add`, `branch`, `check-ignore`, `checkout`, `diff`, `ls-files`, `ls-tree`,
`log`, `mv`, `pull`, `remote`, `restore`, `rev-parse`, `show`, `status`, `worktree`

The `-C <path>` flag is supported before the subcommand.

```bash
git status
git diff --staged
git log --oneline -10
git -C /path/to/repo status
git mv old_name.py new_name.py
```

### Cargo

All cargo subcommands are allowed except: `publish`, `yank`, `login`, `logout`,
`owner`, `install`. Command substitution is blocked.

```bash
cargo build
cargo test
cargo clippy -- -D warnings
cargo fmt --check
```

### Shell scripts

```bash
bash script.sh
./script.sh
./script.py
./subdir/script.py
tools/runner.py          # bare relative-path scripts
scripts/build.sh
```

`bash -n script.sh` (syntax check) is denied -- inspect the script with the
Read tool instead. See the denied commands section.

### Safe utilities

These commands are allowed as single commands. Command substitution is blocked.

**File and text processing:**
`cat`, `colordiff`, `comm`, `cut`, `diff`, `expand`, `file`, `fmt`, `fold`,
`grep`, `head`, `jq`, `mediainfo`, `nl`, `od`, `paste`, `pdftotext`, `rg`, `sed`,
`seq`, `shuf`, `sort`, `tac`, `tail`, `tee`, `tr`, `unexpand`, `uniq`, `wc`, `xargs`

**Filesystem navigation:**
`basename`, `cd`, `chmod`, `cp`, `dirname`, `du`, `df`, `ls`, `lsof`, `mkdir`,
`mktemp`, `open`, `readlink`, `realpath`, `stat`, `tar`, `touch`, `tree`, `type`,
`unzip`, `which`

**Process and system info:**
`curl`, `date`, `echo`, `env`, `export`, `expr`, `false`, `id`, `ln`, `md5`,
`nproc`, `numfmt`, `pgrep`, `pkill`, `printenv`, `printf`, `ps`, `pwd`,
`screencapture`, `sleep`, `source`, `test`, `timeout`, `true`, `tty`, `uname`,
`unlink`, `wc`, `whoami`, `xcrun`, `xxd`

Note: Some of these (like `cat`, `grep`, `head`, `tail`) have deny rules that block
them when used with file path arguments. See the denied commands section. Use the
Read tool for file inspection, and `git ls-files <pathspec>` plus targeted Read for
file search; piped `grep`/`rg` on already-bounded stdout stays allowed. `awk` is not
in this list at all -- it is denied entirely (see the `awk` denied section below).

### Local runtimes

**Node.js:**
Use `node <script>` or `node --test <test-file>` for local project files; write `_temp.mjs` and run `node _temp.mjs` instead of `node -e "..."`. Auto-allowed shape: `node <flags> <path>.{js,mjs,cjs,ts,tsx} [script args...]`. Whitelisted flags: `--test`, `--watch`, `--check`, `-c`, `--loader=<arg>` / `--loader <arg>`, `--import=<arg>` / `--import <arg>`, any short `-<letters>`. Bare diagnostic forms `--test`, `--version`, `--help` are allowed. Inline JS (`-e` / `--eval`) is **denied** (see the `node -e` section under denied commands). Unrecognized `--long-flags` passthrough. Command substitution is blocked.

```bash
node script.js                              # allowed
node --test tests/test_foo.mjs              # allowed
node --loader=tsx tests/walker.mjs          # allowed
node --loader tsx/esm --test tests/x.ts    # allowed
node --watch script.mjs                     # allowed
node -c script.js                           # allowed
node --test                                 # allowed (default test glob)
node --version                              # allowed
node -e "require('./data.json')"            # denied (inline JS)
node --eval "console.log(1)"                # denied (inline JS)
node --inspect tests/x.mjs                  # passthrough (unknown long-flag)
node --experimental-vm-modules tests/x.mjs  # passthrough
```

**npx (whitelisted packages):**
Allowed for: `tsc`, `tsx`, `eslint`, `prettier`, `playwright`, `esbuild`. Unknown packages require user approval.

```bash
npx tsc --noEmit              # allowed
npx tsx --test tests/x.ts     # allowed (TypeScript file runner)
npx eslint src/               # allowed
npx prettier --check .        # allowed
npx playwright screenshot ... # allowed
npx esbuild src/x.ts          # allowed
npx some-package              # requires approval
```

If `npx tsc` fails because TypeScript is not installed, run `npm install --save-dev typescript` (whitelisted). Do not work around failure by calling `./node_modules/.bin/tsc` directly (denied).

**eslint and prettier (direct):**
`eslint` and `prettier` are allowed as direct commands for linting and formatting.

```bash
eslint src/app.ts
prettier --write src/
```

**Deno:**
`deno` is allowed for `run`, `check`, `fmt`, `lint`, and `test` subcommands,
plus `--version` queries. Remote URLs and `deno eval` are not auto-allowed.

```bash
deno run script.ts
deno check script.ts
deno fmt --check
deno lint
deno test
deno --version
```

### Podman (containers)

Read-only inspection, build, compose, lifecycle, and exec are allowed:

```bash
podman ps
podman pod ls
podman images
podman logs web
podman inspect web
podman info
podman build -t foo .
podman compose up -d
podman compose down
podman start web
podman stop web
podman restart web
podman exec web ls /var/www
podman exec web cat /etc/hostname
```

Destructive operations are denied: `podman rm -f`, `podman rmi -f`,
`podman kill`, `podman stop -t 0`, `podman system prune`,
`podman volume rm|prune`, `podman network rm|prune`, `podman image rm|prune`.
Ask the user to run these manually if truly needed.

Note: arguments to `podman exec` are not re-decomposed by the hook, so a
destructive shell inside a container (`podman exec web rm -rf /tmp/x`) is not
blocked. Destructive behavior inside a container is a container-level concern.

### Tools scoped to /tmp scratch dirs

These tools are auto-allowed when every path argument lives under `/tmp/` or `/private/tmp/`, but denied for paths outside scratch directories (`/Users`, `/etc`, `/usr`, `/opt`, `/var`, `/Library`, `/System`, etc.):

`ffmpeg`, `sox`, `convert`, `magick`, `mogrify`, `gm`, `optipng`, `pngcrush`, `jpegoptim`, `cwebp`, `tesseract`, `qpdf`, `pdftk`, `gs`, `lame`, `flac`

```bash
ffmpeg -i /tmp/in.wav /tmp/out.m4a              # allowed
sox /tmp/clip.wav -n trim 0 20 stat             # allowed
convert /tmp/in.png /tmp/out.jpg                # allowed
ffmpeg -i /tmp/in.wav /Users/me/out.wav         # passthrough (out of tmp)
convert in.png out.png                          # passthrough (no tmp path)
```

### File deletion (safe patterns)

The `rm` command is denied by default, but these specific patterns are allowed:

| Pattern | Example |
| --- | --- |
| Underscore-prefixed files | `rm _temp.py`, `rm -f /path/to/_scratch.sh` |
| `/tmp/` paths | `rm /tmp/test_output.json` |
| Cache directories | `rm -rf __pycache__`, `rm -r ~/Library/Caches/foo` |
| `git rm` with relative paths | `git rm old_file.py` |
| `rmdir` (empty-dir only) | `rmdir /tmp/empty`, `rmdir src/content/old/` |

`rmdir` (including `rmdir -p`) is allowed because it only removes empty directories and fails if non-empty. Use to clean up empty source directories after `git mv` chains.

### Package managers

**pip read-only:**
`pip show`, `pip list`, `pip freeze`, `pip check`

**npm read-only and run:**
`npm list`, `npm root`, `npm ls`, `npm show`, `npm view`, `npm info`, `npm search`,
`npm outdated`, `npm doctor`, `npm prefix`, `npm version`, `npm --version`

`npm run` is allowed for executing scripts defined in local `package.json`.

**brew read-only:**
`brew list`, `brew info`, `brew search`, `brew --prefix`

```bash
pip show numpy
npm list --depth=0
npm run build
brew info python
```

### File access zones

The hook may contain rules for Claude Code tools that are not exposed in
every agent context (`Grep` and `Glob` in particular -- see notes
below). This guide recommends only recovery paths observed to be
available in the target context.

| Tool | Allowed paths |
| --- | --- |
| Read | `~/nsh/`, `~/.<dotdirs>`, site-packages, `/tmp/`, `/var/folders/` |
| Write | `~/nsh/`, `~/.claude/`, `/tmp/` |
| Edit | `~/nsh/`, `~/.claude/`, `/tmp/` |
| Glob | Supported defensively when exposed by Claude Code; not a standard recovery path in this agent context |
| Grep | Supported defensively when exposed by Claude Code; not a standard recovery path in this agent context |

All file tools block path traversal (`..`). Reading `.env` and `.secret` files is denied.

### Web tools

`WebFetch` and `WebSearch` are allowed without restrictions.

### Agent types

Any agent with a valid name matching the pattern `^[a-zA-Z][a-zA-Z0-9_:-]*$` is
allowed. This includes built-in types (Explore, Plan, general-purpose) and custom
agents in `~/.claude/agents/`. Missing `subagent_type` falls through to user prompt.

### Orchestration tools

These tools are auto-allowed: `TaskOutput`, `TaskCreate`, `TaskList`, `TaskGet`,
`TaskUpdate`, `TaskStop`, `Skill`, `SendMessage`, `TeamCreate`, `TeamDelete`,
`NotebookEdit`.

Playwright MCP browser tools (`mcp__plugin_playwright_playwright__browser_*`)
are also allowed.

## Denied commands

### `rm` (file deletion)

**Instead:** Use underscore-prefixed filenames for scratch files (`_temp.py`),
write to `/tmp/`, or use `git rm` for tracked files.

**Why:** Prevents accidental deletion of important files.

**Blocked:** `rm file.txt`, `rm -rf dir/`.

### `git commit`, `git stash`, `git clean` (branch-aware)

**Instead:** Work on an `agent/<task>` branch where commits are allowed. To
prepare a merge into a protected branch, use `git merge --no-commit --no-ff
agent/<task>` and let the human review and commit. See
[Worktrees and protected branches](#worktrees-and-protected-branches) for the
full workflow.

**Why:** On protected branches (typically `main`, `master`), commits are made by
the human after reviewing the staged merge via `git diff`. On agent branches,
you have full commit access. `git stash` and `git clean` are destructive and
remove tracked or untracked work.

**Blocked on protected branches:** `git commit`, `git commit --amend` (all
variations including flag insertion like `git -C /tmp commit`). `git stash` and
`git clean` are denied everywhere.

### `cat`/`head`/`tail` with file paths

**Instead:** Invoke the Read tool directly with `file_path` and optional
`offset` and `limit`. The pipeline form (`... | head -5`, `... | tail -5`,
`... | cat`) stays allowed for slicing piped stdout, where Read does not
apply.

**Why:** Read is a Claude Code tool call (like Edit/Write). It provides line
numbers, offset, and limit, and is the canonical way to inspect a file from
this harness.

**Blocked:** `cat /path/to/file`, `head -20 /abs/path/file.txt`.

<a name="grep-recovery"></a>
### `grep`/`rg` with file paths

`grep` and `rg` against a file path are **allowed** when the path is in a safe zone, denied only when it escapes that zone. The Grep/Glob tools are not exposed in this agent context, so Bash `grep`/`rg` is the primary file-search path -- search files directly, no `git ls-files` dance required.

**Allowed** (path in a safe zone):

- CWD-relative paths: `grep -n foo src/main.rs`, `rg pattern docs/`
- workspace absolute: `grep -n foo ~/<workspace>/repo/x`, `rg pat /Users/<me>/<workspace>/repo/src`
- `/tmp`, `/private/tmp`: `grep foo /tmp/x.log`
- narrow `~/.claude/{agents,commands,skills,plugins,plans,projects}` subtrees

**Blocked** (escapes the safe zone -- can flood context with an unbounded scan):

- out-of-zone absolute: `grep root /etc/passwd`, `rg pattern /usr/lib/x`, arbitrary `/Users/<me>/<non-workspace>/...`
- bare `~` (whole home) and `..` traversal: `grep foo ../secrets`, `rg foo ~/Documents/x`
- absolute **binary** path regardless of target: `/usr/bin/grep ...`, `/opt/homebrew/bin/rg ...` -- use the bare PATH form (`grep`, `rg`)
- `egrep`/`fgrep` with any file path -- deprecated; use `grep -E` / `grep -F`
- `pcregrep`/`ack`/`ag` with a file path; `less <file>` (route to the Read tool)

To search an out-of-zone path: read a known file with the Read tool, or narrow to a relative/workspace path. Pipeline filters (`... | grep pat`, no file arg) stay allowed and are unaffected. For bulk content search a `git ls-files <pathspec> | xargs grep PAT` pipeline is still allowed end-to-end if you prefer it.

### `git grep`

**Blocked:** `git grep <pattern>`, including all git invocation forms (`/usr/bin/git grep`, `command git grep`, `env X=y git grep`, `git -c core.pager=cat grep`, `git -C <path> grep`, `git --git-dir=<dir> grep`, `git --work-tree=<dir> grep`). Recovery: see [grep/rg with file paths](#grep-recovery).

### `find`

Recovery: bounded read-only `find` in safe path zones (`.`, `/tmp`, `~/<workspace>/...`); or `git ls-files <pathspec>` inside a git repo.

Read-only forms in safe path zones are allowed. Destructive predicates, unsafe roots, and command substitution are denied.

**Instead:** Use bounded read-only `find` in a safe path zone:

- relative paths: `.`, `docs`, `src/sub`, `tests`
- `/tmp`, `/tmp/...`, `/private/tmp/...`
- workspace via tilde: `~/<workspace>/...` (e.g.
  `~/nsh/<repo>/...`); bare `~` is denied
- workspace via absolute path:
  `/Users/<me>/<workspace>/<repo>/...` or
  `$HOME/<workspace>/...`
- narrow Claude agent-config subtrees:
  `~/.claude/agents/...`, `~/.claude/commands/...`,
  `~/.claude/skills/...` (and absolute / `$HOME` equivalents).
  Bare `~/.claude` is denied; non-allowlist subpaths like
  `~/.claude/projects` passthrough.

Common read-only predicates ride along: `-name`, `-iname`,
`-type f|d|l`, `-path`, `-maxdepth`, `-mindepth`, `-not`, `!`,
`-o`, `-a`, grouping `(` `)`, `-print`, `-empty`. Output shaping
pipes (`| head`, `| sort`, `| grep`, `| rg`) stay allowed.
**Not in this pass:** `-size`, `-print0`, `-printf`, `-prune`,
`-newer`, `-mtime`, `-atime`, `-user`, `-group`, `-perm`, `-links`,
`-inum`, `-samefile`, `-fstype`, `-mount`, `-xdev`, `-regex`,
`-iregex` (add a focused rule + fixtures if needed).

Inside a git repo, prefer `git ls-files <pathspec>` when
tracked-file discovery is enough -- it excludes ignored and
build artifacts. Use `find` for `/tmp`, generated trees, untracked
files, and mixed/non-git subtrees.

**Why:** Read-only discovery in safe path zones is bounded by the
path zone, not by `-maxdepth`. Destructive predicates and destructive
`xargs` pipelines stay denied so mutation is a separate, reviewed
step.

**Blocked:**

- Bare `find` with no args -- it is an unbounded recursive listing.
- Destructive / output-file predicates (hard deny): `-delete`,
  `-exec`, `-execdir`, `-ok`, `-okdir`, `-fprint`, `-fprintf`,
  `-fls`.
- Advanced filters not yet supported in this pass (conservative
  deny -- ask for a focused rule + fixtures if needed): `-printf`,
  `-print0`, `-prune`, `-newer`, `-mtime`, `-atime`, `-user`,
  `-group`, `-perm`, `-size`, `-links`, `-inum`, `-samefile`,
  `-fstype`, `-mount`, `-xdev`, `-regex`, `-iregex`.
- Destructive xargs pipelines: `find ... | xargs rm`,
  `find ... | xargs -0 rm`, `xargs chmod`, `xargs chown`,
  `xargs mv`, `xargs sudo`.
- Bare `/`, system roots (`/etc`, `/usr`, `/opt`, `/System`,
  `/Library`, `/var`, `/bin`, `/sbin`, `/root`, `/sys`, `/proc`,
  `/dev`, `/boot`).
- Bare `/Users`, `/home`, or `/Users/<user>` without a workspace
  subpath. Use `~/<workspace>/...` or
  `/Users/<me>/<workspace>/...` instead.
- Broad user-config / cache trees: bare `~/.claude`, `~/.config`,
  `/var/folders`. The narrow Claude allowlist
  (`~/.claude/agents`, `~/.claude/commands`, `~/.claude/skills`)
  is allowed.
- Command substitution: `find . -name "$(...)"`,
  `VAR=$(find ...)`.
- Path traversal: `find ../`, `find docs/../`.

Residual passthrough: a non-standard home subdir like
`/Users/<me>/scratch_random_dir/...` is neither in the explicit
non-workspace denylist (`Downloads`, `Documents`, `Desktop`,
`Library`, `Movies`, `Music`, `Pictures`, `Public`, `Applications`)
nor in the safe-zone allow. It falls through to user approval.

Quoted path roots (`find "docs" -name '*.md'`, `find './src' -type f`)
are out of scope in this pass and passthrough. Drop the quotes
to auto-allow.

### `awk`

Recovery: `git ls-files <pathspec>` then Read tool on targets; piped `grep`/`rg` on bounded stdout for filtering; `_temp.py` for broad searches.

For line-matching, use `git ls-files <pathspec>` + Read or `_temp.py` helper. For field extraction use `cut`.

`awk`'s `/regex/` syntax makes file-vs-stdin guard impractical, so deny is unconditional.

**Blocked:** All `awk` invocations -- `awk '/pat/{print}' file`, `awk '{print $2}'`, `gawk`, `mawk`, absolute-path/`command`/`env` forms, pipeline leaves (`... | awk ...`). Unlike `cat`/`grep`/`sed`, there is no pipe exception: `awk` is denied even as a stdin filter.

### `sed -n` with file paths

Recovery: Read tool with `offset`/`limit` for file reads; piped `sed -n` remains allowed.

Use Read for file reads; `sed` is the right tool for slicing piped stdout.

**Allowed (pipe usage):** `git diff HEAD -- file.py | sed -n '250,400p'`

**Blocked:** `sed -n '10,20p' file.txt`.

### Claude Code tool names typed as Bash commands

**Instead:** Invoke the actual tool, not its name typed into Bash. `Read`
reads a file; `Edit`/`Write` modify files; `Task`/`WebFetch`/`WebSearch`
are first-class tool calls. For file search use `git ls-files <pathspec>`
plus the Read tool.

**Why:** `Grep`, `Read`, `Glob`, `Edit`, `Write`, `Task`, `WebFetch`, and
`WebSearch` are Claude Code TOOLS, not shell commands. Pasting the tool
name into Bash runs whatever (if anything) is on `PATH` by that name --
not the actual tool.

**Blocked:** `Grep -n "^## " docs/CHANGELOG.md`, `Read README.md`,
`Glob "**/*.py"`, `Edit file.py`, `Write /tmp/x.py`. Also caught when
chained or piped, since the decomposer splits leaves before matching:
`echo hi && Read README.md`, `cat /tmp/x | Grep foo`.

A grep pattern that *contains* a tool name does not hit *this* deny:
`grep "Grep\|Read" file` is not flagged as a tool-name-in-Bash command
(the deny anchors at start-of-leaf, so only the lowercase `grep` token
matters). Note it is still denied by the file-`grep` rule above if a
file path argument is present -- a file search is a file search
regardless of what the pattern spells.

### Pipe-only commands (allowed in pipes, denied as the lead command)

These have a "use dedicated tool" deny with file paths, but stay allowed as piped stdin:

| Command | Denied (lead) | Allowed (in pipe) |
| --- | --- | --- |
| `cat`, `head`, `tail` | `cat /tmp/x.txt` | `... \| head -5` |
| `egrep`, `fgrep` | `egrep pat /tmp/x.txt` (deprecated; use `grep -E`/`-F`) | `... \| grep pat` |
| `sed -n` | `sed -n '10,20p' /tmp/x.txt` | `... \| sed -n '10,20p'` |

(`grep`/`rg` are no longer in this table -- file-path forms are allowed in safe zones; see [grep/rg with file paths](#grep-recovery).)

### `tsc` via `node_modules` paths

Use `npx tsc` (whitelisted). If TypeScript is missing, run `npm install --save-dev typescript` (whitelisted). Direct `node_modules` paths are a workaround that masks missing installs. Do not work around the failure with absolute paths, `node node_modules/...`, or `source source_me.sh &&` chains.

**Blocked:** `./node_modules/.bin/tsc`, `./node_modules/typescript/bin/tsc`,
`/abs/path/node_modules/typescript/bin/tsc`, `node node_modules/typescript/bin/tsc`.

### `ffprobe` (steered to `mediainfo`)

Use `mediainfo --Output=JSON <file>` for cleaner output. `ffprobe` is allowed only for chapter/packet/frame/lavfi inspection:

```bash
ffprobe -show_chapters file.m4b   # allowed (chapter atoms)
ffprobe -show_packets file.m4b    # allowed (per-packet timing)
ffprobe -show_frames  file.mp4    # allowed (per-frame timing)
ffprobe -f lavfi -i sine=440      # allowed (synthetic/lavfi probe)
```

**Blocked:** `ffprobe file.m4b`, `ffprobe -show_streams file.mp3`, `ffprobe -i file.wav`.

### `perl` on `.pg`/`.pgml` files

Use the `/webwork-writer` skill lint guide instead. PGML is not standard Perl.

**Blocked:** `perl -c problem.pgml`, `perl problem.pg`.

### Heredocs (`<<EOF`)

Write code to `_temp.py` or `_temp.sh`, run with `source source_me.sh && python3 _temp.py` or `bash _temp.sh`. Heredocs are hard to read, lint, and test.

**Blocked:** `python3 - <<EOF`, `bash <<'SCRIPT'`.

### `for` and `while` loops

Write loop logic to `_temp.py` or `_temp.sh` files, not inline Bash.

**Blocked:** `for f in *.py; do ...`, `while read line; do ...`, pipeline forms like `ls *.md | while read f; do ...; done`, nested loops after `do `. The deny anchors the loop keyword at start-of-leaf, after a `|`, `;`, or `&` character, or after a `do ` (a loop nested inside a `do ... done` body).

### `bash -c` / `bash -lc`

Run commands directly. The Bash tool already runs bash; `bash -c` is redundant bash-in-bash.

**Blocked:** `bash -c "command"`, `bash -lc "source && python3 ..."`.

### `bash`/`sh`/`zsh -n` (syntax check)

Inspect scripts with the Read tool. Shell syntax check is an anti-pattern for script analysis.

**Blocked:** `bash -n script.sh`, `sh -n x.sh`, `zsh -n x.sh`, and absolute-path / `command`/`env` prefixes.

### `sudo`

Do not escalate to root. Ask the user if needed.

**Blocked:** `sudo command`.

### `git reset --hard`

**Instead (on protected branches):** Use safer alternatives like
`git checkout -- file` or `git restore file` to discard working changes.

**On agent branches:** `git reset --hard` is allowed for local cleanup and
rebasing your own work.

**Why:** On `main`/`master`, `git reset --hard` is a destructive history
rewrite that destroys uncommitted work and changes the branch tip.

**Blocked on protected branches:** `git reset --hard`. Allowed on
agent/feature branches.

### `git restore .` and `git checkout -- .` (wholesale discard)

**Instead:** Discard a single file at a time:

- `git restore path/to/file.py` (allowed)
- `git restore --staged path/to/file.py` (allowed)
- `git checkout -- one_file.py` (allowed)
- `git checkout HEAD~1 -- file.py` (allowed)

Branch switches (`git checkout main`, `git checkout -b feature/x`) remain
allowed unchanged. If you really want to wipe everything, ask the user to
run the command themselves.

**Why:** These forms have the same blast radius as `git reset --hard` --
they wipe every uncommitted change and unstage all renames in one shot.
That destroys agent work in progress (edits, renames, staged content) with
no recovery path other than `git reflog`.

**Blocked:** Any `git restore` or `git checkout` invocation whose pathspec is
`.` or `:/` (the "all tracked files" selector). Examples:

- `git restore .`
- `git restore :/`
- `git restore --staged --worktree .`
- `git restore --source=HEAD .`
- `git checkout .`
- `git checkout -- .`
- `git checkout HEAD -- .`
- `git checkout main -- .`
- `git checkout :/`

### `git push --force` (including --force-with-lease)

**Instead:** Ask the user to push manually if rebase is necessary.

**Why:** Destructive remote history change.

**Blocked:** `git push --force`, `git push origin main --force-with-lease`.

### `deno run` with URLs

Download with `curl` to a file, review it, then run locally. Remote code execution requires prior review.

**Blocked:** `deno run https://example.com/script.ts`.

### `curl`/`wget` piped to runtime

Download to a file first with `curl -o script.sh https://...`, review, then run. Never pipe remote code to shell/runtime.

**Blocked:** `curl https://example.com/install.sh | bash`, `wget -O - url | python3`.

### Write/Edit to system directories

Write to `~/nsh/` or `/tmp/` instead. System files should only be modified by root or package managers.

**Blocked:** Writing to `/etc/`, `/usr/`, `/opt/`, `/System/`, `/Library/`.

### `mv`

Use `git mv` for tracked files to preserve history. For untracked files, use `cp` + `rm`.

**Blocked:** `mv old.py new.py`.

### `VAR=$(...)` assignments

Command substitution in assignments creates hidden side effects. Use direct commands or `source source_me.sh` instead.

**Blocked:** `PROJECT=$(basename $PWD)`, `OUTPUT=$(python3 script.py)`.

### `$PYTHON` variable

Use the actual interpreter name for clarity.

**Blocked:** `$PYTHON script.py`, `${PYTHON} -m pytest`.

### `PYTHONDONTWRITEBYTECODE` / `PYTHONUNBUFFERED`

`source_me.sh` already exports these.

**Blocked:** Setting these environment variables manually.

### Bare variable assignments

The decomposer splits `A=x && cmd` into leaves; a bare assignment leaf is useless. Use space-separated env prefixes: `REPO_ROOT=/path python3 script.py`.

**Blocked:** `REPO_ROOT=/path/to/repo` (with no command following).

### `gh` CLI

`gh` is not installed. Ask the user to run GitHub operations manually.

**Blocked:** All `gh` commands.

### python `-c` (inline code)

Write `_temp.py` and run with `source source_me.sh && python3 _temp.py`. Inline code is hard to lint and debug.

**Blocked:** Every `python -c` form -- bare `python3 -c "print(1)"`, `python -c`,
version-suffixed `python3.12 -c`, absolute-path binaries
(`/opt/homebrew/bin/python3 -c`), `command`/`env` prefixes, and interpreter
flags before `-c` (`python3 -B -c`). `python3 script.py` and `python3 -m pytest`
are unaffected -- only the `-c` inline-code form is denied.

### `node -e` / `node --eval` (inline JS)

Write `_temp.mjs` and run with `node _temp.mjs`. Inline JS is hard to lint and debug, can hide command substitution (`node -e "$(curl ...)"`), and can spawn child processes (`require('child_process').execSync(...)`). Same rule shape as `python -c`.

**Blocked:** Every `node -e` / `node --eval` form -- bare `node -e console.log(1)`,
`node --eval "..."`, absolute-path binaries (`/usr/local/bin/node -e`),
`command`/`env` prefixes, and interpreter flags before `-e`/`--eval`
(`node -B -e "1+1"`). `node script.js`, `node --test`, and `node --version` are
unaffected -- only the `-e` / `--eval` inline-code forms are denied.

### `printf` with file redirect (Write-tool replacement)

Use the Write tool for new files or the Edit tool for appends. Using `printf` to assemble file content bypasses the Write/Edit tools that provide diffs, line counts, and proper change tracking.

**Blocked:** `printf '...' > FILE`, `printf '...' >> FILE`, `printf '...' | tee FILE`, `printf '...' | tee -a FILE`. Bare `printf '...'` for stdout formatting (no redirect, no `tee`) stays allowed.

## Path existence pre-check

Before evaluating allow or deny rules, the hook stats the target path of `Read`, `Edit`, `MultiEdit`, `Glob`, and `Grep` calls and denies if the path is missing or unusable, immediately catching the common "hallucinated path" failure mode.

### Per-tool semantics

| Tool | Requirement | Failure modes |
| --- | --- | --- |
| `Read` | `file_path` resolves to an existing, non-directory target | missing path; path is a directory; broken symlink |
| `Edit` / `MultiEdit` | `file_path` exists, OR its parent directory exists | both file and parent missing |
| `Glob` | resolved `path` is an existing directory | missing path; file passed where directory expected |
| `Grep` | resolved `path` (when provided) exists as file or directory | missing path |
| `Write` | exempt | n/a -- Write creates new files by design |

Symlinks-to-existing-files are accepted for `Read`. Broken symlinks deny
because `fs::metadata` follows the link and reports the missing target.
Relative paths are resolved against the hook input's `cwd`. When `Glob` or
`Grep` is called without a `path` field, the pre-check is skipped (the
cwd fallback is trusted).

### Reason strings the agent sees

| Condition | Reason |
| --- | --- |
| Read target missing | `Verify the file path before retrying. Read target does not exist: <path>.` |
| Read target is a directory | ``Read targets a file, not a directory. Use `ls <dir>` or `git ls-files <pathspec>` to list directory contents. Path is a directory: <path>.`` |
| Edit / MultiEdit both missing | `Create the parent directory first or choose an existing path. Edit target and parent directory are both missing: <path>; parent: <parent>.` |
| Glob path missing or not a directory | `Choose an existing search directory before retrying. Glob path does not exist as a directory: <path>.` |
| Grep path missing | `Choose an existing file or directory before retrying. Grep path does not exist: <path>.` |
| Stat failed for any reason other than NotFound (permissions, etc.) | `Verify the path before retrying. The hook could not confirm that this path exists: <path>.` |

The pre-check distinguishes `Ok(false)` (path confirmed missing) from
`Err(_)` (could not stat -- permission denied on a parent directory,
malformed path, etc.). Only confirmed-missing emits "does not exist";
errors emit "could not confirm" so the message stays accurate.

### What to do when you see one of these reasons

- Verify the path before retrying. The hook printed exactly which path it
  could not find and, for Edit, which parent directory was also missing.
- If the path was a typo, fix it. If the path belongs to a different
  working directory, set `cwd` correctly or use an absolute path.
- For Read of a directory, use `ls <dir>` or `git ls-files <pathspec>`
  to list contents. For Glob with a file argument, switch to Read for a
  single file or `git ls-files <pathspec>` to list candidates.
- For a brand-new file you intend to create, prefer `Write`; the pre-check
  is exempt for `Write`. `Edit` of a brand-new file is also accepted as long
  as the parent directory already exists.

## Worktrees and protected branches

Agents work on `agent/<task>` branches (often inside a worktree) and prepare
merges into protected branches (`main`, `master` by default) using:

```bash
git merge --no-commit --no-ff agent/<task>
```

This stages the merge result without creating the commit. The human reviews with `git diff HEAD` and runs the final `git commit` and `git push` themselves. Direct `git commit`, `git rebase`, `git reset --hard`, `git cherry-pick`, `git revert`, and pushes targeting protected refs are denied while on a protected branch; the same commands are allowed on feature/agent branches.

## Passthrough (requires user approval)

These commands intentionally require user approval (passthrough) because they have
significant side effects or security implications:

- **npx (non-whitelisted)**: May fetch remote packages from npm registry
- **npm install**: Modifies machine state, adds/updates dependencies
- **pip install**: Modifies machine state, adds/updates Python packages
- **git rebase**: Rewrites repository history
- **deno eval**: Executes arbitrary inline code

## Passthrough (interactive tools)

These tools intentionally passthrough to Claude Code's default permission flow
so the user sees interactive dialogs:

| Tool | Reason |
| --- | --- |
| `AskUserQuestion` | User must see and answer the question dialog |
| `EnterWorktree` | User must consent to worktree creation |
| `ExitWorktree` | User must consent to keep/remove decision |
| `CronCreate` | User should approve scheduled recurring jobs |
| `CronDelete` | User should approve canceling scheduled jobs |
| `CronList` | Kept consistent with other Cron tools |

Do NOT add these tools to any allow rule. Auto-approving them bypasses Claude Code's
interactive UI dialogs, causing blank answers or skipped consent screens.

## Best practices

- Always use `source source_me.sh && python3` for Python execution
- Use the Read tool for file inspection (offset / limit available)
- Search file contents with `grep`/`rg` directly on a relative or workspace path (`grep -rn pat src/`); the Grep tool is not available here
- Use `ls <dir>` or `git ls-files <pathspec>` to list files
- Write scratch code to `_temp.py` or `_temp.sh` (underscore prefix = safe to delete)
- Keep compound commands under 5 chained sub-commands
- Destructive `xargs` pipelines (`xargs rm`, `xargs chmod`, `xargs chown`, `xargs mv`, `xargs sudo`) stay denied
- Use relative paths for project files where possible
- Stage changes and update `docs/CHANGELOG.md`; let the user commit

## Common patterns

Use `Read`, `Edit`, `Write` as tool calls; search file contents with `grep`/`rg` directly on a relative or workspace path; list files with `ls` or `git ls-files`.

| Task | Wrong | Right |
| --- | --- | --- |
| Run Python | `python3 script.py` | `source source_me.sh && python3 script.py` |
| Read a file | `cat /path/to/file.py` | Read tool: `file_path="/path/to/file.py"` |
| Search files | `grep -r pat /etc` (out-of-zone); `Grep` tool (not available) | `grep -rn pat src/`, `rg pat docs/` (CWD-relative or workspace path, allowed directly) |
| Tool name as Bash | `Grep -n "^## " docs/CHANGELOG.md` | Bash `grep -n "^## " docs/CHANGELOG.md` (relative path, allowed) |
| Find files | `find / -name "*.py"` (system root); `find . -delete` (destructive) | Bounded read-only: `find <safe-root> -type f -name PAT` (relative paths, `/tmp`, `~/<workspace>/...`); or `git ls-files <pathspec>` for tracked-only repo content |
| Read lines 10-20 | `sed -n '10,20p' file.txt` | Read tool: `offset=10`, `limit=11` |
| Delete temp file | `rm temp.py` | Name it `_temp.py`, then `rm _temp.py` |
| Rename file | `mv old.py new.py` | `git mv old.py new.py` |
| Loop over files | `for f in *.py; do ...` | Write `_temp.sh` with the loop, run `bash _temp.sh` |
| Inline Python | `python3 -c "print(1)"` | Write `_temp.py`, run with source_me.sh |
| Inline JS | `node -e "console.log(1)"` | Write `_temp.mjs`, run with `node _temp.mjs` |
| Write file via printf | `printf '...' > FILE` | Use the Write tool (or Edit for appends) |
| Set env + run | `REPO_ROOT=/x && python3 s.py` | `REPO_ROOT=/x python3 s.py` (one line) |
| Run heredoc | `python3 - <<EOF ...` | Write `_temp.py`, run with source_me.sh |
| GitHub CLI | `gh pr list` | Not available (`gh` not installed) |
| Probe media | `ffprobe -show_streams f.m4b` | `mediainfo --Output=JSON f.m4b` (ffprobe only for chapters/packets/frames/lavfi) |
| Encode audio | `ffmpeg -i in.wav out.m4a` | Stage to `/tmp`: `ffmpeg -i /tmp/in.wav /tmp/out.m4a` |
