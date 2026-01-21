# Matching Problems and Legacy PG Style

## Summary

Matching problems in WeBWorK **do not have a modern PGML-first inline answer specification**. The matching generator script ([problems/matching_sets/yaml_match_to_pgml.py](../../problems/matching_sets/yaml_match_to_pgml.py)) uses legacy PG style with `ANS()` calls because no modern alternative exists as of January 2026.

## Background

In January 2026, we updated the multiple-choice generator ([problems/multiple_choice_statements/yaml_mc_statements_to_pgml.py](../../problems/multiple_choice_statements/yaml_mc_statements_to_pgml.py)) to use pure PGML style, replacing:

```perl
BEGIN_PGML
[@ $rb->buttons() @]*
END_PGML
ANS($rb->cmp());
```

With modern inline answer specs:

```perl
BEGIN_PGML
[_]{$rb}
END_PGML
```

This eliminates the mixed-style warning from the PGML linter and follows modern WeBWorK authoring best practices.

## Research Findings

### What We Found

After extensive research including:

1. Official OpenWeBWorK PG documentation
2. WeBWorK wiki resources
3. Local PGML training corpus ([webwork-pgml-opl-training-set](https://github.com/example/training-set))
4. PGML linter documentation ([webwork-pgml-linter](https://github.com/example/linter))
5. LibreTexts ADAPT textbook materials ([webwork-pgml-libretexts-adapt-texbook](https://github.com/example/adapt))

**No modern PGML equivalent exists for matching problems.**

### Official Sources

The official OpenWeBWorK PG documentation sample for matching problems ([https://openwebwork.github.io/pg-docs/sample-problems/Misc/Matching.html](https://openwebwork.github.io/pg-docs/sample-problems/Misc/Matching.html)) uses legacy style as of January 2026:

```perl
# Create matching list using PGchoicemacros.pl
$ml = new_match_list();
$ml->qa(...);
$ml->choose(6);

BEGIN_PGML
[@ ColumnMatchTable($ml) @]***
END_PGML

# Legacy ANS() call (no PGML inline alternative exists)
ANS(str_cmp($ml->ra_correct_ans));
```

### Why No Modern Alternative

Matching problems rely on infrastructure from `PGchoicemacros.pl`, which predates PGML:

- `new_match_list()` creates a legacy match list object
- `ColumnMatchTable($ml)` renders the matching interface
- Answer checking requires `ANS(str_cmp($ml->ra_correct_ans))`

Unlike radio buttons (`RadioButtons` from `parserRadioButtons.pl`), which have MathObjects support and work with inline specs like `[_]{$rb}`, matching lists do not have a corresponding `parserMatchingList.pl` or equivalent modern macro.

### Training Corpus Gap

The [webwork-pgml-opl-training-set](https://github.com/example/training-set) repository contains **no matching problems**, confirming this is a known gap in the PGML ecosystem.

## Current Implementation

The matching generator ([problems/matching_sets/yaml_match_to_pgml.py](../../problems/matching_sets/yaml_match_to_pgml.py)) uses the legacy approach because:

1. It is the only documented method
2. The official OpenWeBWorK samples use this pattern
3. No modern PGML-first alternative has been developed
4. The implementation is stable and functional

### Code Pattern

```perl
# From build_statement_text() in yaml_match_to_pgml.py
BEGIN_PGML
[question text]
[note text]

[@ ColumnMatchTable($ml) @]***
END_PGML

# From build_solution_text() in yaml_match_to_pgml.py
ANS(str_cmp($ml->ra_correct_ans));
```

## Linter Behavior

The PGML linter ([webwork-pgml-linter](https://github.com/example/linter)) plugin `pgml_ans_style` will flag this pattern with:

```
WARNING: ANS() call after END_PGML block (mixed style).
Pure PGML uses inline answer specs: [_]{$answer} instead of ANS($answer->cmp())
```

**This warning is expected for matching problems** and reflects a limitation in the PGML ecosystem, not an authoring error.

## Recommendations

### For Matching Problem Authors

- Use the legacy pattern as shown in the official documentation
- Expect the PGML linter warning for matching problems
- Document matching problems as a known exception to pure PGML style

### For Future Updates

If a modern PGML matching solution becomes available (e.g., `parserMatchingList.pl` with inline answer spec support), this generator should be updated to use it. Monitor:

- OpenWeBWorK PG documentation updates
- New parser macros in WeBWorK releases
- Community discussions about PGML matching problems

## References

- Official matching sample: [https://openwebwork.github.io/pg-docs/sample-problems/Misc/Matching.html](https://openwebwork.github.io/pg-docs/sample-problems/Misc/Matching.html)
- PGchoicemacros documentation: [https://openwebwork.github.io/pg-docs/pod/pg/macros/ui/PGchoicemacros.html](https://openwebwork.github.io/pg-docs/pod/pg/macros/ui/PGchoicemacros.html)
- LibreTexts matching guidance: [webwork-pgml-libretexts-adapt-texbook/Textbook/05_Different_Question_Types/5.4-Matching.html](https://github.com/example/adapt)
- Related issue: Multiple choice generator modernization (January 2026)

## Document History

- 2026-01-21: Initial documentation of matching problems legacy style rationale
