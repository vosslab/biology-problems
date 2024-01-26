#!/usr/bin/env python3

import sys
import yaml
import pubchemlib

def save_data(new_molecules_data_dict):
	filename = "new_molecules_dict.yml"
	#new_molecules_data_list = sorted(new_molecules_data_list, key=lambda d: d['Abbreviation'])
	print(f'... saving data ... to {filename}')
	# Write updated molecules to molecules.yml
	with open(filename, "w") as f:
		yaml.dump(new_molecules_data_dict, f)
	sys.exit(1)
	return


def main():
	filename = 'molecules.txt'
	new_molecules = pubchemlib.read_molecules_from_file(filename)

	new_molecules_data_dict = {}

	count = 0
	# Process each molecule
	for molecule in new_molecules:
		if len(molecule) < 2 or molecule.startswith("#"):
			continue
		count += 1
		if count % 10 == 0:
			save_data(new_molecules_data_dict)
		print(molecule)
		cid = pubchemlib.get_cid(molecule)
		if cid:
			low_molecular_name = molecule.lower()
			smiles = pubchemlib.get_smiles(cid)
			full_name = pubchemlib.get_chemical_name(cid)
			molecular_weight = pubchemlib.get_molecular_weight(cid)
			molecular_formula = pubchemlib.get_molecular_formula(cid)
			logp = pubchemlib.get_logp(cid)

			# Creating the molecule dictionary
			molecule_data = {
				'Abbreviation': low_molecular_name,
				'CID': cid,
				'Full name': full_name,
				'LogP': logp,
				'Molecular_Formula': molecular_formula,
				'Molecular_Weight': molecular_weight,
				'SMILES': smiles,
			}
			new_molecules_data_dict[low_molecular_name] = molecule_data
		else:
			print(f" .. Could not find data for {low_molecular_name}")

	save_data(new_molecules_data_dict)


if __name__ == "__main__":
	main()
