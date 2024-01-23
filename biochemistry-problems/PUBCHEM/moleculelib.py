#!/usr/bin/env python3

import random
import crcmod.predefined #pip

debug = False

pyrimidines = {
	'cytosine': 'C1=CN(C(=O)N=C1N)[Si@H]', #ONH
	'thymine': 'CC1=CN(C(=O)NC1=O)[Si@H]', #OHO
	'uracil': 'C1=CN(C(=O)NC1=O)[Si@H]', #OHO
}

#=================================================
#=================================================
rdkit_js_url = "https://unpkg.com/@rdkit/rdkit/dist/RDKit_minimal.js"

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
	if debug is True:
		js_code += 'console.log(RDKitModule);'
	js_code += f'let/* */smiles="{smiles}";'
	js_code += 'let/* */mol=RDKitModule.get_mol(smiles);'
	js_code += 'let/* */mdetails={};'
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
def generate_html_for_molecule(smiles, molecule_name=None, width=256, height=256):
	"""Generates HTML section for each molecule."""
	# Display molecule name
	crc_code = getCrc16_FromString(smiles)
	if molecule_name is None:
		molecule_name = crc_code
	molecule_html = f'<h4>{molecule_name}</h4>'
	if debug is True:
		molecule_html += f'<p>SMILES: {smiles}</p>'
	canvas_id = f"canvas_{crc_code}"
	molecule_html += f'<p><canvas id="{canvas_id}" width="{width}" height="{height}"></canvas></p>'
	# Horizontal rule for separation
	molecule_html += '<hr/>'
	molecule_html += generate_js_functions(smiles, canvas_id, molecule_name)
	return molecule_html

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
	html_content = generate_html_header(title="Test Molecules")
	# includes generate_load_script()
	for name, smiles in pyrimidines.items():
		html_content += generate_html_for_molecule(smiles, name)
	html_content += generate_html_footer()

	# Write the HTML to a file
	html_file = 'test_molecules.html'
	with open('test_molecules.html', 'w') as file:
		file.write(html_content)
	print(f'open {html_file}')


# Run the main function
if __name__ == "__main__":
	main()


