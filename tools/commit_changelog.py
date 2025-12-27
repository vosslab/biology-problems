import os
import shlex
import subprocess
import sys
import tempfile

def edit_file_in_editor(path: str) -> int:
    editor = (
        os.environ.get("GIT_EDITOR")
        or os.environ.get("EDITOR")
        or "nano"
    )
    cmd = shlex.split(editor) + [path]
    return subprocess.run(cmd).returncode

def confirm(prompt: str) -> bool:
    ans = input(prompt).strip().lower()
    return ans in ("y", "yes")

def commit_with_editor_gate(message: str) -> int:
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as tf:
        tf.write(message)
        msg_path = tf.name

    rc = edit_file_in_editor(msg_path)
    if rc != 0:
        print("Editor exited non-zero. Aborting.", file=sys.stderr)
        return rc

    with open(msg_path, "r", encoding="utf-8") as f:
        edited = f.read().strip()

    if not edited:
        print("Empty commit message. Aborting.", file=sys.stderr)
        return 2

    if not confirm("Proceed with git commit -a using this message? [y/N] "):
        print("Aborted.", file=sys.stderr)
        return 3

    return subprocess.run(["git", "commit", "-a", "-F", msg_path]).returncode
