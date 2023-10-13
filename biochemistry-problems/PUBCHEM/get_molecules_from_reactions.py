#!/usr/bin/env python3

import yaml

def extract_molecules_from_yaml(filename):
	with open(filename, 'r') as file:
		data = yaml.safe_load(file)

	all_molecules = set()  # Using a set to avoid duplicates

	for enzyme_class, details in data.items():
		reactions = details.get('Reactions', [])
		for reaction in reactions:
			substrates = reaction.get('Substrates', [])
			products = reaction.get('Products', [])

			for molecule in substrates + products:
				all_molecules.add(molecule)

	return list(all_molecules)


if __name__ == "__main__":
	filename = "reactions.yml"
	molecules = extract_molecules_from_yaml(filename)

	print("List of Molecules:")
	for molecule in molecules:
		print(molecule)

