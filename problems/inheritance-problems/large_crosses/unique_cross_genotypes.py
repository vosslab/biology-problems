#!/usr/bin/env python3
"""Existing homework entry point; shared implementation is unique_counts_lib."""

import unique_counts_lib


def main() -> None:
	unique_counts_lib.main('genotypes', default_genes=6)


if __name__ == "__main__":
	main()
