# PGML Question Type Patterns

This guide describes the preferred PGML style for common question types in this
repo. It complements [WEBWORK_PROBLEM_AUTHOR_GUIDE.md](WEBWORK_PROBLEM_AUTHOR_GUIDE.md)
and [MATCHING_PROBLEMS.md](MATCHING_PROBLEMS.md).

## General rules (all question types)

- PGML-first: put student-facing text and blanks inside `BEGIN_PGML ... END_PGML`.
- File extensions: use `.pgml` only for full PGML-first problems; use `.pg` when
  legacy `ANS(...)` or mixed PG/PGML structure is required.
- Inline graders: attach the answer evaluator in the PGML blank (for example
  `[_]{$rb}` or `[__________]{$ans}`), not via a separate `ANS(...)` call.
- Use `MODES(...)` only when HTML must be emitted from Perl or PGML would escape
  or misparse it. Do not wrap plain text in `MODES(...)`.
- If you must pass HTML stored in a Perl variable into PGML, render it with
  `[$var]*` so PGML does not escape it.

## Multiple choice (RadioButtons)

Use `RadioButtons` with `parserRadioButtons.pl` and inline it in PGML.

```perl
loadMacros(
  "PGstandard.pl",
  "PGML.pl",
  "parserRadioButtons.pl",
  "PGcourse.pl",
);

$rb = RadioButtons(
  [ [ 'Red', 'Blue', 'Green' ], 'None of these' ],
  'Blue',
  labels        => 'ABC',
  displayLabels => 1,
  randomize     => 0,
);

BEGIN_PGML
My favorite color is

[_]{$rb}
END_PGML
```

Notes:
- Use `labels => 'ABC'` for consistent labeling.
- Keep `randomize => 0` unless you are safely randomizing and mapping the
  correct answer.
- For horizontal options, use a separator (for example `separator => $SPACE x 5`)
  or HTML spacing via `separator => '<div ...>'`.

## Multiple answer (checkbox)

Checkbox macros are unreliable in our PG 2.17 renderer snapshot. Avoid
checkboxes unless you have verified the macro exists in
[PG_2_17_RENDERER_MACROS.md](PG_2_17_RENDERER_MACROS.md) and tested rendering.

Preferred fallback patterns:
- Use multiple `RadioButtons` or `PopUp` widgets, one per statement.
- Convert to multiple choice if the learning goal allows it.

If checkboxes are confirmed available, keep the same PGML-first pattern and
inline the evaluator in the blank.

## Fill-in-blank (string)

Use a string MathObject only if the string context is available in the renderer.
If it is not available, convert the question to multiple choice or PopUp.

```perl
# If Context("String") or Context("LimitedString") is available:
Context("String");
$ans = Compute("blue");

BEGIN_PGML
Enter the color: [__________]{$ans}
END_PGML
```

## Numerical with tolerance

Use a numeric MathObject with explicit tolerance settings.

```perl
Context("Numeric");
$ans = Compute("3.2")->with(tolType => "absolute", tolerance => 0.1);

BEGIN_PGML
Enter the value: [__________]{$ans}
END_PGML
```

Notes:
- State the tolerance policy in the prompt when it matters.
- If units are required, use a units-aware evaluator and verify the macro is
  available in the renderer snapshot.

## Matching

Follow [MATCHING_PROBLEMS.md](MATCHING_PROBLEMS.md): use `PopUp` widgets and
HTML layout wrappers with `MODES(...)` when the HTML must be emitted from Perl.
PGML should render the layout and the PopUps inline.

```perl
loadMacros(
  "PGstandard.pl",
  "PGML.pl",
  "parserPopUp.pl",
  "PGcourse.pl",
);

$popup = PopUp([ 'A', 'B', 'C' ], 'B');

BEGIN_PGML
1. Prompt text [_]{$popup}
END_PGML
```

Notes:
- Keep matching layout HTML-only.
- Use the label and ordering rules in MATCHING_PROBLEMS.md.

## Ordering (DraggableProof)

Use `draggableProof.pl` and emit the widget HTML from Perl, then inject it into
PGML with `[$var]*`. The inline `[_]{$ordering}` pattern is not supported by the
current PG 2.17 renderer in this repo (it errors with an unrecognized evaluator),
so use the legacy `->Print` + `ANS(...)` form here.

```perl
loadMacros(
  "PGstandard.pl",
  "MathObjects.pl",
  "PGML.pl",
  "draggableProof.pl",
  "PGcourse.pl",
);

$ordering = DraggableProof(
  [ "Option 1", "Option 2", "Option 3" ],
  [],
  SourceLabel => "Options",
  TargetLabel => "Rank in order of increasing property",
);
$ordering_html = $ordering->Print;
BEGIN_PGML
Arrange the options in order.

[$ordering_html]*
END_PGML

ANS($ordering->cmp);
```

Notes:
- Keep the correct order in the first list; the second list holds items that
  should start in the target (usually empty).
- Include `MathObjects.pl`; it is required by the macro.
- See [ORDERING_PROBLEMS.md](ORDERING_PROBLEMS.md) for full guidance.

## Multipart (mixed formats or repeated formats)

Define each answer object separately and attach them inline in PGML. Keep each
blank close to its prompt. Avoid relying on implicit `ANS(...)` ordering.

```perl
Context("Numeric");
$a = Compute("2");
$b = Compute("5");

BEGIN_PGML
Part A: [__________]{$a}

Part B: [__________]{$b}
END_PGML
```

Notes:
- For mixed formats (for example radio + numeric), define and place each blank
  near its text.
- If repeated formats are used, keep naming consistent (`$ans1`, `$ans2`, etc.).

## Molecular structures (RDKit.js)

Use RDKit.js to render chemical structures from SMILES strings without requiring
image files. This pattern is preferred for biochemistry and organic chemistry
questions involving molecular visualization.

```perl
loadMacros(
  "PGstandard.pl",
  "PGML.pl",
  "parserRadioButtons.pl",
  "PGcourse.pl",
);

# ----------------------------
# 2) Setup
# ----------------------------

# Define SMILES for L-alanine (zwitterion)
$smiles_alanine = 'C[C@@H](C(=O)[O-])[NH3+]';

# Create canvas element with data-smiles attribute
$canvas = '<canvas id="canvas_alanine" width="320" height="240" data-smiles="' . $smiles_alanine . '"></canvas>';

# Create answer widget
$answer = RadioButtons(
  ['Alanine', 'Glycine', 'Serine', 'Valine'],
  'Alanine',
  labels => 'ABC',
  displayLabels => 1,
);

# ----------------------------
# 2) Header - Load RDKit.js
# ----------------------------

HEADER_TEXT(<<'END_HEADER');
<script src="https://unpkg.com/@rdkit/rdkit/dist/RDKit_minimal.js"></script>
<script>
let RDKitReady = null;
function getRDKit() {
	if (!RDKitReady) {
		RDKitReady = initRDKitModule();
	}
	return RDKitReady;
}
function initMoleculeCanvases() {
	getRDKit().then(function(RDKit) {
		const canvases = document.querySelectorAll('canvas[data-smiles]');
		canvases.forEach((canvas) => {
			const smiles = canvas.dataset.smiles;
			if (!smiles) return;
			const mol = RDKit.get_mol(smiles);
			const mdetails = {"legend": "", "explicitMethyl": true};
			if (canvas && mol) {
				mol.draw_to_canvas_with_highlights(canvas, JSON.stringify(mdetails));
				mol.delete();
			}
		});
	}).catch(error => {
		console.error('Error initializing RDKit:', error);
	});
}
if (document.readyState === 'loading') {
	document.addEventListener('DOMContentLoaded', initMoleculeCanvases);
} else {
	initMoleculeCanvases();
}
</script>
END_HEADER

# ----------------------------
# 3) Statement (PGML)
# ----------------------------

BEGIN_PGML
**Identify this amino acid:**

[$canvas]*

[_]{$answer}
END_PGML
```

Notes:
- Use `[$canvas]*` to render HTML without escaping (the `*` is critical).
- Each canvas must have a unique `id` attribute.
- SMILES strings must be valid and properly escaped in the data attribute.
- Always validate SMILES with Python RDKit or online tools before use.
- For charged species, use square brackets: `[NH3+]`, `[O-]`, `[NH+]`, etc.
- **Critical for imidazole:** Protonated form is `NH + NH+`, NOT `NH2+`.

### Working examples in this repository

- **Basic:** `problems/biochemistry-problems/PUBCHEM/rdkit_working_in_webwork.pgml`
  - Minimal working example, good starting template

- **Intermediate:** `problems/biochemistry-problems/PUBCHEM/which_amino_acid.pgml`
  - Random molecule selection from database

- **Advanced:** `problems/biochemistry-problems/histidine_protonation_states.pgml`
  - Multiple charge states, pH-dependent protonation

### Detailed guide

See [RDKIT_MOLECULAR_STRUCTURES.md](RDKIT_MOLECULAR_STRUCTURES.md) for:
- SMILES syntax reference
- Charged species notation (amino acids, nucleotides)
- Common chemistry pitfalls (especially imidazole protonation)
- Validation workflow
- Troubleshooting rendering issues
