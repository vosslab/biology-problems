# RDKit.js Molecular Structure Rendering in PGML

This guide covers using RDKit.js to render chemical structures from SMILES strings in WeBWorK PGML problems.

---

## Why RDKit.js?

**Advantages over static images:**
- High-quality, consistent rendering across all molecules
- No image file management or hosting required
- SMILES strings are compact and easy to maintain
- Customizable rendering options (explicit hydrogens, stereochemistry, etc.)
- Students can't reverse-image-search for answers
- Same structure will render identically on any device

**Requirements:**
- Internet connection for CDN access
- Modern browser with JavaScript enabled
- WeBWorK server allows external script loading from CDN

---

## Quick Start: Basic Pattern

### 1) Define SMILES strings in Setup

```perl
# ----------------------------
# 2) Setup
# ----------------------------

# SMILES for L-alanine (neutral zwitterion)
$smiles_alanine = 'C[C@@H](C(=O)[O-])[NH3+]';

# Create canvas element
$canvas_alanine = '<canvas id="canvas_alanine" width="320" height="240" data-smiles="' . $smiles_alanine . '"></canvas>';
```

### 2) Load RDKit.js in HEADER_TEXT

```perl
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
			if (!smiles) {
				return;
			}
			const mol = RDKit.get_mol(smiles);
			const mdetails = {
				"legend": "",
				"explicitMethyl": true
			};
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
```

### 3) Display canvas in PGML

```perl
BEGIN_PGML
**Identify this amino acid:**

[$canvas_alanine]*

[_]{$answer}
END_PGML
```

**Key points:**
- Use `[$variable]*` syntax to render HTML variables in PGML
- The `*` tells PGML not to escape the HTML
- JavaScript automatically finds all `canvas[data-smiles]` elements and renders them

---

## SMILES String Basics

SMILES (Simplified Molecular Input Line Entry System) is a text notation for chemical structures.

### Basic SMILES syntax

- **Atoms:** C, N, O, S, P (uppercase for standard atoms)
- **Bonds:** Single bonds are implicit, `=` for double, `#` for triple
- **Branches:** Use parentheses `(...)` for side chains
- **Rings:** Use numbers to close rings (e.g., `C1CCCCC1` for cyclohexane)
- **Aromatic:** Lowercase letters (e.g., `c1ccccc1` for benzene)

### Stereochemistry

- **Chiral centers:** `[C@@H]` or `[C@H]` for tetrahedral chirality
- **Double bonds:** `/` and `\` for E/Z stereochemistry

### Example: L-Alanine

```
C[C@@H](C(=O)[O-])[NH3+]
```

Breaking it down:
- `C` - methyl group (CH3)
- `[C@@H]` - chiral carbon with specific stereochemistry
- `(C(=O)[O-])` - carboxylate group (COO-)
- `[NH3+]` - ammonium group (charged nitrogen)

---

## Charged Species: Critical for Biochemistry

### Formal Charges in SMILES

Use square brackets `[...]` for atoms with:
- Formal charges
- Explicit hydrogens
- Non-default valence

### Common ionizable groups in amino acids

| Group | Neutral | Charged | SMILES (neutral) | SMILES (charged) |
|-------|---------|---------|------------------|------------------|
| Carboxylic acid | COOH | COO- | `C(=O)O` | `C(=O)[O-]` |
| Amino group | NH2 | NH3+ | `N` | `[NH3+]` |
| Imidazole (His) | NH + N | NH + NH+ | `C1=CNC=C1` or `C1=CN=C([NH]1)` | `C1=C([NH]C=[NH+]1)` |
| Guanidinium (Arg) | | NH2+ | | `C(=N)(N)N` becomes `C(=[NH2+])(N)N` |
| Thiol (Cys) | SH | S- | `S` | `[S-]` |
| Phenol (Tyr) | OH | O- | `O` | `[O-]` |

### CRITICAL: Imidazole Ring Protonation

**Common mistake:** Using `NH2+` for protonated imidazole

**Correct forms:**

**Protonated imidazole (pH < 6.0):**
- Has **NH + NH+** (one hydrogen on each nitrogen)
- SMILES: `C1=C([NH]C=[NH+]1)` or similar
- NOT `NH2+` which implies two hydrogens on one nitrogen

**Neutral imidazole (pH > 6.0):**
- Has **NH + N** (one hydrogen on one nitrogen)
- SMILES: `C1=CN=C([NH]1)` or `C1=CNC=C1`

**Example: Histidine at different pH**

```perl
# Protonated (pH < 6): imidazole has NH and NH+
$his_protonated = 'C1=C([NH]C=[NH+]1)C[C@@H](C(=O)[O-])[NH3+]';

# Neutral (pH > 6): imidazole has NH and N
$his_neutral = 'C1=CN=C([NH]1)C[C@@H](C(=O)[O-])[NH3+]';
```

---

## Validating SMILES Strings

**Always validate SMILES before using in PGML!**

### Method 1: Python RDKit (recommended)

```python
from rdkit import Chem

smiles = "C[C@@H](C(=O)[O-])[NH3+]"
mol = Chem.MolFromSmiles(smiles)

if mol is None:
    print("ERROR: Invalid SMILES!")
else:
    print(f"Valid SMILES")
    print(f"Formula: {Chem.rdMolDescriptors.CalcMolFormula(mol)}")
    print(f"Charge: {Chem.GetFormalCharge(mol)}")
```

### Method 2: Online SMILES viewers

- [PubChem Sketcher](https://pubchem.ncbi.nlm.nih.gov/edit3/index.html)
- [ChemDraw Online](https://chemdrawdirect.perkinelmer.cloud/js/sample/index.html)

### Method 3: Test render in WebWork

Use the local renderer to preview:

```bash
python3 /path/to/webwork-pg-renderer/script/lint_pg_via_renderer_api.py -i yourfile.pgml -r > test.html
open test.html
```

---

## Canvas Sizing Guidelines

### Recommended sizes

```perl
# Single molecule display
width="320" height="240"  # Standard, fits most amino acids

# Large molecule (peptides, nucleotides)
width="480" height="320"  # 3:2 aspect ratio

# Very large molecule
width="640" height="480"  # For complex structures

# Compact display (multiple molecules in grid)
width="240" height="180"  # Smaller, for comparisons
```

### Aspect ratios

- **4:3** is recommended for most molecules
- **16:9** works well for elongated peptides
- **1:1** (square) can work but wastes space for most organic molecules

---

## Rendering Options (mdetails)

Customize how RDKit draws molecules:

```javascript
const mdetails = {
    "legend": "",                  // Text label below molecule
    "explicitMethyl": true,        // Show CH3 groups explicitly
    "addAtomIndices": false,       // Show atom numbers (debug)
    "addBondIndices": false,       // Show bond numbers (debug)
    "addStereoAnnotation": false,  // Show R/S labels
    "width": 320,                  // Override canvas width
    "height": 240                  // Override canvas height
};
```

### Common option combinations

**Production (students):**
```javascript
{
    "legend": "",
    "explicitMethyl": true
}
```

**Debug (development):**
```javascript
{
    "legend": "Debug view",
    "explicitMethyl": true,
    "addAtomIndices": true,
    "addBondIndices": true,
    "addStereoAnnotation": true
}
```

---

## Multiple Molecules in One Problem

### Pattern 1: Sequential display

```perl
# Setup
$smiles_ala = 'C[C@@H](C(=O)[O-])[NH3+]';
$smiles_gly = 'C(C(=O)[O-])[NH3+]';

$canvas_ala = '<canvas id="canvas_ala" width="320" height="240" data-smiles="' . $smiles_ala . '"></canvas>';
$canvas_gly = '<canvas id="canvas_gly" width="320" height="240" data-smiles="' . $smiles_gly . '"></canvas>';

# PGML
BEGIN_PGML
**Molecule A:**
[$canvas_ala]*

**Molecule B:**
[$canvas_gly]*

Which molecule is glycine? [_]{$answer}
END_PGML
```

### Pattern 2: Side-by-side with HTML wrapper

```perl
# Create side-by-side wrapper
$side_by_side = '<div style="display: flex; gap: 1em;">' .
                '<div>' . $canvas_ala . '<p>Molecule A</p></div>' .
                '<div>' . $canvas_gly . '<p>Molecule B</p></div>' .
                '</div>';

# PGML
BEGIN_PGML
Compare these molecules:

[$side_by_side]*

Which is glycine? [_]{$answer}
END_PGML
```

---

## Randomization with RDKit

### Pattern: Random molecule selection

```perl
# Setup
%amino_acids = (
    'alanine' => 'C[C@@H](C(=O)[O-])[NH3+]',
    'glycine' => 'C(C(=O)[O-])[NH3+]',
    'serine' => 'C([C@@H](C(=O)[O-])[NH3+])O',
);

# Sort keys before random selection for seed stability
@aa_names = sort keys %amino_acids;
$selected_name = list_random(@aa_names);
$selected_smiles = $amino_acids{$selected_name};

$canvas = '<canvas id="canvas_aa" width="320" height="240" data-smiles="' . $selected_smiles . '"></canvas>';

# PGML
BEGIN_PGML
Identify this amino acid:

[$canvas]*

[_]{$selected_name}
END_PGML
```

**Important:** Always sort hash keys before random selection to ensure the same seed produces the same result!

---

## Common Pitfalls and Solutions

### 1. Incorrect formal charges

**Wrong:**
```perl
$smiles = 'CC(C(=O)O)NH3+';  # Missing brackets around NH3+
```

**Right:**
```perl
$smiles = 'CC(C(=O)O)[NH3+]';  # Proper bracket notation
```

### 2. Imidazole protonation errors

**Wrong:**
```perl
$his_protonated = 'C1=C(N=C[NH2+]1)...';  # NH2+ is incorrect!
```

**Right:**
```perl
$his_protonated = 'C1=C([NH]C=[NH+]1)...';  # NH + NH+
```

### 3. Forgetting to escape quotes in SMILES

**Wrong:**
```perl
$canvas = "<canvas data-smiles="$smiles"></canvas>";  # Quote hell!
```

**Right:**
```perl
$canvas = '<canvas data-smiles="' . $smiles . '"></canvas>';  # Proper concatenation
```

### 4. Canvas ID collisions

**Wrong:**
```perl
# Multiple canvases with same ID
$canvas1 = '<canvas id="canvas" ...>';
$canvas2 = '<canvas id="canvas" ...>';  # Duplicate ID!
```

**Right:**
```perl
$canvas1 = '<canvas id="canvas_state1" ...>';
$canvas2 = '<canvas id="canvas_state2" ...>';  # Unique IDs
```

### 5. Not using `*` in PGML

**Wrong:**
```perl
BEGIN_PGML
[$canvas]  # Will escape the HTML!
END_PGML
```

**Right:**
```perl
BEGIN_PGML
[$canvas]*  # The * prevents HTML escaping
END_PGML
```

---

## Chemistry-Specific Guidelines

### Amino Acids

**Standard zwitterion (physiological pH):**
- Carboxylate: `C(=O)[O-]`
- Ammonium: `[NH3+]`
- Neutral side chain (unless ionizable)

**Examples:**

```perl
# L-Alanine (zwitterion)
$ala = 'C[C@@H](C(=O)[O-])[NH3+]';

# L-Lysine (zwitterion, charged side chain)
$lys = 'C(CCN)[C@@H](C(=O)[O-])[NH3+]';  # Wait, need charged lysine!
$lys = 'C(CC[NH3+])[C@@H](C(=O)[O-])[NH3+]';  # Corrected

# L-Aspartate (zwitterion, charged side chain)
$asp = 'C([C@@H](C(=O)[O-])[NH3+])C(=O)[O-]';

# L-Histidine (zwitterion, protonated side chain)
$his = 'C1=C([NH]C=[NH+]1)C[C@@H](C(=O)[O-])[NH3+]';
```

### Nucleotides/Nucleosides

**Bases are typically neutral or protonated:**

```perl
# Adenine (neutral)
$adenine = 'C1=NC(=C2C(=N1)N=CN2)N';

# Cytosine (neutral)
$cytosine = 'C1=CN(C(=O)N=C1N)C';  # With ribose attachment point
```

### Peptides

**Show peptide bonds:**

```perl
# Dipeptide: Gly-Ala
$gly_ala = 'C[C@@H](C(=O)O)NC(=O)CN';
```

---

## Working Examples in This Repository

### Basic examples

- `problems/biochemistry-problems/PUBCHEM/rdkit_working_in_webwork.pgml`
  - Minimal working example with two amino acids
  - Good starting template

### Intermediate examples

- `problems/biochemistry-problems/PUBCHEM/which_amino_acid.pgml`
  - Random amino acid selection
  - Single molecule identification

### Advanced examples

- `problems/biochemistry-problems/histidine_protonation_states.pgml`
  - Multiple charge states
  - pH-dependent protonation
  - Individual radio buttons per structure

- `problems/biochemistry-problems/PUBCHEM/polypeptide_mc_sequence-easy.pgml`
  - Peptide bond highlighting
  - Larger molecules

---

## Troubleshooting

### RDKit not loading

**Symptom:** Canvas elements show as empty boxes

**Check:**
1. CDN is accessible: Open browser console, look for network errors
2. JavaScript is enabled
3. HEADER_TEXT is in correct location (after loadMacros, before BEGIN_PGML)

### SMILES not rendering

**Symptom:** Console shows "Error initializing RDKit"

**Check:**
1. SMILES is valid (test with Python RDKit)
2. SMILES is properly escaped in canvas data attribute
3. Canvas has unique ID
4. `data-smiles` attribute is properly quoted

### Wrong structure appears

**Symptom:** Molecule renders but looks wrong

**Check:**
1. Stereochemistry symbols: `[C@@H]` vs `[C@H]`
2. Formal charges: `[NH3+]` vs `NH3`
3. Explicit hydrogens on charged atoms: `[NH+]` vs `[N+]`
4. Ring closures: numbers match correctly

---

## Additional Resources

### SMILES references

- [Daylight SMILES Theory](http://www.daylight.com/dayhtml/doc/theory/theory.smiles.html)
- [OpenSMILES Specification](http://opensmiles.org/opensmiles.html)
- [PubChem SMILES Guidelines](https://pubchemdocs.ncbi.nlm.nih.gov/smiles)

### RDKit.js documentation

- [RDKit.js GitHub](https://github.com/rdkit/rdkit/tree/master/Code/MinimalLib)
- [RDKit.js npm package](https://www.npmjs.com/package/@rdkit/rdkit)

### Validation tools

- [PubChem Structure Search](https://pubchem.ncbi.nlm.nih.gov/)
- [ChemSpider](http://www.chemspider.com/)
- Python RDKit: `pip install rdkit`

---

## Best Practices Checklist

Before publishing a problem with RDKit:

- [ ] All SMILES validated with Python RDKit or online tool
- [ ] Formal charges correct (especially `[NH3+]`, `[O-]`, `[NH+]`)
- [ ] Canvas IDs are unique across all molecules
- [ ] Canvas sizes appropriate for molecule complexity
- [ ] Rendering tested in local renderer with `-r` flag
- [ ] Random selection uses sorted keys for seed stability
- [ ] Solution explains chemistry (especially charge states)
- [ ] Stereochemistry is correct for chiral molecules
- [ ] Variables use `*` in PGML for HTML rendering

---

## License Note

When using RDKit.js from the CDN, you are using software licensed under BSD-3-Clause. The educational content and PGML code in this repository remain under CC BY 4.0 / LGPLv3 as specified in the repository license.
