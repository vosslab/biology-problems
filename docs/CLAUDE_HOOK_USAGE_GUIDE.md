# Claude hook usage guide

Best practices for AI agents working in repos that use the `claude-code-permissions-hook`.
This guide covers what commands are allowed, denied, and passed through, along with
preferred alternatives for denied patterns.

This doc is Claude-specific and does not apply to Codex.

This guide documents current Claude hook behavior. Repo style conventions live in
[docs/REPO_STYLE.md](REPO_STYLE.md) and [docs/PYTHON_STYLE.md](PYTHON_STYLE.md).

## Trust model

The hook optimizes for high task completion with bounded blast radius: allow routine
local work, deny/steer on machine-changing actions, prompt on high-impact operations.

## Overview

The permissions hook intercepts every Claude Code tool call and evaluates it against
TOML config rules. Each call gets one of three outcomes:

| Outcome | Meaning |
| --- | --- |
| **Allow** | Tool call proceeds automatically |
| **Deny** | Tool call is blocked with an error message |
| **Passthrough** | Falls back to Claude Code's default permission flow (user prompt) |

### Command decomposition

The hook splits compound Bash commands (`&&`, `||`, `;`, pipes) into leaf sub-commands
and checks each leaf independently:

- **Deny**: if ANY leaf matches a deny rule, the entire command is denied
- **Allow**: ALL leaves must match an allow rule for the command to be allowed
- **Passthrough**: if any leaf has no matching rule (and none are denied)

A compound command fails as a whole even if only one leaf is illegal. If
`find ... ; ls ...` is denied, the `ls ...` half would have run on its own --
drop the denied leaf and re-run rather than rewriting both.

The hook also unwraps `bash -c "..."` patterns and extracts commands inside `$(...)`.

Environment-variable assignments (e.g., `NODE_PATH=/foo`) are stripped from leaf
commands by the decomposer, so `NODE_PATH=/foo node script.js` is evaluated as
just `node script.js`.

### Max chain length

Commands with more than **5** chained sub-commands are denied automatically. Break
long chains into smaller commands or write a script file.

### Bash-side reference for redirected commands

`Read`, `Grep`, `Glob`, `Edit`, and `Write` are Claude Code *tool calls*,
invoked directly with named parameters. They replace the Bash forms below.
The third column lists the Bash forms that remain allowed for cases the tool
calls do not cover (typically slicing piped stdout or listing files for a
shell pipeline).

| Denied Bash form | Tool call | Allowed Bash forms |
| --- | --- | --- |
| `cat /path/to/file`, `head -20 /path`, `tail -20 /path` | `Read(file_path=..., offset=..., limit=...)` | `... \| cat`, `... \| head -5`, `... \| tail -5` (pipeline, no file arg) |
| `grep pat /path`, `/usr/bin/grep ...`, `rg pat dir/`, `egrep`, `fgrep` | `Grep(pattern=..., path=..., glob=..., output_mode=..., head_limit=...)` | `... \| grep pat` (pipeline, no file arg) for stdout filtering |
| `find . -name "*.py"` (any path form) | `Glob(pattern='**/*.py', path=...)` | `ls <dir>`, `git ls-files <pathspec>` |
| `sed -n '10,20p' file.txt` | `Read(file_path=..., offset=10, limit=11)` | `... \| sed -n '10,20p'` (pipeline) |

The deny rules cover all binary variants (alternate names, absolute paths like
`/usr/bin/grep` or `/opt/homebrew/.../grep`, `rg`). The fastest path through a
deny is the tool call in column two.

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
bash -n script.sh        # syntax check only
./script.sh
./script.py
./subdir/script.py
tools/runner.py          # bare relative-path scripts
scripts/build.sh
```

### Safe utilities

These commands are allowed as single commands. Command substitution is blocked.

**File and text processing:**
`awk`, `cat`, `colordiff`, `comm`, `cut`, `diff`, `expand`, `file`, `fmt`, `fold`,
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
dedicated tools (Read, Grep, Glob) instead.

### Local runtimes

**Node.js:**
`node` is allowed for running `.js`, `.mjs`, and `.cjs` files, syntax checking with
`-c` or `--check`, inline evaluation with `-e` or `--eval`, and `--version` queries.

```bash
node script.js
node -c script.js
node -e "require('./data.json')"
node --version
```

**npx (whitelisted packages):**
`npx` is allowed for a whitelist of known-safe local dev tool packages: `tsc`,
`eslint`, `prettier`, `playwright`, `esbuild`. Unknown packages still require
user approval (passthrough).

```bash
npx tsc --noEmit              # allowed
npx eslint src/               # allowed
npx prettier --check .        # allowed
npx playwright screenshot ... # allowed
npx esbuild src/x.ts          # allowed
npx some-package              # requires approval
```

If `npx tsc` fails because TypeScript is not installed, stop and tell the user
to run `npm install --save-dev typescript` (or `npm install -g typescript` for
a global install). Do not work around the failure by calling
`./node_modules/.bin/tsc` or `node_modules/typescript/bin/tsc` directly --
those paths are denied (see "Denied commands" below).

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

These tools may write output files anywhere by default, but are auto-allowed
when every path argument lives under `/tmp/` or `/private/tmp/`:

`ffmpeg`, `sox`, `convert`, `magick`, `mogrify`, `gm`, `optipng`, `pngcrush`,
`jpegoptim`, `cwebp`, `tesseract`, `qpdf`, `pdftk`, `gs`, `lame`, `flac`

The rule requires at least one literal `/tmp/` (or `/private/tmp/`) token in
the leaf and blocks invocations that touch any non-scratch absolute root
(`/Users`, `/etc`, `/usr`, `/opt`, `/var`, `/Library`, `/System`, etc.).
Virtual sources (`-f lavfi -i sine=...`, stdin `-`, sox null sink `-n`)
ride along as long as a real `/tmp/` path is also in the leaf.

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

| Tool | Allowed paths |
| --- | --- |
| Read | `~/nsh/`, `~/.<dotdirs>`, site-packages, `/tmp/`, `/var/folders/` |
| Write | `~/nsh/`, `~/.claude/`, `/tmp/` |
| Edit | `~/nsh/`, `~/.claude/`, `/tmp/` |
| Glob | `~/nsh/`, `~/.claude/`, `/tmp/` |
| Grep | `~/nsh/`, `~/.claude/`, `/tmp/` |

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

**Blocked:** `rm file.txt`, `rm -rf dir/`

**Why:** Prevents accidental deletion of important files.

**Instead:** Use underscore-prefixed filenames for scratch files (`_temp.py`),
write to `/tmp/`, or use `git rm` for tracked files.

### `git commit`, `git stash`, `git clean` (branch-aware)

**Blocked on protected branches:** `git commit`, `git commit --amend` (all variations
including flag insertion like `git -C /tmp commit`). `git stash` and `git clean` are
denied everywhere.

**Why:** On protected branches (typically `main`, `master`), commits are made by the
human after reviewing the staged merge via `git diff`. On agent branches, you have
full commit access. `git stash` and `git clean` are destructive and remove tracked
or untracked work.

**Instead:** Work on an `agent/<task>` branch where commits are allowed. To prepare
a merge into a protected branch, use `git merge --no-commit --no-ff agent/<task>`
and let the human review and commit. See
[Worktrees and protected branches](#worktrees-and-protected-branches) for the full
workflow.

### `cat`/`head`/`tail` with file paths

**Blocked:** `cat /path/to/file`, `head -20 /abs/path/file.txt`

**Why:** Read is a Claude Code tool call (like Edit/Write). It provides line
numbers, offset, and limit, and is the canonical way to inspect a file from
this harness.

**Instead:** Invoke the Read tool directly with `file_path` and optional
`offset` and `limit`. The pipeline form (`... | head -5`, `... | tail -5`,
`... | cat`) stays allowed for slicing piped stdout, where Read does not
apply.

### `grep`/`rg` with file paths

**Blocked:** `grep pattern /path/to/file`, `rg pattern /abs/search/dir`,
`/usr/bin/grep ...`, `/opt/homebrew/.../grep ...`, `egrep`, `fgrep`. The
deny covers all binary names and absolute paths.

**Why:** Grep is a Claude Code tool call (like Read/Edit/Write). It supplies
structured output modes, glob filters, and context lines, and is the
canonical way to search files from this harness.

**Instead:** Invoke the Grep tool directly with `pattern`, `path`, `glob`,
`-A`/`-B`/`-C`, `output_mode`, and `head_limit`. The pipeline form
(`... | grep pat`) stays allowed for slicing piped stdout, where Grep does
not apply.

### `git grep`

**Blocked:** `git grep <pattern>`, including all git invocation forms
(`/usr/bin/git grep`, `command git grep`, `env X=y git grep`,
`git -c core.pager=cat grep`, `git -C <path> grep`,
`git --git-dir=<dir> grep`, `git --work-tree=<dir> grep`).

**Why:** Grep is a Claude Code tool call (like Read/Edit/Write); `git grep`
would keep every search shell-side and re-create the loop the file-`grep`
deny is meant to break. The Grep tool is the canonical search path.

**Instead:** Invoke the Grep tool directly with `pattern`, `path`, `glob`,
`-A`/`-B`/`-C`, `output_mode`, and `head_limit`. There is no Bash escape
hatch for repo searches. For Bash file listings, `ls <dir>` and
`git ls-files <pathspec>` remain allowed.

### `find`

**Blocked:** `find . -name "*.py"`, including absolute-path invocations.

**Why:** Glob is a Claude Code tool call (like Read/Edit/Write) and supports
recursive patterns directly.

**Instead:** Invoke the Glob tool directly with `pattern='**/*.py'` and `path`.
For a shell-side file listing, `ls <dir>` and `git ls-files <pathspec>` are
both allowed.

### `sed -n` with file paths

**Blocked:** `sed -n '10,20p' file.txt`

**Allowed (pipe usage):** `git diff HEAD -- file.py | sed -n '250,400p'`
-- paginating subprocess stdout is fine; Read can't substitute for it.

**Why:** The Read tool with offset and limit does file reads better, but sed
is the right tool for slicing piped stdout.

**Instead (file case):** Use `Read(file_path='file.txt', offset=10, limit=11)`.
Other sed operations (substitution, etc.) are allowed.

### Claude Code tool names typed as Bash commands

**Blocked:** `Grep -n "^## " docs/CHANGELOG.md`, `Read README.md`,
`Glob "**/*.py"`, `Edit file.py`, `Write /tmp/x.py`. Also caught when
chained or piped, since the decomposer splits leaves before matching:
`echo hi && Read README.md`, `cat /tmp/x | Grep foo`.

A grep pattern that *contains* a tool name is not affected:
`grep "Grep\|Read" file` is allowed (the deny anchors at start-of-leaf,
so only the lowercase `grep` token matters).

**Why:** `Grep`, `Read`, `Glob`, `Edit`, `Write`, `Task`, `WebFetch`, and
`WebSearch` are Claude Code TOOLS, not shell commands. Pasting the tool
name into Bash runs whatever (if anything) is on `PATH` by that name --
not the actual tool.

**Instead:** Invoke the tool directly as a tool call with its real
parameters (e.g., the Grep tool with `pattern='^## '`,
`path='docs/CHANGELOG.md'`).

### Pipe-only commands (allowed in pipes, denied as the lead command)

These tools have a "use the dedicated tool instead" deny when run against
a file path, but remain allowed when consuming piped stdin:

| Command | Denied (lead) | Allowed (in pipe) |
| --- | --- | --- |
| `cat`, `head`, `tail` | `cat /tmp/x.txt` | `... \| head -5` |
| `grep`, `egrep`, `fgrep`, `rg` | `grep pat /tmp/x.txt` | `... \| grep pat` |
| `sed -n` | `sed -n '10,20p' /tmp/x.txt` | `... \| sed -n '10,20p'` |

The decomposer splits Bash commands on `|`/`&&`/`;` and evaluates each
leaf independently. A pipeline leaf with no file path argument matches
the "safe utility" allow list; the same command with a file argument
hits a deny that steers to the Read or Grep tool.

### `tsc` via `node_modules` paths

**Blocked:** `./node_modules/.bin/tsc`, `./node_modules/typescript/bin/tsc`,
`/abs/path/node_modules/typescript/bin/tsc`,
`node node_modules/typescript/bin/tsc`

**Why:** Project-local `tsc` paths are a workaround for `npx tsc` failing.
Retrying different invocation forms wastes turns and masks missing installs.

**Instead:** Use `npx tsc` (whitelisted). If `npx tsc` fails because TypeScript
is not installed, run exactly one of these two commands (both are whitelisted):

```bash
npm install --save-dev typescript   # allowed
npm install -g typescript           # allowed
```

Any other `npm install` variation (different flags, version pins, extra
packages, bare `npm install`) still passes through for user approval.

Do not work around the failure with absolute paths, `node node_modules/...`,
or `source source_me.sh &&` chains.

### `ffprobe` (steered to `mediainfo`)

**Blocked:** `ffprobe file.m4b`, `ffprobe -show_streams file.mp3`,
`ffprobe -i file.wav`

**Why:** `mediainfo` produces cleaner JSON for container, codec, and track
metadata and is the preferred tool.

**Instead:** Use `mediainfo --Output=JSON <file>`. `ffprobe` is allowed
only with the flags `mediainfo` cannot replicate:

```bash
ffprobe -show_chapters file.m4b   # allowed (chapter atoms)
ffprobe -show_packets file.m4b    # allowed (per-packet timing)
ffprobe -show_frames  file.mp4    # allowed (per-frame timing)
ffprobe -f lavfi -i sine=440      # allowed (synthetic/lavfi probe)
```

### `perl` on `.pg`/`.pgml` files

**Blocked:** `perl -c problem.pgml`, `perl problem.pg`

**Why:** PGML is not standard Perl. Running perl on these files produces misleading
results.

**Instead:** Use the `/webwork-writer` skill lint guide to validate WeBWorK problems.

### Heredocs (`<<EOF`)

**Blocked:** `python3 - <<EOF`, `bash <<'SCRIPT'`

**Why:** Heredocs are hard to read, lint, and test.

**Instead:** Write code to a `_temp.py` or `_temp.sh` file using the Write tool,
then run it with `source source_me.sh && python3 _temp.py` or `bash _temp.sh`.
Underscore-prefixed files can be removed freely.

### `for` and `while` loops

**Blocked:** `for f in *.py; do ...`, `while read line; do ...`

**Why:** Loop logic belongs in script files, not inline Bash.

**Instead:** Write the logic in a `_temp.py` or `_temp.sh` file and execute it.

### `bash -c` / `bash -lc`

**Blocked:** `bash -c "command"`, `bash -lc "source && python3 ..."`

**Why:** The Bash tool already runs bash. `bash -c` is redundant bash-in-bash.

**Instead:** Run the command directly: `source source_me.sh && python3 script.py`.
Running script files (`bash script.sh`, `bash -n script.sh`) is still allowed.

### `sudo`

**Blocked:** `sudo command`

**Why:** Do not escalate to root. Ask the user to run privileged commands manually.

**Instead:** Ask the user to run the command as root if truly necessary.

### `git reset --hard`

**Blocked on protected branches:** Destructive history rewrite. Denied on protected
branches (`main`, `master`); allowed on agent/feature branches for local work.

**Instead on protected:** Use safer alternatives like `git checkout -- file` or
`git restore file` to discard working changes.

**On agent branches:** `git reset --hard` is allowed for local cleanup and rebasing
your own work.

### `git restore .` and `git checkout -- .` (wholesale discard)

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

**Why:** These forms have the same blast radius as `git reset --hard` --
they wipe every uncommitted change and unstage all renames in one shot.
That destroys agent work in progress (edits, renames, staged content) with
no recovery path other than `git reflog`.

**Instead:** Discard a single file at a time:

- `git restore path/to/file.py` (allowed)
- `git restore --staged path/to/file.py` (allowed)
- `git checkout -- one_file.py` (allowed)
- `git checkout HEAD~1 -- file.py` (allowed)

Branch switches (`git checkout main`, `git checkout -b feature/x`) remain
allowed unchanged. If you really want to wipe everything, ask the user to
run the command themselves.

### `git push --force` (including --force-with-lease)

**Blocked:** `git push --force`, `git push origin main --force-with-lease`

**Why:** Destructive remote history change.

**Instead:** Ask the user to push manually if rebase is necessary.

### `deno run` with URLs

**Blocked:** `deno run https://example.com/script.ts`

**Why:** Remote code execution. Download and review first.

**Instead:** Download with `curl` to a file, review it, then run locally.

### `curl`/`wget` piped to runtime

**Blocked:** `curl https://example.com/install.sh | bash`, `wget -O - url | python3`

**Why:** Executes remote code without local review.

**Instead:** Download to a file first with `curl -o script.sh https://...`, review,
then run.

### Write/Edit to system directories

**Blocked:** Writing to `/etc/`, `/usr/`, `/opt/`, `/System/`, `/Library/`

**Why:** System files should only be modified by root or package managers.

**Instead:** Write to `~/nsh/` or `/tmp/` instead.

### `mv`

**Blocked:** `mv old.py new.py`

**Why:** Use `git mv` for tracked files to preserve history.

**Instead:** `git mv old.py new.py`. For untracked files, use `cp` + `rm` or ask
the user.

### `VAR=$(...)` assignments

**Blocked:** `PROJECT=$(basename $PWD)`, `OUTPUT=$(python3 script.py)`

**Why:** Command substitution in assignments creates hidden side effects.

**Instead:** Use `source source_me.sh` for environment setup or inline the command
directly.

### `$PYTHON` variable

**Blocked:** `$PYTHON script.py`, `${PYTHON} -m pytest`

**Why:** Use the actual interpreter name for clarity.

**Instead:** `python3 script.py`

### `PYTHONDONTWRITEBYTECODE` / `PYTHONUNBUFFERED`

**Blocked:** Setting these environment variables manually.

**Why:** `source_me.sh` already exports these.

**Instead:** `source source_me.sh && python3 ...`

### Bare variable assignments

**Blocked:** `REPO_ROOT=/path/to/repo` (with no command following)

**Why:** The decomposer splits `A=x && cmd` into leaves; a bare `A=x` leaf is
useless.

**Instead:** Use space-separated env prefixes on one line: `REPO_ROOT=/path python3 script.py`

### `gh` CLI

**Blocked:** All `gh` commands.

**Why:** `gh` is not installed on this system.

**Instead:** N/A. GitHub operations are not available via CLI.

### Homebrew python `-c`

**Blocked:** `/opt/homebrew/bin/python3 -c "print('hello')"`

**Why:** Inline code is hard to lint and debug.

**Instead:** Write a `_temp.py` file and run it with
`source source_me.sh && python3 _temp.py`.

## Worktrees and protected branches

Agents work on `agent/<task>` branches (often inside a worktree) and prepare
merges into protected branches (`main`, `master` by default) using:

```bash
git merge --no-commit --no-ff agent/<task>
```

This stages the merge result without creating the commit. The human reviews
with `git diff HEAD` and runs the final `git commit` and `git push` themselves.
Direct `git commit`, `git rebase`, `git reset --hard`, `git cherry-pick`,
`git revert`, and pushes targeting protected refs are denied while on a
protected branch; the same commands are allowed on a feature/agent branch.

For shipped copies of this guide, treat this section as the complete worktree
summary: agents prepare changes, humans create final commits and pushes, and
protected-branch history-changing commands stay denied.

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
- Use dedicated tools (Read, Grep, Glob) instead of their Bash equivalents
- Write scratch code to `_temp.py` or `_temp.sh` (underscore prefix = safe to delete)
- Keep compound commands under 5 chained sub-commands
- No command substitution (`` ` `` or `$(...)`) in variable assignments
- Use relative paths for project files where possible
- For loops or conditionals, write a script file instead of inline Bash
- Stage changes and update `docs/CHANGELOG.md`; let the user commit

## Common patterns

The Grep, Read, Glob, Edit, and Write entries below are Claude Code
*tool calls*, not shell commands. Invoke them as tools, not via Bash.
There is no Bash escape hatch for searching repo files -- use the Grep
tool. For Bash file listings, `git ls-files <pathspec>` and `ls <dir>`
are allowed; for slicing piped stdout, `... | grep pat`, `... | head -5`,
and `... | sed -n '10,20p'` are allowed.

| Task | Wrong | Right |
| --- | --- | --- |
| Run Python | `python3 script.py` | `source source_me.sh && python3 script.py` |
| Read a file | `cat /path/to/file.py` | Read tool: `file_path="/path/to/file.py"` |
| Search files | `grep -r "pattern" src/` | Grep tool: `pattern="pattern"`, `path="src/"` |
| Tool name as Bash | `Grep -n "^## " docs/CHANGELOG.md` | Invoke the Grep tool directly (not via Bash) |
| Find files | `find . -name "*.py"` | Glob tool: `pattern="**/*.py"`. For Bash listings, `ls <dir>` or `git ls-files '*.py'` |
| Read lines 10-20 | `sed -n '10,20p' file.txt` | Read tool: `offset=10`, `limit=11` |
| Delete temp file | `rm temp.py` | Name it `_temp.py`, then `rm _temp.py` |
| Rename file | `mv old.py new.py` | `git mv old.py new.py` |
| Loop over files | `for f in *.py; do ...` | Write `_temp.sh` with the loop, run `bash _temp.sh` |
| Inline Python | `python3 -c "print(1)"` | Write `_temp.py`, run with source_me.sh |
| Set env + run | `REPO_ROOT=/x && python3 s.py` | `REPO_ROOT=/x python3 s.py` (one line) |
| Run heredoc | `python3 - <<EOF ...` | Write `_temp.py`, run with source_me.sh |
| GitHub CLI | `gh pr list` | Not available (`gh` not installed) |
| Probe media | `ffprobe -show_streams f.m4b` | `mediainfo --Output=JSON f.m4b` (ffprobe only for chapters/packets/frames/lavfi) |
| Encode audio | `ffmpeg -i in.wav out.m4a` | Stage to `/tmp`: `ffmpeg -i /tmp/in.wav /tmp/out.m4a` |
