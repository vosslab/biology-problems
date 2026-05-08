// Resolve repo root via git, not via brittle relative-path math.
// Imported by tests/playwright/*.mjs and tests/playwright/e2e/*.mjs

import { execSync } from "node:child_process";

// .trim() strips the trailing newline git rev-parse appends; without it,
// path.join(REPO_ROOT, "...") would produce a broken path.
export const REPO_ROOT = execSync("git rev-parse --show-toplevel", { encoding: "utf8" }).trim();
