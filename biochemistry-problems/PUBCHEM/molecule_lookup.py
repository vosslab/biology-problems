#!/usr/bin/env python3

import sys
import yaml
import pubchemlib

def save_data(new_molecules_data_list):
	new_molecules_data_list = sorted(new_molecules_data_list, key=lambda d: d['Abbreviation'])
	print('... saving data ...')

	# Write updated molecules to molecules.yml
	with open("new_molecules.yml", "w") as f:
		yaml.dump(new_molecules_data_list, f)
	return


def main():
	filename = 'molecules.txt'
	new_molecules = pubchemlib.read_molecules_from_file(filename)

	new_molecules_data_list = []

	count = 0
	# Process each molecule
	for molecule in new_molecules:
		if len(molecule) < 2:
			continue
		count += 1
		if count % 10 == 0:
			save_data(new_molecules_data_list)
		print(molecule)
		cid = pubchemlib.get_cid(molecule)
		if cid:
			smiles = pubchemlib.get_smiles(cid)
			full_name = pubchemlib.get_chemical_name(cid)
			molecular_weight = pubchemlib.get_molecular_weight(cid)
			molecular_formula = pubchemlib.get_molecular_formula(cid)

			# Creating the molecule dictionary
			molecule_data = {
				'Abbreviation': molecule.lower(),  # Adjust as needed
				'Full name': full_name,
				'SMILES': smiles,
				'Molecular_Weight': molecular_weight,
				'Molecular_Formula': molecular_formula,
				'CID': cid
			}
			new_molecules_data_list.append(molecule_data)
		else:
			print(f" .. Could not find data for {molecule}")

	save_data(new_molecules_data_list)


if __name__ == "__main__":
	main()
