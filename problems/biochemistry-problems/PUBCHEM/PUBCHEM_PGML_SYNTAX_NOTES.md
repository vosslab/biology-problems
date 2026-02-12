# PGML Syntax Notes for Dynamic Content

## The Problem with `>>...<<`

The `>>...<<` syntax in PGML is for **verbatim HTML** - it escapes the content rather than executing it. This means script tags get displayed as text instead of executing.

### What Doesn't Work
```perl
BEGIN_PGML

>>
<canvas id="[$canvas_id]" width="480" height="400"></canvas>
<script>initMolecule("[$canvas_id]", "[$mol_smiles]");</script>
<<

END_PGML
```

**Result**: The HTML is displayed as escaped text, not rendered.

## The Solution: Use `[@ @]*`

For dynamic HTML with JavaScript, use `[@ @]*` which **evaluates** the Perl expression and inserts the result as HTML.

### What Works
```perl
BEGIN_PGML

[@
"<canvas id='$canvas_id' width='480' height='400'></canvas>" .
"<script>initMolecule('$canvas_id', \"$mol_smiles_js\");</script>"
@]*

END_PGML
```

**Key points:**
- `[@ ... @]*` evaluates Perl code and returns HTML
- Use double quotes `"..."` for strings
- Use `.` to concatenate strings
- Use single quotes `'...'` inside HTML for attributes (avoids escaping)
- Escape double quotes inside strings with `\"`
- The `*` suffix prevents adding `<p>` tags around the output

## Alternative: Stick with BEGIN_TEXT

If PGML causes too many issues with dynamic content, use `BEGIN_TEXT` for that section:

```perl
BEGIN_TEXT
<p><canvas id="$canvas_id" width="480" height="400"></canvas></p>
<script>initMolecule("$canvas_id", "$mol_smiles_js");</script>
$PAR
END_TEXT

BEGIN_PGML
Which one of the four main types of macromolecules is represented by the chemical structure shown above?

[_]{$mc}
END_PGML
```

## PGML Syntax Quick Reference

| Syntax | Purpose | Use Case |
|--------|---------|----------|
| `[$var]` | Variable interpolation | Display Perl variables in text |
| `[_]{$obj}` | Answer blank | Create answer input with grading object |
| `[@ code @]*` | Evaluated expression | Return HTML from Perl code |
| `>>html<<` | Verbatim HTML | Static HTML (gets escaped, no scripts!) |
| `**bold**` | Markdown formatting | Text styling |
| `---` | Horizontal rule | Section dividers |

## Our Working Solution

```perl
# Setup: Escape SMILES for JavaScript
$mol_smiles_js = $mol_smiles;
$mol_smiles_js =~ s/\\/\\\\/g;  # Escape backslashes
$mol_smiles_js =~ s/"/\\"/g;    # Escape double quotes

BEGIN_PGML

## Identify the Macromolecule Type

Study the chemical structure below...

---

[@
"<canvas id='$canvas_id' width='480' height='400'></canvas>" .
"<script>initMolecule('$canvas_id', \"$mol_smiles_js\");</script>"
@]*

---

Which one of the four main types of macromolecules is represented?

[_]{$mc}

END_PGML
```

## Why This Works

1. **JavaScript escaping**: `$mol_smiles_js` has backslashes and quotes properly escaped
2. **String concatenation**: Multiple strings joined with `.`
3. **Evaluated output**: `[@ @]*` evaluates the Perl expression
4. **No extra paragraphs**: The `*` prevents PGML from wrapping in `<p>` tags
5. **Direct variable access**: Inside `[@ @]*`, use `$var` not `[$var]`

## Testing Checklist

- [ ] Canvas element appears (not as text)
- [ ] JavaScript console shows "RDKit version: ..."
- [ ] Molecule renders on canvas
- [ ] No JavaScript errors in console
- [ ] Answer buttons work correctly
