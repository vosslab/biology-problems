# Proposal: Investigate class checks in Python and Rust QPM

## Goal

Investigate how Python and Rust QPM should detect unsupported class-based styling in
Blackboard question output. Recommend the smallest appropriate change based on the code.

## Context

Blackboard Ultra needs SVG artwork and HTML tables rendered to PNGs first. Rendering inputs
and the HTML ultimately sent to Blackboard are different things; do not assume they should
have identical restrictions.

The Biology-problems source-scanning pytest catches common class usage, but Python generators
can assemble HTML dynamically. A source check alone cannot establish what the output contains.
QPM already has HTML and inline-CSS validation code worth investigating before adding anything.
QPM does not handle PGML.

## Questions to investigate

- Where does each implementation receive the final question HTML after PNG rendering?
- Which class or stylesheet usage can actually survive into Blackboard output?
- Can an existing validation point catch that usage without restricting rendering inputs or
  adding another validation layer?
- How should failures identify the offending content and reach the caller?
- What small set of existing tests can demonstrate the intended behavior in both implementations?

## Expected result

Return a concise recommendation grounded in the current code: the appropriate check location,
the minimum change needed, any demonstrated compatibility concern, and focused verification.
Leave implementation details to the manager's findings. Avoid speculative cases, new configuration,
and broad refactoring. This brief does not authorize QPM implementation.
