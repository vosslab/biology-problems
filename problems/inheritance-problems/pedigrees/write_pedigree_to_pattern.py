#!/usr/bin/env python3
"""Given a randomly generated pedigree, answer its inheritance pattern."""

import pedigree_lib.cli as cli


def main() -> None:
	args = cli.parse_arguments()
	cli.run(args, question_format='identify')


if __name__ == '__main__':
	main()
