#!/usr/bin/env python3

import time
import yaml
import random
import requests

BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

with open('molecules.yml', 'r') as file:
	molecules = yaml.safe_load(file)

#=======================
def read_molecules_from_file(filename):
	with open(filename, 'r') as file:
		return [line.strip() for line in file]

#=======================
def api_call(endpoint):
	"""Make a common API call, and sleep for a random short duration afterwards."""
	response = requests.get(endpoint)
	time.sleep(random.random())  # Sleep for 0 to 1 second
	return response.json()

#=======================
def get_cid(molecule_name):
	"""Get the CID of a molecule from its name."""
	response_json = api_call(f"{BASE_URL}/compound/name/{molecule_name}/cids/JSON")
	if 'IdentifierList' in response_json:
		return response_json['IdentifierList']['CID'][0]
	else:
		return None

#=======================
def get_smiles(cid):
	"""Get the SMILES notation for a molecule given its CID."""
	response_json = api_call(f"{BASE_URL}/compound/cid/{cid}/property/IsomericSMILES/JSON")
	return response_json['PropertyTable']['Properties'][0]['IsomericSMILES']

#=======================
def get_cids_for_formula(formula):
	"""Retrieve compound CIDs from PubChem for a given formula using api_call."""
	endpoint = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastformula/{formula}/cids/JSON"
	response = api_call(endpoint)
	if response and 'IdentifierList' in response:
		return response['IdentifierList']['CID']
	return []

#=======================
def get_chemical_name(cid):
	"""Retrieve the chemical name for a given CID."""
	endpoint = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/synonyms/JSON"
	response = api_call(endpoint)
	if response and 'InformationList' in response:
		# Return the first name (usually the most common name)
		return response['InformationList']['Information'][0]['Synonym'][0].title()
	return None

#=======================
def get_molecular_weight(cid):
	# Assuming there's a function in your library that retrieves the molecular weight given a CID
	endpoint = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/MolecularWeight/JSON"
	response = api_call(endpoint)
	return response["PropertyTable"]["Properties"][0]["MolecularWeight"]

#=======================
def get_molecular_formula(cid):
	# Assuming there's a function in your library that retrieves the molecular formula given a CID
	endpoint = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/MolecularFormula/JSON"
	response = api_call(endpoint)
	return response["PropertyTable"]["Properties"][0]["MolecularFormula"]

#=======================
def main2():
	molecules = ['Ethanol', 'NAD+', 'Acetaldehyde', 'L-Serine']
	for molecule in molecules:
		cid = get_cid(molecule)
		if cid:
			smiles = get_smiles(cid)
			print(f"SMILES for {molecule}: {smiles}")
		else:
			print(f"Could not find SMILES for {molecule}")

#=======================
def get_molecule_info_dict(molecule_name):
	molecule_name = molecule_name.lower()
	cid = get_cid(molecule_name)
	if not cid:
		return None
	smiles = get_smiles(cid)
	full_name = get_chemical_name(cid)
	molecular_weight = get_molecular_weight(cid)
	molecular_formula = get_molecular_formula(cid)

	# Creating the molecule dictionary
	molecule_data = {
		molecule_name.lower(): {
			'Abbreviation': molecule_name.lower(),  # Adjust as needed
			'Full name': full_name,
			'SMILES': smiles,
			'Molecular_Weight': molecular_weight,
			'Molecular_Formula': molecular_formula,
			'CID': cid
		}
	}
	return molecule_data

#=======================
def save_data(molecules_data_dict, data_filename):
	print('... saving data ...')
	# Write updated molecules to molecules.yml
	with open(data_filename, "w") as f:
		yaml.dump(molecules_data_dict, f)
	return

#=======================
#=======================
def main():
	# Load existing molecules from molecules.yml
	try:
		with open("molecules.yml", "r") as f:
			existing_molecules = yaml.safe_load(f)
			if existing_molecules is None:
				existing_molecules = []
	except FileNotFoundError:
		existing_molecules = []

	existing_molecule_names = [mol[list(mol.keys())[0]]['Full name'] for mol in existing_molecules]

	# Read molecules from molecules_to_add.txt
	new_molecules = read_molecules_from_file("molecules_to_add.txt")

	# Process each molecule
	for molecule in new_molecules:
		if molecule not in existing_molecule_names:
			molecule_data = get_molecule_info_dict(molecule_name)
			if molecule_data:
				existing_molecules.append(molecule_data)
			else:
				print(f"Could not find data for {molecule}")

	# Write updated molecules to molecules.yml
	with open("molecules.yml", "w") as f:
		yaml.dump(existing_molecules, f)

if __name__ == "__main__":
	main()
