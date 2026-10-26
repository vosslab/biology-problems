#!/usr/bin/env python3
"""Generate ordering questions from a YAML bank."""

import orderinglib


def main() -> None:
	orderinglib.main(mc=True)


if __name__ == '__main__':
	main()
