# Color Text in WeBWorK (PGML)

## Summary
In our WeBWorK setup, CSS styling via PGML tag wrappers works reliably, while MathJax or TeX color commands do not reliably render (especially when TeX is injected through variables).

Use PGML tag wrappers to emit `span` tags with either a CSS class (preferred) or an inline style.

## What works
### 1) PGML tag wrapper + CSS class (preferred)
Define CSS once using `HEADER_TEXT`:

```perl
HEADER_TEXT(MODES(TeX => '', HTML => <<'END_STYLE'));
<style>
.css-magenta { color:#cc00cc; font-weight:700; }
.css-green   { color:#009900; font-weight:700; }
</style>
END_STYLE
```

Then in PGML:

```text
[<CSS class magenta>]{['span', class => 'css-magenta']}{['','']}
[<CSS class green>]{['span', class => 'css-green']}{['','']}
```

### 2) PGML tag wrapper + inline style (works, but less maintainable)

```text
[<Inline style green>]{['span', style => 'color:#009900;font-weight:700;']}{['','']}
```

## What does not work (in our setup)

MathJax or TeX color commands in PGML text do not render as colored text. They appear as plain text, or the backslashes are wrapped in tex2jax_ignore spans and never processed by MathJax.

Examples that failed:
- `[\color{#cc00cc}{\text{...}}]`
- `\(\color{#cc00cc}{\text{...}}\)`
- Injecting TeX color strings via variables such as `[$var_tex]`

Observed behavior in HTML output:
- Backslashes are escaped into `<span class="tex2jax_ignore">\\</span>`.
- MathJax never sees the TeX, so no color is applied.

## Recommendation

Use CSS coloring, not MathJax coloring.
- Treat PGML as the markup layer and use its tag wrapper feature to emit safe HTML.
- Prefer CSS classes over inline styles.
- Put style definitions in `HEADER_TEXT` (HTML mode) at the top of the problem.

## Recommended pattern for matching problems

For right-column choice labels that need color:
1. Decide a stable class name per label (generator rule or author choice).
2. Print the label using a PGML tag wrapper:

```perl
# Example: $bond is the plain label, $cls is something like 'choice-covalent'
"[<[$bond]>]{['span', class => '$cls']}{['','']}"
```

3. Define CSS once:

```css
.choice-covalent { color:#cc00cc; font-weight:700; }
.choice-ionic    { color:#009900; font-weight:700; }
.choice-hbond    { color:#e60000; font-weight:700; }

## Fixed label colors in matching problems (working solution)

When label colors must be fixed by meaning (not by position), build an HTML
mapping in Perl and emit the labels with `*` so PGML does not escape the spans.

Pattern:

```perl
# Label -> HTML mapping (fixed colors by meaning)
%answer_html = (
  'polar covalent bond' => '<span style="color: #00b3b3; font-weight:700;">polar covalent bond</span>',
  'non-polar covalent bond' => '<span style="color: #b3b300; font-weight:700;">non-polar covalent bond</span>',
  'ionic bond' => '<span style="color: #009900; font-weight:700;">ionic bond</span>',
  'hydrogen bond' => '<span style="color: #e60000; font-weight:700;">hydrogen bond</span>',
);
@answers_html = map { $answer_html{$_} || $_ } @answers;
```

Then in the right-column PGML list:

```perl
[@ join(
  "\n\n",
  map {
    '*' . $ALPHABET[($_)] . '.* ' . '[$answers_html[$shuffle[' . $_ . ']]]*'
  } 0 .. $#answers
) @]**
```

Notes:
- The trailing `*` is required; it tells PGML to pass through the HTML rather
  than escape it.
- This keeps colors tied to the label text even when the order is randomized.
```

## Notes
- Use `A)` instead of `A.` in rendered lists when PGML auto-converts `A.` into an ordered list.
- The warning "unknown block type 'balance'" may appear in PGML logs; it did not affect CSS-based coloring in our tests.
