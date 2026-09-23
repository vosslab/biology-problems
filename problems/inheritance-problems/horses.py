#!/usr/bin/env python3

"""Compatibility entry point; use horse_coat_pattern_inference.py."""

import pathlib
import runpy


if __name__ == '__main__':
	generator_path = pathlib.Path(__file__).with_name(
		"horse_coat_pattern_inference.py"
	)
	runpy.run_path(str(generator_path), run_name="__main__")
