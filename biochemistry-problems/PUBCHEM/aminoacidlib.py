#!/usr/bin/env python3

zwitterion_amino_acid = '[NH3+][C@@H]R1(C(=O)[O-])'
neutral_amino_acid = 'N[C@@H]R1(C(=O)O)'
amino_acid = zwitterion_amino_acid
rdkit_js_url = "https://unpkg.com/@rdkit/rdkit/dist/RDKit_minimal.js"

glycine = '[NH3+][C@@H](C(=O)[O-])'
alanine = '[NH3+][C@@H](C)(C(=O)[O-])'

dipeptide = '[NH3+][C@@H]R1(C(=O)N[C@@H]R2(C(=O)[O-]))'
tripeptide = '[NH3+][C@@H]R1(C(=O)N[C@@H]R2(C(=O)N[C@@H]R3(C(=O)[O-])))'
tetrapeptide = '[NH3+][C@@H]R1(C(=O)N[C@@H]R2(C(=O)N[C@@H]R3(C(=O)N[C@@H]R4(C(=O)[O-]))))'
pentapeptide = '[NH3+][C@@H]R1(C(=O)N[C@@H]R2(C(=O)N[C@@H]R3(C(=O)N[C@@H]R4(C(=O)N[C@@H]R5(C(=O)[O-])))))'

def make_poly_peptide(length=5):
	amino_terminal_end = '[NH3+][C@@H]'
	carboxyl_terminal_end = '(C(=O)[O-])'
	peptide_bond = '(C(=O)N)[C@@H]'
	# make chain
	peptide_chain = ''
	peptide_chain += amino_terminal_end
	for i in range(length):
		peptide_chain += f'R{i+1}'
		if i+1 < length:
			peptide_chain += peptide_bond
	peptide_chain += carboxyl_terminal_end
	for i in range(length-1):
		peptide_chain += ')'
	return peptide_chain


side_chains = {
	#smallest
	'gly': '([H])',         # Glycine
	'gly2': '',         # Glycine
	'ala': '(C)',       # Alanine

	#polar
	'ser': '(CO)',        # Serine
	'thr': '([C@H](O)C)',    # Threonine
	#'allo-thr': '([C@@H](O)C)', # AlloThreonine
	'asn': '(CC(=O)N)',    # Asparagine
	'gln': '(CCC(=O)N)',    # Glutamine
	#negative charge
	'asp': '(CC(=O)[O-])',    # Aspartate
	'glu': '(CCC(=O)[O-])',    # Glutamate
	#positive charge
	'lys': '(CCCC[NH3+])',        # Lysine
	'arg': '(CCCNC(=[NH2+])N)',  # Arginine
	'his': '(CC1=C[NH]C=N1)',      # Histidine delta tautomer at pH 7
	'his2': '(CC1=CN=C[NH]1)',     # Histidine epsilon tautomer at pH 7
	'his3': '(CC1=C[NH]C=[NH+]1)', # Histidine delta tautomer at pH 5
	'his4': '(CC1=C[NH+]=C[NH]1)', # Histidine epsilon tautomer at pH 5
	#branch chain
	'val': '(C(C)C)',       # Valine
	'leu': '(CC(C)C)',    # Leucine
	'ile': '([C@H](CC)C)', # Isoleucine
	'met': '(CCSC)',       # Methionine
	#aromatic
	'phe': '(Cc1ccccc1)',  # Phenylalanine
	'tyr': '(Cc1ccc(O)cc1)', # Tyrosine
	'trp': '(CC1=CC=C2C(=C1)C(=CN2))', # Tryptophan
	#special
	#'pro': '(C1CC)', # Proline does not fit the model :(
	'cys': '(CS)',      # Cysteine
}

def generate_html_header(title="Test Amino Acids"):
	"""Generates the initial part of the HTML including the RDKit initialization."""
	# Start with DOCTYPE and open the HTML and head tags
	html_header = f"<!DOCTYPE html> <html> <head> <title>{title}</title>"
	# Add the script tag for the RDKit library
	html_header += f'<script src="{rdkit_js_url}"></script>'
	# Append the JavaScript functions related to molecule rendering
	html_header += generate_js_functions()
	# Close the head tag and open the body tag
	html_header += '</head> <body>'
	return html_header

def generate_js_functions2():
	"""Generates JavaScript functions for rendering molecules with RDKit."""
	javascript_functions = '<script>'
	# Define a function to render a molecule with given details
	javascript_functions += 'function renderMolecule(smiles, canvasId, legend) { '
	# Get the molecule object from the provided SMILES string
	javascript_functions += ' let mol = window.RDKit.get_mol(smiles); '
	# Define the details for the molecule rendering
	javascript_functions += ' let mdetails = { '
	javascript_functions += '  explicitMethyl: true,'
	javascript_functions += '  addStereoAnnotation: true,'
	javascript_functions += '  legend: legend,'
	javascript_functions += ' };'
	# Fetch the canvas and draw the molecule onto it
	javascript_functions += ' let canvas = document.getElementById(canvasId);'
	javascript_functions += ' mol.draw_to_canvas_with_highlights(canvas, JSON.stringify(mdetails));'
	javascript_functions += '};'
	javascript_functions += '</script>'
	return javascript_functions

def generate_js_functions3():
	"""Generates JavaScript functions for rendering molecules with RDKit, highlighting peptide bonds."""
	# Base JavaScript for rendering the molecule
	javascript_functions = '<script>'
	javascript_functions += 'function renderMolecule(smiles, canvasId, legend) { '
	javascript_functions += ' let mol = window.RDKit.get_mol(smiles);'
	# Highlight the peptide bond using substructure search
	javascript_functions += ' let peptide_bond = "C(=O)N";'
	javascript_functions += ' let qmol = window.RDKit.get_qmol(peptide_bond);'
	javascript_functions += ' let mdetails = JSON.parse(mol.get_substruct_match(qmol));'
	javascript_functions += ' mdetails["legend"] = legend;'
	javascript_functions += ' mdetails["explicitMethyl"] = true;'
	javascript_functions += ' mdetails["addStereoAnnotation"] = true;'
	javascript_functions += ' mdetails["addBondIndices"] = true;'
	# Fetch the canvas and draw the molecule with highlighted peptide bond
	javascript_functions += ' let canvas = document.getElementById(canvasId);'
	javascript_functions += ' mol.draw_to_canvas_with_highlights(canvas, JSON.stringify(mdetails));'
	javascript_functions += '};'
	javascript_functions += '</script>'

	return javascript_functions

def generate_js_functions():
	"""Generates JavaScript functions for rendering molecules with RDKit, highlighting peptide bonds."""
	# Base JavaScript for rendering the molecule
	javascript_functions = '<script>'
	# New function to process matches and keep only the bonds
	javascript_functions += 'function getPeptideBonds(mol) {'
	javascript_functions += ' let peptide_bond = "CC(=O)NC";'
	javascript_functions += ' let qmol = window.RDKit.get_qmol(peptide_bond);'
	javascript_functions += ' let matches = JSON.parse(mol.get_substruct_matches(qmol));'
	javascript_functions += ' console.log("Matches result:", matches);'
	javascript_functions += ' let aggregatedBonds = [];'
	javascript_functions += ' for(let i = 0; i < matches.length; i++) {'
	javascript_functions += '    let match = matches[i];'
	javascript_functions += '    if (Array.isArray(match["bonds"])) {'
	# Assuming the peptide bond C-N is always the last bond in the bonds array
	javascript_functions += '      console.log("Bonds for match:", match["bonds"], i);'
	javascript_functions += '      let peptideBond = match["bonds"].slice(-2)[0];'
	javascript_functions += '      aggregatedBonds.push(peptideBond);'
	javascript_functions += '    }'
	javascript_functions += '  }'
	javascript_functions += ' console.log(JSON.stringify(aggregatedBonds, null, 2));'
	javascript_functions += '  return aggregatedBonds;'
	javascript_functions += '}'


	javascript_functions += 'function renderMolecule(smiles, canvasId, legend) { '
	javascript_functions += ' let mol = window.RDKit.get_mol(smiles);'
	javascript_functions += ' mol.straighten_depiction(true);'
	# Add hydrogens to the molecule
	#javascript_functions += ' let mol = mol.add_hs_in_place();'
	# Highlight the peptide bond using substructure search
	javascript_functions += ' let mdetails = {};'
	javascript_functions += ' mdetails["bonds"] = getPeptideBonds(mol);'
	javascript_functions += ' mdetails["legend"] = legend;'
	javascript_functions += ' mdetails["explicitMethyl"] = true;'
	javascript_functions += ' mdetails["addStereoAnnotation"] = true;'
	javascript_functions += ' mdetails["highlightColour"] = [0,1,0];'
	#javascript_functions += ' mdetails["addBondIndices"] = true;'
	# Fetch the canvas and draw the molecule with highlighted peptide bond
	javascript_functions += ' let canvas = document.getElementById(canvasId);'
	javascript_functions += ' mol.draw_to_canvas_with_highlights(canvas, JSON.stringify(mdetails));'
	javascript_functions += '};'
	javascript_functions += '</script>'

	return javascript_functions


def generate_html_footer():
	"""Closes off the HTML structure."""
	# Close the body and HTML tags
	return "</body> </html>"

def generate_html_for_molecule(smiles, molecule_name):
	"""Generates HTML section for each molecule."""
	# Display molecule name and its SMILES string
	molecule_html = f'<h3>{molecule_name}</h3> <p>SMILES: {smiles}</p>'
	# Add canvas for molecule visualization
	molecule_html += f'<p><canvas id="canvas_{molecule_name}" width="700" height="350"></canvas></p>'
	# Horizontal rule for separation
	molecule_html += '<hr/>'
	return molecule_html

def generate_js_for_molecule(smiles, molecule_name):
	"""Generates JavaScript function call to render a molecule."""
	return f'renderMolecule("{smiles}", "canvas_{molecule_name}", "{molecule_name}");'

def generation_rdkit_window_code(molecule_js_functions):
	"""Generates JavaScript code to initialize RDKit and render molecules."""
	js_code = '<script>'
	js_code += 'window.initRDKitModule().then(function (RDKit) {'
	# Assign the RDKit instance to the global window object
	js_code += ' window.RDKit = RDKit;'
	# Append the JavaScript function calls to render each molecule
	for js_function in molecule_js_functions:
		js_code += js_function
	js_code += '}); '
	js_code += '</script>'
	return js_code

def main():
	"""Main function to generate the complete HTML page."""
	# Start with the header
	html_content = generate_html_header()
	# List to store JavaScript function calls for each molecule
	molecule_js_functions = []
	# Loop through each molecule and generate HTML content
	for molecule_name, side_chain_smiles in side_chains.items():
		molecule_smiles = pentapeptide.replace('R1', side_chain_smiles)
		molecule_smiles = molecule_smiles.replace('R2', side_chain_smiles)
		molecule_smiles = molecule_smiles.replace('R3', side_chain_smiles)
		molecule_smiles = molecule_smiles.replace('R4', side_chain_smiles)
		molecule_smiles = molecule_smiles.replace('R5', side_chain_smiles)
		html_content +=  generate_html_for_molecule(molecule_smiles, molecule_name)
		molecule_js_function = generate_js_for_molecule(molecule_smiles, molecule_name)
		molecule_js_functions.append(molecule_js_function)
	# Append the JavaScript code
	html_content += generation_rdkit_window_code(molecule_js_functions)
	# Append the HTML footer
	html_content += generate_html_footer()

	# Write the HTML to a file
	with open('test_amino_acids.html', 'w') as file:
		file.write(html_content)

	print(tetrapeptide)
	print(make_poly_peptide(4))

# Run the main function
if __name__ == "__main__":
	main()


