#!/usr/bin/env python3

import os
import time
import yaml
import random
import requests


class PubChemLib():
	#============================
	#============================
	def __init__(self):
		self.start_time = time.time()
		self.BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
		self.cache_file = 'cache_pubchem_molecules.yml'
		self.api_count = 0
		self.molecule_data_lookup_count = 0
		self.molecule_cid_lookup_count = 0
		self.expected_molecule_data_keys = 7
		self.load_cache()
		#self.molecular_data_cache has two maps:
		# 1. maps cid number to molecular data
		# 2. maps molecular name to cid number
		# 3. time stamp

	#============================
	#============================
	def load_cache(self):
		print('==== LOAD CACHE ====')
		if os.path.isfile(self.cache_file):
			t0 = time.time()
			with open(self.cache_file, 'r') as file:
				self.molecular_data_cache = yaml.safe_load(file)
			print('.. loaded {0} entires from {1} in {2:,d} usec'.format(
				len(self.molecular_data_cache['cid_to_data']), self.cache_file, int((time.time()-t0)*1e6)))
		else:
			print(f".. creating NEW data file {self.cache_file}")
			self.molecular_data_cache = {
				'cid_to_data': {},
				'name_to_cid': {},
				'time_stamp': int(time.time()),
			}
		#print(len(self.molecular_data_cache['cid_to_data']))
		print('==== END CACHE ====')

	#============================
	#============================
	def close(self):
		self.save_cache()
		print(f"{self.molecule_cid_lookup_count} cid lookup requests were made")
		print(f"{self.molecule_data_lookup_count} molecular data dict requests were made")
		print(f"{self.api_count} api calls were made")

	#============================
	#============================
	def save_cache(self):
		print('==== SAVE CACHE ====')
		t0 = time.time()
		self.molecular_data_cache['time_stamp'] = int(t0)
		if len(self.molecular_data_cache) > 0:
			with open(self.cache_file, 'w') as file:
				yaml.dump(self.molecular_data_cache, file)
			print('.. wrote {0} entires to {1} in {2:,d} usec'.format(
				len(self.molecular_data_cache['cid_to_data']), self.cache_file, int((time.time()-t0)*1e6)))
		print('==== END CACHE ====')

	#============================
	#============================
	#=======================
	def api_call(self, endpoint):
		self.api_count += 1
		"""Make a common API call, and sleep for a random short duration afterwards."""
		response = requests.get(endpoint)
		time.sleep(random.random())  # Sleep for 0 to 1 second
		return response.json()

	#============================
	#============================
	#=======================
	def get_cid(self, molecule_name):
		#check if cached value exists:
		low_molecule_name = molecule_name.lower().strip()
		cid_number = self.molecular_data_cache['name_to_cid'].get(low_molecule_name)
		if cid_number is not None:
			return cid_number

		self.molecule_cid_lookup_count += 1

		"""Get the CID of a molecule from its name."""
		response_json = self.api_call(f"{self.BASE_URL}/compound/name/{molecule_name}/cids/JSON")
		if 'IdentifierList' in response_json:
			cid_number = response_json['IdentifierList']['CID'][0]
			cid_number = int(cid_number)
			self.molecular_data_cache['name_to_cid'][low_molecule_name] = cid_number
			return cid_number
		else:
			return None

	#=======================
	def get_cids_for_formula(self, formula):
		"""Retrieve compound CIDs from PubChem for a given formula using api_call."""
		endpoint = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastformula/{formula}/cids/JSON"
		response = self.api_call(endpoint)
		if response and 'IdentifierList' in response:
			return response['IdentifierList']['CID']
		return []

	#============================
	#============================
	#============================
	#============================
	#=======================
	def get_smiles(self, cid):
		"""Get the SMILES notation for a molecule given its CID."""
		response_json = self.api_call(f"{self.BASE_URL}/compound/cid/{cid}/property/IsomericSMILES/JSON")
		return response_json['PropertyTable']['Properties'][0]['IsomericSMILES']

	#=======================
	def get_logp(self, cid):
		"""Get the SMILES notation for a molecule given its CID."""
		response_json = self.api_call(f"{self.BASE_URL}/compound/cid/{cid}/property/XLogP/JSON")
		return response_json['PropertyTable']['Properties'][0]['XLogP']

	#=======================
	def get_chemical_name(self, cid):
		"""Retrieve the chemical name for a given CID."""
		endpoint = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/synonyms/JSON"
		response = self.api_call(endpoint)
		if response and 'InformationList' in response:
			# Return the first name (usually the most common name)
			return response['InformationList']['Information'][0]['Synonym'][0].title()
		return None

	#=======================
	def get_molecular_weight(self, cid):
		# Assuming there's a function in your library that retrieves the molecular weight given a CID
		endpoint = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/MolecularWeight/JSON"
		response = self.api_call(endpoint)
		return response["PropertyTable"]["Properties"][0]["MolecularWeight"]

	#=======================
	def get_molecular_formula(self, cid):
		# Assuming there's a function in your library that retrieves the molecular formula given a CID
		endpoint = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/MolecularFormula/JSON"
		response = self.api_call(endpoint)
		return response["PropertyTable"]["Properties"][0]["MolecularFormula"]

	#============================
	#============================
	#============================
	#============================
	#=======================
	def get_molecule_data_dict(self, molecule_name):
		if len(molecule_name) < 2 or molecule_name.startswith("#"):
			return None
		low_molecule_name = molecule_name.lower().strip()
		cid_number = self.get_cid(low_molecule_name)
		if cid_number is None:
			return None
		#check if cached value exists:
		molecule_data = self.molecular_data_cache['cid_to_data'].get(cid_number)
		if molecule_data is not None and len(molecule_data) == self.expected_molecule_data_keys:
			return molecule_data

		self.molecule_data_lookup_count += 1

		smiles = self.get_smiles(cid_number)
		full_name = self.get_chemical_name(cid_number)
		molecular_weight = self.get_molecular_weight(cid_number)
		molecular_formula = self.get_molecular_formula(cid_number)
		logp = self.get_logp(cid_number)

		# Creating the molecule dictionary
		molecule_data = {
			'Abbreviation': low_molecule_name,
			'CID': cid_number,
			'Full name': full_name,
			'LogP': logp,
			'Molecular_Formula': molecular_formula,
			'Molecular_Weight': molecular_weight,
			'SMILES': smiles,
		}

		self.molecular_data_cache['cid_to_data'][cid_number] = molecule_data

		if self.molecule_data_lookup_count % 10 == 0:
			self.save_cache()

		return molecule_data

#=======================
#=======================
def main():
	pcl = PubChemLib()

	# Read molecules from molecules_to_add.txt
	molecules_list =['acetone', 'glucose', 'adenine', 'alanine', 'palmitate']

	# Process each molecule
	for molecule_name in molecules_list:
		molecule_data = pcl.get_molecule_data_dict(molecule_name)
		print(molecule_data)
	pcl.close()

if __name__ == "__main__":
	main()
