#!/usr/bin/env python

from rdkit import Chem
from rdkit.Chem import AllChem, Draw
from rdkit.Chem.AllChem import GenerateDepictionMatching2DStructure

# Step 1: Template mol (extended backbone, e.g. polyglycine)
template = Chem.MolFromSequence('G-G-G-G-G')
AllChem.Compute2DCoords(template)  # Fix layout

# Step 2: Input peptide SMILES
smiles = "N[C@@H](C)C(=O)N[C@@H](C)C(=O)N[C@@H](C)C(=O)N[C@@H](C)C(=O)N[C@@H](C)C(=O)O"
mol = Chem.MolFromSmiles(smiles)
mol = Chem.AddHs(mol)

# Generate 2D layout that matches the template
GenerateDepictionMatching2DStructure(mol, template)

# Step 3: Draw molecule
img = Draw.MolToImage(mol, size=(600,300))
img.show()
