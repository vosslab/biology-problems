# Macromolecule Identification PGML Question

This directory contains the tooling to generate a self-contained WeBWorK PGML question file for teaching students to identify macromolecule types from chemical structures.

## Overview

The generated question:
- Shows students a dynamically-rendered chemical structure (via RDKit.js)
- Asks them to identify which of the four macromolecule types it represents:
  - Carbohydrates (monosaccharides)
  - Lipids (fatty acids)
  - Proteins (amino acids and dipeptides)
  - Nucleic acids (nucleobases)
- Randomly selects from 358 molecules across all four categories
- Includes molecular formula and weight information
- Provides hints for identifying each macromolecule type

## Related guides

- `README_PUBCHEM_BPTOOLS.md` for Python/bptools Blackboard generators in this folder.

## Files

- **`generate_macromolecule_id_pgml.py`**: Python script that generates the PG file
- **`macromolecule_identification.pg`**: Generated WeBWorK problem file (66KB)
- **`macromolecules.yml`**: Source data - molecule names organized by type
- **`../../../data/pubchem_molecules_data.yml`**: Source data - molecule details (SMILES, formulas, etc.)
- **`rdkit_working_in_webwork.pg`**: Working prototype demonstrating RDKit.js in WeBWorK

## Generated File Statistics

- **Total molecules**: 358
- **Breakdown**:
  - Proteins: 113 molecules
  - Carbohydrates: 124 molecules
  - Lipids: 66 molecules
  - Nucleic acids: 55 molecules
- **File size**: ~26KB (self-contained, SMILES only)

## Editing the Question

**For most changes**: Edit `macromolecule_identification.pg` directly.

**Only regenerate if**: You're adding/removing many molecules from the YAML files.

```bash
cd /Users/vosslab/nsh/biology-problems/problems/biochemistry-problems/PUBCHEM
python3 generate_macromolecule_id_pgml.py
```

The generator script was primarily a one-time data conversion tool.

## Technical Details

### Embedded Data Structure

The PG file uses simple Perl arrays organized by macromolecule type:
```perl
@proteins = (
    'C[C@@H](C(=O)O)N',            # alanine SMILES
    'C(C[C@@H](C(=O)O)N)CN=C(N)N', # arginine SMILES
    # ... 111 more
);

@lipids = ( ... );
@carbohydrates = ( ... );
@nucleic_acids = ( ... );
```

This is much more efficient than storing names, formulas, and weights that the question doesn't use.

### RDKit.js Integration

The question uses RDKit.js for dynamic molecular rendering:
- Loads from CDN: `https://unpkg.com/@rdkit/rdkit/dist/RDKit_minimal.js`
- Renders SMILES strings to canvas elements
- Each student sees the same structure (controlled by problem seed)

### Features

1. **Randomization**: Each problem seed selects a different molecule
2. **Radio buttons**: WeBWorK's standard `RadioButtons` with randomized order
3. **Hints**: Built-in guide for identifying macromolecule types
4. **Clean output**: No anti-cheating hacks (WeBWorK provides its own security)
5. **PGML-first**: Uses modern PGML syntax throughout

### ADAPT Integration

For use in ADAPT (LibreTexts):
- The hint section can be replaced with ADAPT's hint system
- The basic structure is compatible with ADAPT's WeBWorK integration
- RDKit.js should work in ADAPT's iframe-based problem rendering

## Design Decisions

### Why Embed Data?

**Constraint**: Cannot add custom Perl modules to WeBWorK servers

**Solution**: Embed all molecule data directly in the PG file
- Makes file larger (~66KB) but self-contained
- No external dependencies (except RDKit.js CDN)
- Easier to distribute and use

### Why RDKit.js Instead of Static Images?

**Advantages**:
- Higher quality rendering than PubChem static images
- Consistent visual style across all molecules
- Can customize rendering options (explicit methyl groups, etc.)
- Students can't right-click to get image URLs

**Requirements**:
- Internet connection for CDN access
- Modern browser with JavaScript enabled
- Working prototype confirmed this approach works in WeBWorK

### Data Efficiency

Only the absolute minimum is embedded:
- **SMILES strings**: Required for RDKit.js rendering
- **Implicit type**: Determined by which array the SMILES is in
- **Excluded**: Names, formulas, weights, CID, partition coefficient, metadata

This reduces file size by 60% compared to storing full molecule details.

## Comparison to Original Python Generator

### Original (`which_macromolecule.py`)
- Generates BlackBoard-formatted text files
- Includes elaborate anti-cheating features (disabled copy/paste, hidden terms)
- Complex HTML styling with colored guide table in every question
- Outputs static question files

### PGML Version (`macromolecule_identification.pg`)
- Generates WeBWorK problems with automatic grading
- No anti-cheating hacks (WeBWorK handles security)
- Simplified styling, guide moved to hints
- Dynamic question generation per student seed

## Future Enhancements

Possible improvements:
1. Add solution explanations specific to each molecule type
2. Include structural feature highlighting (e.g., circle the amino group)
3. Create difficulty levels (easy: amino acids, hard: complex lipids)
4. Add more molecule information (biological function, occurrence)
5. Generate separate PG files for each macromolecule type

## Testing

To test the generated PG file:
1. Upload to a WeBWorK course
2. Or test locally using the renderer from `OTHER_REPOS-do_not_commit/webwork-pg-renderer`
3. Or use the PGML linter from `OTHER_REPOS-do_not_commit/webwork-pgml-linter`

## License

This follows the biology-problems repository licensing:
- Code: GPLv3
- Educational content: CC BY-SA 4.0
