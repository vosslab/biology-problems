#!/usr/bin/env python

from rdkit import Chem
from rdkit.Chem import AllChem, Draw
from rdkit.Chem.Draw import rdMolDraw2D
from PIL import Image
from io import BytesIO
import math

# Step 1: Build and rotate poly-alanine
def rotate_mol_180(mol):
    conf = mol.GetConformer()
    for i in range(mol.GetNumAtoms()):
        pos = conf.GetAtomPosition(i)
        conf.SetAtomPosition(i, (-pos.x, -pos.y, pos.z))

polyglycine = "[NH3+][C@@H]([H])(C(=O)N[C@@H]([H])(C(=O)N[C@@H]([H])(C(=O)N[C@@H]([H])(C(=O)N[C@@H]([H])(C(=O)[O-])))))"
mol = Chem.MolFromSmiles(polyglycine)

mol = Chem.MolFromSequence('G-G-G-G-G')

AllChem.Compute2DCoords(mol)
rotate_mol_180(mol)

# Step 2: Save to .mol file with coordinates
Chem.MolToMolFile(mol, "polyglycine_template.mol")

polyalanine = "[NH3+][C@@H](C)(C(=O)N[C@@H](C)(C(=O)N[C@@H](C)(C(=O)N[C@@H](C)(C(=O)N[C@@H](C)(C(=O)[O-])))))"
polyalanine = "[NH3+][CH](C)(C(=O)N[CH](C)(C(=O)N[CH](C)(C(=O)N[CH](C)(C(=O)N[CH](C)(C(=O)[O-])))))"
polyalanine = "N[C@@H](C)C(=O)N[C@@H](C)C(=O)N[C@@H](C)C(=O)N[C@@H](C)C(=O)N[C@@H](C)C(=O)O"
polyserine = "[NH3+][C@@H](CO)(C(=O)N[C@@H](CO)(C(=O)N[C@@H](CO)(C(=O)N[C@@H](CO)(C(=O)N[C@@H](CO)(C(=O)[O-])))))"
polythreonine = "[NH3+][C@@H]([C@H](O)C)(C(=O)N[C@@H]([C@H](O)C)(C(=O)N[C@@H]([C@H](O)C)(C(=O)N[C@@H]([C@H](O)C)(C(=O)N[C@@H]([C@H](O)C)(C(=O)[O-])))))"
polytrp = "[NH3+][C@@H](CC1=CC=C2C(=C1)C(=CN2))(C(=O)N[C@@H](CC1=CC=C2C(=C1)C(=CN2))(C(=O)N[C@@H](CC1=CC=C2C(=C1)C(=CN2))(C(=O)N[C@@H](CC1=CC=C2C(=C1)C(=CN2))(C(=O)N[C@@H](CC1=CC=C2C(=C1)C(=CN2))(C(=O)[O-])))))"
polyisoleucine = "[NH3+][C@@H]([C@H](CC)C)(C(=O)N[C@@H]([C@H](CC)C)(C(=O)N[C@@H]([C@H](CC)C)(C(=O)N[C@@H]([C@H](CC)C)(C(=O)N[C@@H]([C@H](CC)C)(C(=O)[O-])))))"

# 🔁 FIX: Read back the template
mol_from_file = Chem.MolFromMolFile("polyglycine_template.mol", removeHs=False)

# Step 3: Make serine molecule
#ser_mol = Chem.MolFromSmiles(polyisoleucine)
ser_mol = Chem.MolFromSequence('I-I-I-I-I')

AllChem.Compute2DCoords(ser_mol)

# Step 4: Align serine to glycine template
AllChem.GenerateDepictionMatching2DStructure(ser_mol, mol_from_file)

# Save aligned polyserine without hydrogens
Chem.MolToMolFile(ser_mol, "pentapeptide_wordle_template.mol")

# Draw aligned polyserine
drawer = rdMolDraw2D.MolDraw2DCairo(600, 300)
opts = drawer.drawOptions()
opts.explicitMethyl = True
opts.addAtomIndices = False

drawer.SetDrawOptions(opts)
drawer.DrawMolecule(ser_mol)
drawer.FinishDrawing()

img = Image.open(BytesIO(drawer.GetDrawingText()))
img.show()

