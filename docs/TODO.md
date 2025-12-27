# TODO

- Consider adding `bptools.make_outfile_from_args(__file__, args, *suffixes)` to auto-append common fields like `args.question_type` to output filenames. This would require wide refactors across scripts.
- Finish migrating the remaining scripts listed in `list_of_phase_1_python_scripts_to_upgrade.txt`.
- Work through `bugs_to_fix.txt` and close any remaining XML/HTML validator errors.
- Decide whether all scripts should have safe defaults (no required flags) for `question_type` and other mutually exclusive options.
- Add a small debug flag pattern (for temporary prints) so troubleshooting output is consistent and easy to remove.
- Review batch vs. individual script defaults and document when to use `add_base_args_batch()` vs. `add_base_args()`.
- Add or update examples in `docs/UNIFICATION_PLAN.md` for converting batch scripts to individual writers.
- Evaluate whether `bptools.make_outfile()` should support an optional `args` parameter instead of a new helper.
- Verify the updated prefix-stripping regex in `qti_package_maker` covers decimal numbers without breaking lettered prefixes.
- Normalize HTML table attribute quoting in older scripts that still use unquoted values.
- Consider adding a quick validator smoke test that runs a small set of generators and fails on HTML parsing errors.
