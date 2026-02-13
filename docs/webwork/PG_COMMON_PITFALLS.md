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

## Variable Scoping

### Pitfall: Using `my` on Variables Referenced in PGML

**Problem:** Declaring a variable with `my` makes it a Perl lexical variable, invisible to PGML's `[_]{$var}` and `[$var]` interpolation. PGML resolves variables in the package symbol table (the Safe compartment's namespace), not the lexical scope.

```perl
# WRONG - lexical variable invisible to PGML
my $radio = RadioButtons(['Alpha', 'Beta'], 'Alpha', labels => 'AB');

BEGIN_PGML
[_]{$radio}
END_PGML
# Result: renders as a plain text input, grading fails with
# "Error in Translator.pm::process_answers" and "HASH is not defined"
```

**Symptom:** RadioButtons (or any widget) renders as a bare text input `<input type=text>` instead of the expected radio list / dropdown / checkbox. Grading fails with `Answer evaluator was not executed due to errors`.

**Fix:** Remove `my` so the variable is a package variable.

```perl
# RIGHT - package variable visible to PGML
$radio = RadioButtons(['Alpha', 'Beta'], 'Alpha', labels => 'AB');

BEGIN_PGML
[_]{$radio}
END_PGML
# Result: renders as radio buttons, grading works
```

**The rule:** Any variable referenced inside `BEGIN_PGML ... END_PGML` (via `[_]{$var}`, `[$var]`, or `[$var]*`) **must be a package variable** (no `my`). Using `my` for intermediate helpers (RNG objects, loop counters, temporary arrays) is fine as long as those variables are never referenced in PGML.

```perl
# OK - my for intermediates, package var for PGML-visible results
my $local_random = PGrandom->new();
my $idx = $local_random->random(0, 3, 1);
$rb = RadioButtons([@choices], $choices[$idx], labels => 'ABC');
```

**Why this happens:** PG evaluates problem source inside a `Safe` compartment. The PGML parser uses Perl's symbol table lookup (`${$package . '::' . $varname}`) to resolve variables, which only finds package-scoped variables. Lexical `my` variables live on the Perl pad stack and are unreachable from this lookup path.

**Examples from this repo (all correct -- no `my` on PGML-visible vars):**
- `which_hydrophobic-simple.pgml`: `$rb = RadioButtons(...)`
- `chemical_group_pka_forms.pgml`: `$form_radio = RadioButtons(...)`
- `titration_pI.pgml`: `$rb_neutral = RadioButtons(...)`

---

### Pitfall: `\@` and `\%` References Are Broken -- Use `~~@` or `[...]`

**Problem:** The standard Perl backslash reference operators (`\@array`, `\%hash`) produce unusable references inside the Safe compartment. Dereferencing them with `@$ref` or `$ref->{key}` fails with "Not an ARRAY/HASH reference".

```perl
# WRONG - \@ produces a broken reference in PG
@choices = ('Alpha', 'Beta', 'Gamma');
$ref = \@choices;
$count = scalar(@$ref);   # Dies: "Not an ARRAY reference"

# WRONG - same issue with RadioButtons
$rb = RadioButtons(\@choices, 'Alpha');  # Dies
```

**Symptom:** `Not an ARRAY reference` or `Not a HASH reference` error at the line where the reference is dereferenced or passed to a function.

**Fix:** Use PG's `~~` (double-tilde) operator for references, or use `[...]`/`{...}` to create anonymous copies.

```perl
# Option 1: ~~@ creates a Safe-compatible array reference
$rb = RadioButtons(~~@choices, 'Alpha', labels => 'ABC');

# Option 2: [...] creates an anonymous array copy (most common in this repo)
$rb = RadioButtons([@choices], 'Alpha', labels => 'ABC');

# Option 3: For hash references, use ~~% or {...}
$href = ~~%data;      # Safe-compatible hash ref
$href = {%data};      # Anonymous hash copy
```

**Why this happens:** PG's Safe compartment overrides the backslash operator. The `\` opcode is restricted, so `\@array` does not produce a normal Perl array reference. The `~~` operator is PG's replacement that works within the sandbox. The `[...]` anonymous constructor also works because it uses a different opcode path.

**Recommendation:** Prefer `[@array]` for clarity; use `~~@array` when you need to avoid copying (rare in problem files).

---

### Pitfall: `use` Is Trapped -- Use `loadMacros` Instead

**Problem:** Perl's `use` statement calls `require` internally, which is blocked by the Safe compartment's operation mask.

```perl
# WRONG - trapped in PG
use POSIX qw(floor);
use List::Util qw(shuffle);
```

**Symptom:** `'require' trapped by operation mask`

**Fix:** Use PG's `loadMacros()` for PG macros, or find PG-native alternatives for standard library functions.

```perl
# RIGHT - load PG macros
loadMacros('PGstandard.pl', 'PGML.pl', 'parserRadioButtons.pl');

# For math functions, PG provides built-ins:
$val = int(3.7);              # truncate (built-in)
$val = sprintf("%.0f", 3.7);  # round via formatting

# For shuffling, PG provides random() and manual shuffle:
@temp = @items;
@shuffled = ();
while (@temp) {
  $i = random(0, $#temp, 1);
  push @shuffled, splice(@temp, $i, 1);
}
```

**Also trapped:** `eval "string"`, `open()`, `close()`, backtick execution (`` `cmd` ``), `system()`, `exec()`. These are all blocked for security -- PG problems run on shared servers and must not access the filesystem or execute shell commands.

---

### Pitfall: `local` Works But `my` Does Not in PGML

**Problem:** Authors who know that `my` is "more modern" than `local` may avoid `local` entirely. But in PG, `local` and `my` have critically different PGML visibility.

```perl
# WORKS - local modifies the package variable dynamically
local $greeting = "Hello from local";

# FAILS - my creates a lexical variable invisible to PGML
my $greeting = "Hello from my";

BEGIN_PGML
[$greeting]
END_PGML
# With local: displays "Hello from local"
# With my: displays nothing (empty string)
```

**Why:** `local` temporarily modifies a **package** variable (it stays in the symbol table), so PGML can find it. `my` creates a **lexical** variable on the pad stack, invisible to symbol-table lookups. For PG problems, the simplest approach is to use bare package variables (no `my`, no `local`) for anything PGML needs to see.

**When to use each:**

| Keyword | PGML visible? | Use for |
|---------|--------------|---------|
| `$var = ...` (bare) | Yes | Variables displayed or graded in PGML |
| `local $var = ...` | Yes | Temporary override of a package variable inside a block |
| `my $var = ...` | No | Helper variables, loop counters, RNG objects, temporary computation |

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
- [ ] No `my` on variables referenced in PGML (`$rb`, `$popup`, display vars)
- [ ] No `\@` or `\%` references -- use `~~@`, `[@array]`, `~~%`, or `{%hash}`
- [ ] No `use` statements -- use `loadMacros()` for PG macros
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
| RadioButtons renders as text input | `my $rb = RadioButtons(...)` | Remove `my`: `$rb = RadioButtons(...)` |
| `Not an ARRAY reference` | `\@array` backslash ref in PG | Use `~~@array` or `[@array]` |
| `Not a HASH reference` | `\%hash` backslash ref in PG | Use `~~%hash` or `{%hash}` |
| `'require' trapped by operation mask` | `use Module` in PG source | Use `loadMacros()` or PG built-ins |
| `'eval "string"' trapped` | `eval $code` in PG | Restructure to avoid string eval |
| `'open' trapped by operation mask` | File I/O in PG | Not possible; use PG data macros |
| Variable shows empty in PGML | `my $var` instead of `$var` | Remove `my` for PGML-visible vars |
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
