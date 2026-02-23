# How to write WeBWorK problems with AI agents

This guide captures the workflow for converting biology homework into LibreTexts ADAPT WeBWorK
problems using AI agents, local rendering, and fast iteration.

## What this guide covers

- Move problem ideas from Blackboard-style content to ADAPT-ready WeBWorK.
- Use a local renderer as a strict pass/fail validation loop.
- Use AI agents to draft and revise PG/PGML without hand-debugging every syntax issue.
- Build and validate a two-part amino acid isoelectric point (pI) question.
- Improve final problem quality with randomization and accessibility checks.

## Prerequisites

- ADAPT context and authoring references:
  [vosslab/ADAPT-WeBWorK-Handbook](https://github.com/vosslab/ADAPT-WeBWorK-Handbook)
- Local WeBWorK renderer sandbox:
  [vosslab/webwork-pg-renderer](https://github.com/vosslab/webwork-pg-renderer)
- Local renderer running at `http://localhost:3000/`
- AI coding agent with access to a WeBWorK-focused skill/doc bundle
- Your content objective (example here: amino acid pI)

## Workflow summary

1. Define the teaching target first.
2. Draft a strict, explicit prompt for the AI.
3. Generate PG/PGML in the agent.
4. Render locally and inspect errors immediately.
5. Feed exact renderer errors back to the agent.
6. Repeat until the question renders and grades correctly.
7. Improve readability, accessibility, and randomization.

## Step 1: Define the problem contract

Start with the learning objective, then lock down what the generated problem must do.

Example objective used here:

- Topic: amino acid isoelectric points
- Part 1: choose the neutral protonation state from multiple charged states
- Part 2: infer pI from the titration curve and pKa positions
- Distractors: plausible values, but no duplicate logic traps

Reference content:
[LibreTexts amino acids and pI](https://chem.libretexts.org/Bookshelves/Organic_Chemistry/Organic_Chemistry_(Morsch_et_al.)/26%3A_Biomolecules-_Amino_Acids_Peptides_and_Proteins/26.03%3A_Amino_Acids_the_Henderson-Hasselbalch_Equation_and_Isoelectric_Points)

## Step 2: Treat local rendering as the source of truth

Do not trust agent output until it passes the renderer.

- Paste generated PG/PGML into the local sandbox.
- Use debug mode to inspect rendered HTML and macro behavior.
- Keep a short loop: generate -> render -> error -> revise.

Key principle: the AI contract is not "AI writes, human debugs forever." The AI must also help
close the debug loop.

## Step 3: Use constrained AI instructions

Unconstrained prompts often fail even for simple WeBWorK tasks. Constrain the agent:

- "Use only the WeBWorK skill docs for syntax and patterns."
- "Do not search unrelated folders for examples."
- "Return a complete, runnable PG/PGML problem."
- "Revise until it renders in the local renderer."

This reduces tool hallucination and keeps code aligned with actual PG behavior.

## Step 4: Start with a small sanity test

Before the complex biology item, run a tiny test question (for example, simple multiple choice).

- Confirms renderer is working
- Confirms agent can produce minimally valid PGML
- Exposes macro and formatting pitfalls early

If the tiny test fails repeatedly, fix the workflow before moving to full-content questions.

## Step 5: Build the full two-part pI item

Use the detailed content prompt and require the agent to output one complete problem file.

Target structure:

- Part 1: protonation-state recognition (identify neutral state)
- Part 2: pI selection using pKa relationships and curve logic
- Randomized variants so repeated attempts are not identical

Validation checks:

- Renders in the local sandbox without syntax/macro errors
- Correct answer grades as expected
- Distractors are plausible but unambiguous

## Step 6: Iterate for quality, not just correctness

After the item works, improve instructional quality:

- Clarify labels and state descriptions
- Improve color usage for charged/neutral groups
- Check contrast and avoid red-green-only distinctions
- Keep option wording consistent and scannable

Correct but confusing problems still underperform in class.

## Step 7: Add anti-copy randomization

Randomize values and state patterns so each student receives a different but equivalent item.

- Vary pKa sets within pedagogically valid ranges
- Keep the scoring logic invariant
- Re-render multiple seeds to verify stability

This supports learning while reducing answer sharing.

## Prompt template you can reuse

```text
Create a WeBWorK PG/PGML problem from scratch.
Topic: amino acid isoelectric points.

Requirements:
- Two parts.
- Part 1: multiple-choice state selection for neutral charge from protonation states.
- Part 2: titration-curve/pKa reasoning to identify pI.
- Include plausible distractors without duplicate-choice ambiguity.
- Use randomized variants.

Constraints:
- Use only the WeBWorK docs provided in the skill context.
- Do not search unrelated directories.
- Return complete runnable PG/PGML.
- Revise based on renderer errors until it passes.
```

## Quick checklist

- Objective is explicit and testable.
- Prompt includes required structure and constraints.
- Local renderer is used on every iteration.
- Correct answer path validates cleanly.
- Multiple random variants render and grade correctly.
- Accessibility pass completed (contrast and color logic).

## Suggested references

- [vosslab/ADAPT-WeBWorK-Handbook](https://github.com/vosslab/ADAPT-WeBWorK-Handbook)
- [vosslab/webwork-pg-renderer](https://github.com/vosslab/webwork-pg-renderer)
- [LibreTexts amino acid pI background](https://chem.libretexts.org/Bookshelves/Organic_Chemistry/Organic_Chemistry_(Morsch_et_al.)/26%3A_Biomolecules-_Amino_Acids_Peptides_and_Proteins/26.03%3A_Amino_Acids_the_Henderson-Hasselbalch_Equation_and_Isoelectric_Points)
