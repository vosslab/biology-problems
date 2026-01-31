# Question Statement Emphasis Strategies

This guide covers techniques for highlighting key phrases, data, and critical information in PGML question statements to improve readability and reduce student errors.

---

## Why Emphasize Key Information?

Students often miss critical details in question statements, leading to:
- Reading the wrong value (pH 7.4 instead of pH 8.0)
- Missing important qualifiers ("most", "least", "NOT")
- Overlooking units or conditions

**Visual emphasis helps students:**
- Quickly locate critical values
- Distinguish between similar questions
- Focus on what matters

---

## Core Technique: HTML Span with Inline CSS

### Basic Pattern

```perl
# In Setup section - create emphasis variable
$key_value_emph = "<span style='color:#0066cc;font-size:1.25em;font-weight:700;'>$variable</span>";

# In PGML - render with * to prevent HTML escaping
BEGIN_PGML
Question text with [$key_value_emph]* embedded.
END_PGML
```

**Key points:**
- Create span in Setup section (before PGML)
- Use single quotes for `style=` attribute (avoids escaping issues)
- Interpolate variables into the span
- Use `[$var]*` in PGML (the `*` prevents HTML escaping)

---

## Emphasis Styles by Use Case

### 1. Numeric Values (pH, concentrations, temperatures)

**Blue badge style** (recommended for pH values):

```perl
$ph_emph = "<span style='color:#0066cc;font-size:1.35em;font-weight:700;background-color:#e6f2ff;padding:0.1em 0.4em;border-radius:4px;'>pH $ph_value</span>";
```

**Example:**
- Color: Blue (#0066cc) - scientific/data association
- Background: Light blue (#e6f2ff) - creates visual badge
- Size: 1.35em - clearly larger than body text
- Padding + border-radius: Creates button-like appearance

**Use for:** pH values, temperatures, concentrations, counts

**Working example:** `problems/biochemistry-problems/histidine_protonation_states.pgml`

---

### 2. Key Terms (hydrophobic, NOT, LEAST, MOST)

**Gold/brown emphasis** (for qualitative terms):

```perl
$hydrophobic_emph = "<span style='color:#997300;font-size:1.25em;font-weight:700;'>hydrophobic</span>";
```

**Example:**
- Color: Gold/brown (#997300) - warm, attention-grabbing
- Size: 1.25em - noticeably larger
- No background - keeps focus on the word

**Use for:** Key adjectives, qualifiers, critical terms

**Working example:** `problems/biochemistry-problems/which_hydrophobic-simple.pgml`

---

### 3. Negation Terms (NOT, EXCEPT, CANNOT)

**Red emphasis** (for negations - use sparingly):

```perl
$not_emph = "<span style='color:#cc0000;font-size:1.3em;font-weight:700;text-transform:uppercase;'>NOT</span>";
```

**Example:**
- Color: Red (#cc0000) - warning color
- Size: 1.3em - larger to catch attention
- Transform: UPPERCASE - additional emphasis
- **Use sparingly** - too much red is alarming

**Use for:** NOT, EXCEPT, CANNOT, FALSE, INCORRECT

---

### 4. Multiple Values (pKa lists, sequences)

**Monospace with background:**

```perl
$pka_values = "<span style='font-family:monospace;background-color:#f5f5f5;padding:0.2em 0.5em;border-radius:3px;font-size:1.1em;'>1.82, 6.00, 9.17</span>";
```

**Example:**
- Font: Monospace - better for numeric alignment
- Background: Light gray (#f5f5f5) - subtle separation
- Size: 1.1em - slightly larger for readability

**Use for:** Lists of values, sequences, molecular formulas

---

## Color Palette Recommendations

### Data/Scientific Values
- **Blue:** `#0066cc` (primary data)
- **Cyan:** `#0099cc` (secondary data)
- **Navy:** `#003366` (strong emphasis)

### Qualitative Terms
- **Gold:** `#997300` (key terms like "hydrophobic")
- **Orange:** `#cc6600` (comparative terms like "most")
- **Brown:** `#663300` (descriptive terms)

### Warnings/Negations
- **Red:** `#cc0000` (NOT, EXCEPT - use sparingly!)
- **Dark red:** `#990000` (CANNOT, FALSE)

### Neutral Emphasis
- **Gray background:** `#f5f5f5` (subtle highlighting)
- **Light blue background:** `#e6f2ff` (data badges)
- **Light yellow background:** `#fff9e6` (gentle attention)

**Avoid:**
- Pure black (#000000) - too harsh
- Pure white (#ffffff) backgrounds - no contrast
- Bright green/yellow - accessibility issues
- More than 2-3 colors per question - visual clutter

---

## Font Size Guidelines

### Relative to Body Text (1em)

- **1.1em** - Subtle emphasis (formulas, lists)
- **1.25em** - Moderate emphasis (key terms)
- **1.35em** - Strong emphasis (pH values, critical data)
- **1.5em** - Maximum (rarely needed, only for warnings)

**Don't exceed 1.5em** - becomes distracting and looks unprofessional

---

## Complete Working Examples

### Example 1: pH-dependent Question

```perl
# Setup
$ph_value = 7.4;
$ph_emph = "<span style='color:#0066cc;font-size:1.35em;font-weight:700;background-color:#e6f2ff;padding:0.1em 0.4em;border-radius:4px;'>pH $ph_value</span>";

# PGML
BEGIN_PGML
Which amino acid is predominantly charged at [$ph_emph]*?

[_]{$answer}
END_PGML
```

**Result:** Blue badge with "pH 7.4" that clearly stands out

---

### Example 2: Negation Question

```perl
# Setup
$not_emph = "<span style='color:#cc0000;font-size:1.3em;font-weight:700;'>NOT</span>";

# PGML
BEGIN_PGML
Which of the following is [$not_emph]* a nucleotide?

[_]{$answer}
END_PGML
```

**Result:** Red "NOT" prevents students from missing the negation

---

### Example 3: Multiple Emphasized Elements

```perl
# Setup
$compound = "glucose";
$compound_emph = "<span style='color:#997300;font-size:1.25em;font-weight:700;'>$compound</span>";

$temp = "37°C";
$temp_emph = "<span style='color:#0066cc;font-size:1.25em;font-weight:700;background-color:#e6f2ff;padding:0.1em 0.3em;border-radius:3px;'>$temp</span>";

# PGML
BEGIN_PGML
At [$temp_emph]*, what is the solubility of [$compound_emph]* in water?

[_]{$answer} g/L
END_PGML
```

**Result:** Both temperature and compound are emphasized with appropriate styles

---

## Best Practices

### Do:
- ✅ Emphasize 1-3 key elements per question
- ✅ Use consistent colors for similar element types (blue for data, gold for terms)
- ✅ Test rendering to ensure spans display correctly
- ✅ Use meaningful color contrast (check accessibility)
- ✅ Create emphasis variables in Setup, not in PGML
- ✅ Use `[$var]*` syntax to render HTML in PGML

### Don't:
- ❌ Emphasize everything (defeats the purpose)
- ❌ Use more than 3 colors in one question
- ❌ Make text too large (>1.5em)
- ❌ Use red for non-warning content
- ❌ Forget the `*` in `[$var]*` (HTML will be escaped)
- ❌ Use italics/bold for critical values (use color + size instead)

---

## Accessibility Considerations

### Color Contrast

Ensure sufficient contrast between text and background:
- **Minimum:** 4.5:1 for normal text
- **Recommended:** 7:1 for important information

**Good combinations:**
- `#0066cc` text on white background (8.6:1 contrast)
- `#997300` text on white background (5.2:1 contrast)
- `#cc0000` text on white background (5.9:1 contrast)

### Multiple Emphasis Methods

Don't rely on color alone:
- Use size + color
- Use background + color
- Use weight + color

This helps colorblind users and screen readers.

---

## Common Patterns by Question Type

### Titration/pH Questions
```perl
$ph_emph = "<span style='color:#0066cc;font-size:1.35em;font-weight:700;background-color:#e6f2ff;padding:0.1em 0.4em;border-radius:4px;'>pH $ph</span>";
```

### Identify/Classify Questions
```perl
$term_emph = "<span style='color:#997300;font-size:1.25em;font-weight:700;'>$key_term</span>";
```

### Negation Questions
```perl
$not_emph = "<span style='color:#cc0000;font-size:1.3em;font-weight:700;'>NOT</span>";
```

### Concentration/Measurement Questions
```perl
$conc_emph = "<span style='font-family:monospace;background-color:#f5f5f5;padding:0.2em 0.5em;border-radius:3px;font-size:1.15em;'>$concentration</span>";
```

---

## Testing Your Emphasis

### Checklist:
- [ ] Emphasis stands out when scanning quickly
- [ ] Colors have sufficient contrast
- [ ] Not too many emphasized elements (max 3)
- [ ] HTML renders correctly (used `[$var]*` syntax)
- [ ] Text is readable (not too large, not too small)
- [ ] Style is consistent with similar questions

### Quick Test:
1. Render the question
2. Look away and then glance at it quickly
3. Does your eye immediately go to the emphasized element?
4. If no, increase emphasis; if it's overwhelming, reduce it

---

## PGML Syntax Reminder

### Correct:
```perl
# Setup
$emph = "<span style='color:blue;'>value</span>";

# PGML
[$emph]*    # The * prevents HTML escaping
```

### Incorrect:
```perl
# PGML
[$emph]     # NO * - HTML will be escaped and show as literal <span>
[$emph]**   # Double ** not needed, single * is correct
```

---

## Related Documentation

- [WEBWORK_PROBLEM_AUTHOR_GUIDE.md](WEBWORK_PROBLEM_AUTHOR_GUIDE.md) - Overall problem structure
- [PGML_QUESTION_TYPES.md](PGML_QUESTION_TYPES.md) - Question type patterns
- [COLOR_TEXT_IN_WEBWORK.md](COLOR_TEXT_IN_WEBWORK.md) - PGML color span handling

---

## Contribution Guidelines

When adding new emphasis patterns to problems:
- Document the pattern here with working example
- Add file reference to "Working examples" section
- Include color values in hex format
- Test accessibility contrast ratios
