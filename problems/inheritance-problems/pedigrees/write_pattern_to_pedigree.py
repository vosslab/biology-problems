#!/usr/bin/env python3
"""Given an inheritance pattern, answer with its randomly generated pedigree."""

import pedigree_lib.cli as cli


def main() -> None:
	args = cli.parse_arguments()
	cli.run(args, question_format='select')


if __name__ == '__main__':
	main()
