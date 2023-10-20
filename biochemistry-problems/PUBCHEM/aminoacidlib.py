#!/usr/bin/env python3

import random
import crcmod.predefined #pip

debug = False

#=================================================
#=================================================
zwitterion_amino_acid = '[NH3+][C@@H]R1(C(=O)[O-])'
neutral_amino_acid = 'N[C@@H]R1(C(=O)O)'
amino_acid = zwitterion_amino_acid
rdkit_js_url = "https://unpkg.com/@rdkit/rdkit/dist/RDKit_minimal.js"

#=================================================
#=================================================
glycine = '[NH3+][C@@H](C(=O)[O-])'
alanine = '[NH3+][C@@H](C)(C(=O)[O-])'

#=================================================
#=================================================
dipeptide = '[NH3+][C@@H]R1(C(=O)N[C@@H]R2(C(=O)[O-]))'
tripeptide = '[NH3+][C@@H]R1(C(=O)N[C@@H]R2(C(=O)N[C@@H]R3(C(=O)[O-])))'
tetrapeptide = '[NH3+][C@@H]R1(C(=O)N[C@@H]R2(C(=O)N[C@@H]R3(C(=O)N[C@@H]R4(C(=O)[O-]))))'
pentapeptide = '[NH3+][C@@H]R1(C(=O)N[C@@H]R2(C(=O)N[C@@H]R3(C(=O)N[C@@H]R4(C(=O)N[C@@H]R5(C(=O)[O-])))))'

#==========================
def getCrc16_FromString(mystr):
	crc16 = crcmod.predefined.Crc('xmodem')
	try:
		crc16.update(mystr.encode('ascii', errors='strict'))
	except UnicodeEncodeError:
		return ''.join(random.choices('0123456789abcdef', k=4))
	return crc16.hexdigest().lower()

#=================================================
#=================================================
def make_poly_peptide(length=5):
	amino_terminal_end = '[NH3+][C@@H]'
	carboxyl_terminal_end = '(C(=O)[O-])'
	peptide_bond = '(C(=O)N[C@@H]'
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

#=================================================
#=================================================
def make_peptide_from_sequence(seq):
	poly_peptide = make_poly_peptide(len(seq))
	for i,aa in enumerate(list(seq.upper())):
		three_letter_code = amino_acid_mapping[aa]
		side_chain = side_chains[three_letter_code]
		poly_peptide = poly_peptide.replace(f'R{i+1}', side_chain)
	return poly_peptide

#=================================================
#=================================================
amino_acid_mapping = {
	'A': 'Ala',  # Alanine
	'C': 'Cys',  # Cysteine
	'D': 'Asp',  # Aspartic Acid
	'E': 'Glu',  # Glutamic Acid
	'F': 'Phe',  # Phenylalanine
	'G': 'Gly',  # Glycine
	'H': 'His',  # Histidine
	'I': 'Ile',  # Isoleucine
	'K': 'Lys',  # Lysine
	'L': 'Leu',  # Leucine
	'M': 'Met',  # Methionine
	'N': 'Asn',  # Asparagine
	'P': 'Pro',  # Proline
	'Q': 'Gln',  # Glutamine
	'R': 'Arg',  # Arginine
	'S': 'Ser',  # Serine
	'T': 'Thr',  # Threonine
	'V': 'Val',  # Valine
	'W': 'Trp',  # Tryptophan
	'Y': 'Tyr'   # Tyrosine
}

#=================================================
#=================================================
side_chains = {
	#smallest
	'Gly': '([H])',         # Glycine
	'Gly2': '',         # Glycine
	'Ala': '(C)',       # Alanine
	#polar
	'Ser': '(CO)',        # Serine
	'Thr': '([C@H](O)C)',    # Threonine
	#'Allo-Thr': '([C@@H](O)C)', # AlloThreonine
	'Asn': '(CC(=O)N)',    # Asparagine
	'Gln': '(CCC(=O)N)',    # Glutamine
	#negative charge
	'Asp': '(CC(=O)[O-])',    # Aspartate
	'Glu': '(CCC(=O)[O-])',    # Glutamate
	#positive charge
	'Lys': '(CCCC[NH3+])',        # Lysine
	'Arg': '(CCCNC(=[NH2+])N)',  # Arginine
	'His': '(CC1=C[NH]C=N1)',      # Histidine delta tautomer at pH 7
	'His2': '(CC1=CN=C[NH]1)',     # Histidine epsilon tautomer at pH 7
	'His3': '(CC1=C[NH]C=[NH+]1)', # Histidine delta tautomer at pH 5
	'His4': '(CC1=C[NH+]=C[NH]1)', # Histidine epsilon tautomer at pH 5
	#branch chain
	'Val': '(C(C)C)',       # Valine
	'Leu': '(CC(C)C)',    # Leucine
	'Ile': '([C@H](CC)C)', # Isoleucine
	'Met': '(CCSC)',       # Methionine
	#aromatic
	'Phe': '(Cc1ccccc1)',  # Phenylalanine
	'Tyr': '(Cc1ccc(O)cc1)', # Tyrosine
	'Trp': '(CC1=CC=C2C(=C1)C(=CN2))', # Tryptophan
	#special
	#'Pro': '(C1CC)', # Proline does not fit the model :(
	'Cys': '(CS)',      # Cysteine
}

#=================================================
#=================================================
def generate_html_header(title="Test Amino Acids"):
	"""Generates the initial part of the HTML including the RDKit initialization."""
	# Start with DOCTYPE and open the HTML and head tags
	html_header = f"<!DOCTYPE html> <html> <head> <title>{title}</title>"
	# Add the script tag for the RDKit library
	html_header += generate_load_script()
	# Close the head tag and open the body tag
	html_header += '</head> <body>'
	return html_header

#=================================================
#=================================================
def generate_load_script():
	"""needs better description"""
	# Add the script tag for the RDKit library
	html_load_script = f'<script src="{rdkit_js_url}"></script>'
	# Append the JavaScript functions related to molecule rendering
	#html_load_script += generate_js_functions()
	return html_load_script

#=================================================
#=================================================
def generate_js_functions_orig():
	"""Generates JavaScript functions for rendering molecules with RDKit, highlighting peptide bonds."""
	# Base JavaScript for rendering the molecule
	javascript_functions = '<script>'
	# New function to process matches and keep only the bonds
	#javascript_functions += 'function handleError() { '
	#javascript_functions += '  var errorMsg = document.createElement("p");'
	#javascript_functions += '  errorMsg.style.color = "red";'
	#javascript_functions += '  errorMsg.textContent = "Failed to load the RDKit library, contact Dr. Voss";'
	#javascript_functions += '  document.body.insertBefore(errorMsg, document.body.firstChild);'
	#javascript_functions += '};'

	"""
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
	"""

	javascript_functions += 'function renderMolecule(smiles, canvasId, legend) { '
	javascript_functions += ' let mol = window.RDKit.get_mol(smiles);'
	#javascript_functions += ' mol.straighten_depiction(true);'
	# Add hydrogens to the molecule
	#javascript_functions += ' let mol = mol.add_hs_in_place();'
	# Highlight the peptide bond using substructure search
	javascript_functions += ' let mdetails = {};'
	#javascript_functions += ' mdetails["bonds"] = getPeptideBonds(mol);'
	#javascript_functions += ' mdetails["legend"] = legend;'
	javascript_functions += ' mdetails["explicitMethyl"] = true;'
	#javascript_functions += ' mdetails["addStereoAnnotation"] = true;'
	#javascript_functions += ' mdetails["highlightColour"] = [0,1,0];'
	#javascript_functions += ' mdetails["addBondIndices"] = true;'
	# Fetch the canvas and draw the molecule with highlighted peptide bond
	javascript_functions += ' let canvas = document.getElementById(canvasId);'
	javascript_functions += ' mol.draw_to_canvas_with_highlights(canvas, JSON.stringify(mdetails));'
	javascript_functions += '};'
	javascript_functions += '</script>'
	javascript_functions = javascript_functions.replace('  ', ' ')
	return javascript_functions

#=================================================
def generate_js_functions(smiles, canvas_id, molecule_name=None):
	"""Generates JavaScript functions for rendering molecules with RDKit, highlighting peptide bonds."""
	# Base JavaScript for rendering the molecule
	#this completely works
	js_code = '<script>'
	js_code += '/* */'
	js_code += 'initRDKitModule().then(function(instance){'
	js_code += 'RDKitModule=instance;'
	js_code += 'console.log("RDKit:"+RDKitModule.version());'
	js_code += '/* */'
	js_code += 'function/* */getPeptideBonds(mol){'
	js_code += 'let/* */peptide_bond="CC(=O)NC";'
	js_code += 'let/* */qmol=window.RDKitModule.get_qmol(peptide_bond);'
	js_code += 'let/* */matches=JSON.parse(mol.get_substruct_matches(qmol));'
	js_code += 'let/* */aggregatedBonds=[];'
	js_code += 'for(let/* */i=0;i<matches.length;i++){'
	js_code += 'match=matches[i];'
	js_code += 'if(Array.isArray(match["bonds"])){'
	# Tthe peptide bond C-N is always the second to last bond in the bonds array
	js_code += 'aggregatedBonds.push(match["bonds"].slice(-2)[0]);'
	js_code += '}'
	js_code += '}'
	js_code += 'return/* */aggregatedBonds;'
	js_code += '}'
	if debug is True:
		js_code += 'console.log(RDKitModule);'
	js_code += f'let/* */smiles="{smiles}";'
	js_code += 'let/* */mol=RDKitModule.get_mol(smiles);'
	js_code += 'let/* */mdetails={};'
	js_code += 'mdetails.explicitMethyl=true;'
	js_code += 'mdetails["bonds"]=getPeptideBonds(mol);'
	js_code += 'mdetails["atoms"]=[0];'
	js_code += 'mdetails["highlightColour"]=[0,1,0];'
	if molecule_name is not None:
		js_code += f'mdetails["legend"]="{molecule_name}";'
	js_code += 'mdetails["explicitMethyl"]=true;'
	if debug is True:
		js_code += 'mdetails["addStereoAnnotation"]=true;'
		js_code += 'mdetails["addBondIndices"]=true;'
		js_code += 'console.log(mdetails);'
	js_code += f'canvas=document.getElementById("{canvas_id}");'
	js_code += 'mol.draw_to_canvas_with_highlights(canvas,JSON.stringify(mdetails));'
	js_code += '});'
	js_code += '/* */'
	js_code += '</script>'
	return js_code

#=================================================
def generate_html_for_molecule(smiles, molecule_name=None, width=1024, height=768):
	"""Generates HTML section for each molecule."""
	# Display molecule name
	if molecule_name is None:
		molecule_name = getCrc16_FromString(smiles)
	molecule_html = f'<h4>{molecule_name}</h4>'
	if debug is True:
		molecule_html += f'<p>SMILES: {smiles}</p>'
	canvas_id = f"canvas_{molecule_name}"
	molecule_html += f'<p><canvas id="{canvas_id}" width="{width}" height="{height}"></canvas></p>'
	# Horizontal rule for separation
	molecule_html += '<hr/>'
	molecule_html += generate_js_functions(smiles, canvas_id)
	return molecule_html

"""
// this completely works
<script>/*
  */initRDKitModule().then(function(instance){
RDKitModule=instance;
console.log("RDKit:"+RDKitModule.version());
smiles="CC(=O)Oc1ccccc1C(=O)O";
mol=RDKitModule.get_mol(smiles);
canvas=document.getElementById("canvas_4ab7");
mol.draw_to_canvas(canvas,-1,-1);
});/*
  */</script>
"""

#=================================================
#=================================================
def generate_html_footer():
	"""Closes off the HTML structure."""
	# Close the body and HTML tags
	return "</body> </html>"






#=================================================
#=================================================
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


