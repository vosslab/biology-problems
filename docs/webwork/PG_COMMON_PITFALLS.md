# PG Common Pitfalls and Debugging Guide

This guide documents common errors, gotchas, and debugging strategies when writing PG/PGML problems, based on real issues encountered in this repository.

---

## Critical: Order of Operations

### Pitfall: Using Variables Before They're Defined

**Problem:** Creating arrays or using variables before their values are assigned.

```perl
# WRONG - shuffle happens before cards are defined!
@all_cards = ($card1, $card2, $card3);  # Line 100 - cards are undefined!
# ... 50 lines later ...
$card1 = '<div>content</div>';          # Line 150 - TOO LATE!
```

**Symptom:** Empty output, missing content, canvases don't render

**Fix:** Define variables BEFORE using them
```perl
# RIGHT - define first, use second
$card1 = '<div>content</div>';          # Define
$card2 = '<div>content</div>';
$card3 = '<div>content</div>';
# ... all definitions ...
@all_cards = ($card1, $card2, $card3);  # THEN use
```

**Why this happens:**
- PG executes code linearly (top to bottom)
- Unlike some languages, Perl doesn't hoist variable declarations
- Undefined variables become empty strings without warnings in PG

**Where to check:** Look at line numbers in your code. Variables must be assigned BEFORE they're referenced.

**Example from this repo:**
- File: `histidine_protonation_states.pgml`
- Bug: Shuffle code at line 100, cards defined at line 116+
- Fix: Moved shuffle to after line 183 (after all cards defined)

---

## PGML Parsing Issues

### Pitfall 1: Asterisks Around Variables

**Problem:** PGML interprets `*` as markdown italics, causing parsing errors when variables contain certain content.

```perl
# WRONG - PGML tries to parse * as italics
BEGIN_PGML
The answer is *[$variable]*.
END_PGML
```

**Error:** `'*' was not closed before paragraph ends`

**Fix:** Use different emphasis or remove asterisks
```perl
# Option 1: Use bold (**) instead
The answer is **[$variable]**.

# Option 2: Remove emphasis
The answer is [$variable].

# Option 3: Use HTML emphasis variable
$answer_emph = "<strong>$variable</strong>";
The answer is [$answer_emph]*.  # * here means "don't escape HTML"
```

**When this fails:**
- Variables that might contain their own asterisks
- Variables next to literal asterisks (bullets, emphasis)
- Multiple `*` markers in close proximity

---

### Pitfall 2: Bold Markers Around Variables

**Problem:** Bold `**` around variables can break if variable contains markup.

```perl
# RISKY - can fail with certain variable content
At pH [$selected_ph], histidine exists in **[$correct_label]**.
```

**Error:** `'**' was not closed before paragraph ends`

**Fix:** Keep variables outside of markdown markers
```perl
# SAFE
At pH [$selected_ph], histidine exists in [$correct_label].
```

---

### Pitfall 3: Using `*` for Bullets in PGML Lists

**Problem:** PGML can confuse `* item` (bullet) with `*italics*` markers.

```perl
# CAN CAUSE ISSUES
BEGIN_PGML
* *State 1* (pH < 1.82): Description
* *State 2* (pH > 1.82): Description
END_PGML
```

**Fix:** Use dashes for bullets when you have italic content
```perl
# SAFER
BEGIN_PGML
- **State 1** (pH < 1.82): Description
- **State 2** (pH > 1.82): Description
END_PGML
```

---

## HTML in PGML

### Pitfall: Forgetting the `*` in `[$var]*`

**Problem:** HTML variables display as literal text instead of rendering.

```perl
$html_content = '<span style="color:red;">Important</span>';

BEGIN_PGML
This is [$html_content] text.
END_PGML
```

**Output:** `This is <span style="color:red;">Important</span> text.` (literal HTML shown!)

**Fix:** Add `*` after the variable to prevent HTML escaping
```perl
BEGIN_PGML
This is [$html_content]* text.
END_PGML
```

**Output:** `This is` <span style="color:red;">Important</span> `text.` (HTML rendered!)

**Rule:** `*` means "don't escape HTML" when used with `[$var]*`

---

## Loops and Control Flow in BEGIN_TEXT

### Pitfall: Using Perl Loops Inside BEGIN_TEXT

**Problem:** `foreach`, `for`, `while` loops don't execute inside `BEGIN_TEXT` blocks.

```perl
# WRONG - loop doesn't execute!
BEGIN_TEXT
foreach my $item (@items) {
    \{ MODES(HTML => $item, TeX => '') \}
}
END_TEXT
```

**Result:** No output, empty page

**Fix:** Build string BEFORE BEGIN_TEXT or use array indexing
```perl
# Option 1: Build before BEGIN_TEXT
$all_items_html = '';
foreach my $item (@items) {
    $all_items_html .= MODES(HTML => $item, TeX => '');
}

BEGIN_TEXT
\{ $all_items_html \}
END_TEXT

# Option 2: Use array indexing (if fixed number)
BEGIN_TEXT
\{ MODES(HTML => $items[0], TeX => '') \}
\{ MODES(HTML => $items[1], TeX => '') \}
\{ MODES(HTML => $items[2], TeX => '') \}
END_TEXT
```

**Why:** `BEGIN_TEXT...END_TEXT` is a special string construction block, not regular Perl code execution.

---

## Shuffling and Randomization

### Pitfall: Shuffle Timing

**Problem:** Shuffling variables before they're defined (see Order of Operations above).

**Correct Pattern:**
```perl
# 1. Define all items first
$item1 = "content 1";
$item2 = "content 2";
$item3 = "content 3";

# 2. Create array
@all_items = ($item1, $item2, $item3);

# 3. Shuffle
@shuffled = ();
@temp = @all_items;
while (@temp) {
    my $index = random(0, $#temp, 1);
    push @shuffled, splice(@temp, $index, 1);
}
```

---

### Pitfall: Hash Key Order Not Deterministic

**Problem:** Iterating over hash keys gives random order that changes between runs.

```perl
# WRONG - order changes every time!
%items = (a => 'Apple', b => 'Banana', c => 'Cherry');
@choices = values %items;  # Random order!
```

**Fix:** Sort keys before selection
```perl
# RIGHT - deterministic order
@sorted_keys = sort keys %items;
$selected = list_random(@sorted_keys);
```

**From documentation:** RANDOMIZATION_REFERENCE.md explicitly warns about this.

---

## Answer Checking

### Pitfall: Legacy ANS() vs PGML Inline Grading Complexity

**Trade-off discovered:**

**PGML Inline (Modern but Complex):**
```perl
# Requires RadioButtons widget, hidden CSS, JavaScript sync
$rb = RadioButtons(['A', 'B'], 'A');
BEGIN_PGML
[_]{$rb}
END_PGML
# Plus complex CSS/JS to hide and sync custom UI
```

**Legacy ANS() (Old but Simple):**
```perl
# Just works with str_cmp
BEGIN_TEXT
\{ ans_rule(20) \}
END_TEXT
ANS(str_cmp($correct_answer));
# Plus simple JS to populate hidden field
```

**Lesson:** Sometimes "legacy" is the pragmatic choice when modern approach is too fragile.

**Use legacy when:**
- Custom UI requires complex JavaScript
- Standard widgets don't fit your layout
- You need simple string comparison
- Code clarity > modern conventions

---

## JavaScript and WebWork

### Pitfall: Answer Field Names

**Problem:** Creating hidden inputs with wrong names that don't match ANS() expectations.

```perl
# WRONG - JavaScript creates input, but ANS() looks elsewhere
ANS(str_cmp($answer));  # Looks for AnSwEr0001
# JS creates input with different name - no connection!
```

**Fix:** Create proper answer blank first
```perl
# Create answer blank that ANS() will check
BEGIN_TEXT
\{ MODES(HTML => '<div style="display:none;">' . ans_rule(20) . '</div>', TeX => '') \}
END_TEXT

# This creates input[name="AnSwEr0001"]
ANS(str_cmp($answer));  # Now they match!
```

**Rule:** `ans_rule()` creates the input field that `ANS()` checks. Create the rule first, THEN call ANS().

---

## RDKit Specific

### Pitfall: SMILES Chemistry Errors

**Problem:** Using incorrect formal charge notation for imidazole ring.

```perl
# WRONG - NH2+ implies TWO hydrogens on one nitrogen
$imidazole_protonated = '...N=C[NH2+]1)...';
```

**Correct:** Imidazole has TWO nitrogens; when protonated, one has H and one has H+
```perl
# RIGHT - one NH and one NH+
$imidazole_protonated = 'C1=C([NH]C=[NH+]1)...';
```

**Chemistry check:** Always validate SMILES with Python RDKit before using.

**See:** RDKIT_MOLECULAR_STRUCTURES.md for detailed chemistry guidance.

---

## Debugging Strategies

### Strategy 1: Check Line Numbers

When variables seem empty or undefined:
1. Find where variable is USED (grep for `$var_name`)
2. Find where variable is DEFINED (`$var_name = ...`)
3. Compare line numbers - definition must come first!

### Strategy 2: Isolate PGML Errors

When getting `'*' was not closed` or similar:
1. Comment out half the PGML block
2. Test - does error persist?
3. Binary search to find problematic line
4. Check for `*`, `**`, or `_` near variables

### Strategy 3: Test with Minimal Example

Create minimal test file:
```perl
# test.pgml
DOCUMENT();
loadMacros("PGstandard.pl", "PGML.pl");

$var = "test";

BEGIN_PGML
Test: [$var]
END_PGML

ENDDOCUMENT();
```

Add complexity incrementally until problem reproduces.

### Strategy 4: Check Renderer Output

Use `-r` flag to see actual HTML:
```bash
python3 lint_pg_via_renderer_api.py -i file.pgml -r > output.html
```

Then inspect:
- Are canvas elements present? (`grep '<canvas'`)
- Is HTML escaped? (look for `&lt;` instead of `<`)
- Are there JavaScript errors in console?

### Strategy 5: Grep for Patterns

Common checks:
```bash
# Find all variable definitions
grep '^\$' file.pgml

# Find PGML blocks
grep -n 'BEGIN_PGML\|END_PGML' file.pgml

# Find answer rules
grep 'ANS\|ans_rule' file.pgml

# Check for problematic asterisks
grep '\*\[' file.pgml
```

---

## Prevention Checklist

Before committing a new PG file:

- [ ] Variables defined before use (check line numbers)
- [ ] No `*` or `**` immediately around `[$variables]` in PGML
- [ ] HTML variables use `[$var]*` syntax (with the asterisk)
- [ ] No Perl loops inside `BEGIN_TEXT...END_TEXT` blocks
- [ ] Hash keys sorted before random selection
- [ ] Shuffling happens AFTER all items are defined
- [ ] `ans_rule()` created BEFORE `ANS()` call
- [ ] SMILES strings validated with Python RDKit
- [ ] Tested with renderer (`-r` flag) to verify HTML output
- [ ] No PGML parsing errors in renderer warnings

---

## Quick Reference: Common Errors

| Error Message | Likely Cause | Fix |
|---------------|--------------|-----|
| `'*' was not closed` | Asterisks around variable in PGML | Remove `*` or use `**` (bold) |
| `'**' was not closed` | Bold markers around variable | Remove bold or move variable out |
| Empty output / no canvas | Variable used before defined | Move definition before usage |
| HTML shown literally | Missing `*` in `[$var]*` | Add asterisk: `[$var]*` |
| Answer always wrong | Answer field name mismatch | Use `ans_rule()` before `ANS()` |
| RadioButtons error | Wrong argument type | Check RadioButtons syntax |
| Random order changes | Hash keys not sorted | Sort keys before selection |

---

## Related Documentation

- [RANDOMIZATION_REFERENCE.md](RANDOMIZATION_REFERENCE.md) - Seeding and shuffling
- [RDKIT_MOLECULAR_STRUCTURES.md](RDKIT_MOLECULAR_STRUCTURES.md) - SMILES validation
- [QUESTION_STATEMENT_EMPHASIS.md](QUESTION_STATEMENT_EMPHASIS.md) - HTML in PGML
- [WEBWORK_PROBLEM_AUTHOR_GUIDE.md](WEBWORK_PROBLEM_AUTHOR_GUIDE.md) - Overall structure

---

## Contributing

Found a new pitfall? Add it here with:
- **Problem:** Clear description of the error
- **Symptom:** What you see when it fails
- **Fix:** Working code example
- **Why:** Explanation of the underlying issue
- **Example:** Reference to a file in this repo where it occurred
