## 2026-10-06

### Fixes and Maintenance

- Audited all 81 YAML replacement-rule mappings. Kept color-palette placeholders and short
  aliases, replaced obsolete plural/closing-tag workarounds with direct rules, and added full
  inflected forms so color spans cover complete words. Fixed singular-to-plural substitutions,
  lost spaces, misspelled labels, and the proofreading direction replaced by "primase".
  Removed unrelated copied rules and redundant bold wrappers inside color replacements.
- Corrected grammar and typos across the inheritance matching-set YAML banks. Color rules
  now preserve plural spellings, avoid duplicated F1/F2 generation labels, and retain the
  intended genotype and ectopic terminology. Added missing whole-word plural color rules.
- Addressed wording review by removing two dominance variants that incorrectly assume a
  dominant allele is always present, defining genetic code in terms of mRNA translation,
  describing drift through allele-frequency changes, and simplifying chromosome-arm wording.
- Reduced pedigree polish search work by skipping unions at their configured non-founder child
  cap and generations whose added child cannot improve row progression. Existing shuffle and
  random-draw order, difficulty checks, and acceptance gates remain; configured numeric limits
  are unchanged. On the 50 saved inputs, whole-call replay counts fell from 820 to 533 `Family`
  constructions and from 591 to 304 difficulty checks, including the unchanged final check.
  Timings did not establish a speed benefit.

### Behavior or Interface Changes

- WeBWorK replacement pairs now use the same literal, longest-match pass as Blackboard,
  replacing temporary-token substitution. Short aliases such as `stattest` remain supported,
  including at the end of a string. Deliberate short-word boundary guards remain where needed.
- Text replacement helpers now use one literal, longest-match pass over each source string;
  inserted markup is never matched again. The implementation spells out sorting, escaping,
  and match lookup. Updated the thermodynamics plural rule to match source text directly.
  Statement-question generation now formats stems and every choice once before constructing
  items, preventing repeated tagging across duplicate questions and final output formatting.
  Existing HTML is still eligible for matching; callers must supply each source field once.
- Added the user-selected 5% exact affected-count teaching filter to shared pedigree acceptance.
  Each sibship is tested conditional on offspring sexes; extreme candidates are rejected and
  generation continues randomly. Repair, polishing, and cache reuse share the gate. Four affected
  offspring from `Aa x Aa` are rejected; three of four remain eligible (tail 0.05078125).
  Cache records now preserve original genotypes, validate them against observations and inheritance,
  and skip legacy entries that cannot supply the original parental cross.
- Added the matched terminal-frontier interest review to
  [PEDIGREE_EVIDENCE.md](../problems/inheritance-problems/pedigrees/PEDIGREE_EVIDENCE.md).
  Two reviewers found no higher interest; their balance, readability, and usefulness judgments
  differed. The evidence preserves production policy and records the corrected-run limitation.

### Developer Tests and Notes

- Replacement audit: 80 focused tests passed; all matching and statement YAML files validated
  with zero errors and five existing warnings. Across 5,592 strings, Blackboard and WeBWorK
  replacement output matched exactly, with no nested color spans, partial-word matches, or
  closing-tag repair rules. All original palette placeholders were checked for preservation.
  The local WeBWorK renderer was unavailable on port 3000; browser rendering was not validated.
- Replacement and YAML-generator checks passed (48 tests). A one-time comparison of 3,438
  source strings across 81 rule-bearing YAML banks found no visible-text changes from the
  single-pass helper. Regression coverage checks plural precedence, literal keys and values,
  unmodified replacement output, item answer consistency, and statement-field formatting.
- The 5% pedigree filter passed the full suite (5,048 tests; two existing source-length warnings)
  and scoped `pyflakes`. Independent exhaustive enumeration agreed with the exact-tail helper for
  all 1,911 sibships in 200 fresh pedigrees across four difficulties; all met the cutoff and retained
  identical tails after cache round trips. The saved four-of-four case was rejected, and a bank with
  that case plus a legacy entry replenished successfully. All three CLI formats exported BBQ and
  HTML self-tests; question-text checks found no issues. Local evidence is under
  `output_pedigree/probability_filter_20261006/`.
- Audited the current pedigree generator with the existing probability tool: 200 fresh accepted
  cases had no impossible transmissions; four had whole-pedigree p < 0.05 and six had a sibship
  joint sex/phenotype p < 0.05. A separate 1,000-case medium autosomal-recessive probe reproduced
  one four-of-four affected carrier cross. Its joint p = 0.0146 exceeds 1% despite the affected-count
  tail being 1/256. Recorded an exact per-sibship phenotype-screen recommendation without changing
  generation policy; six diagnostic tests passed. See the
  [pedigree_offspring_probability_20261006.md](archive/audits/pedigree_offspring_probability_20261006.md).
- Focused pedigree tests passed (148); scoped `pyflakes` passed. All 50 saved inputs retained
  byte-identical results and ending RNG state. Whole-call replay work counts included the final
  endpoint check; paired timings varied without establishing a speed benefit.
