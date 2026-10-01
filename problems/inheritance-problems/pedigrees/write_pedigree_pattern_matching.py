#!/usr/bin/env python3
"""Match randomly generated pedigrees with their inheritance patterns."""

import pedigree_lib.cli as cli


def main() -> None:
	args = cli.parse_arguments()
	cli.run(args, question_format='match')


if __name__ == '__main__':
	main()
