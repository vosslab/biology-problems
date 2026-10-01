#!/usr/bin/env python3
"""Generate pedigree homework through the shared family pipeline."""

import pedigree_lib.cli as cli


def main() -> None:
	args = cli.parse_arguments('authored')
	cli.run(args, matching=True)


if __name__ == '__main__':
	main()
