#!/bin/sh
# setup_playwright.sh - one-time Playwright install for smoke testing.
#
# The web-game-parallel-build skill mandates a Playwright smoke test
# between every batch. This script installs the @playwright/test package
# locally and the chromium browser. Idempotent; safe to rerun.
#
# Kept separate from setup_game.sh because the chromium download is
# heavier than the rest of npm install and may be skipped on machines
# where Playwright is already installed system-wide.

set -e

cd "$(git rev-parse --show-toplevel)"

if ! command -v npm >/dev/null 2>&1; then
	echo "ERROR: npm not found. Install Node.js first (e.g., 'brew install node')." >&2
	exit 1
fi

echo "Installing @playwright/test as a dev dependency..."
npm install --save-dev @playwright/test

echo "Downloading chromium browser for Playwright..."
npx playwright install chromium

echo
echo "Playwright setup complete. See templates/playwright_smoke_test.md"
echo "for the smoke-test recipe used between batches."
