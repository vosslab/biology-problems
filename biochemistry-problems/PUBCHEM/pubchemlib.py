#!/usr/bin/env python3

import os
import re
import copy
import time
import yaml
import random
import requests

#============================
#============================
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
		if self.api_count == 0:
			return
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
		xlogp_str = response_json['PropertyTable']['Properties'][0].get('XLogP')
		if xlogp_str is None:
			return None
		return float(response_json['PropertyTable']['Properties'][0]['XLogP'])

	#=======================
	def get_chemical_name(self, cid):
		"""Retrieve the chemical name for a given CID."""
		endpoint = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/synonyms/JSON"
		response = self.api_call(endpoint)
		if response and 'InformationList' in response:
			# Return the first name (usually the most common name)
			return response['InformationList']['Information'][0]['Synonym'][0]
		return None

	#=======================
	def get_molecular_weight(self, cid):
		# Assuming there's a function in your library that retrieves the molecular weight given a CID
		endpoint = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/MolecularWeight/JSON"
		response = self.api_call(endpoint)
		return float(response["PropertyTable"]["Properties"][0]["MolecularWeight"])

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
		if molecule_name is None:
			return None
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
		if full_name == full_name.upper():
			full_name = full_name.title()
		molecular_weight = self.get_molecular_weight(cid_number)
		molecular_formula = self.get_molecular_formula(cid_number)
		logp = self.get_logp(cid_number)

		# Creating the molecule dictionary
		molecule_data = {
			'Abbreviation': low_molecule_name,
			'CID': cid_number,
			'Full name': full_name,
			'Partition coefficient': logp,
			'Molecular formula': molecular_formula,
			'Molecular weight': molecular_weight,
			'SMILES': smiles,
		}

		self.molecular_data_cache['cid_to_data'][cid_number] = molecule_data

		if self.molecule_data_lookup_count % 10 == 0:
			self.save_cache()

		return molecule_data

	#============================
	#============================
	#=======================
	def format_molecular_formula(self, formula):
		# Regular expression to match numbers and enclose them in <sub> tags
		return re.sub(r'(\d+)', r'<sub>\1</sub> ', formula)


	#============================
	#============================
	#=======================
	def calculate_c_to_on_ratio(self, formula):
		# Find all elements and their counts in the formula
		elements = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
		print(elements)
		element_counts = {element: int(count) if count else 1 for element, count in elements}
		print(element_counts)

		# Extract counts for C, O, and N
		c_count = element_counts.get('C', 0)
		o_count = element_counts.get('O', 0)
		n_count = element_counts.get('N', 0)
		p_count = element_counts.get('P', 0)
		if p_count > 0:
			o_count -= p_count*3

		# Calculate the C/(O+N) ratio
		try:
			return c_count / (o_count + n_count) if (o_count + n_count) > 0 else None
		except ZeroDivisionError:
			return None

	#============================
	def get_link_to_image(self, cid_number):
		return f'https://pubchem.ncbi.nlm.nih.gov/image/imgsrv.fcgi?cid={cid_number}&t=l'

	#============================
	def get_html_to_image(self, cid_number):
		url = self.get_link_to_image(cid_number)
		return f'<a href="{url}" target="_blank" rel="noopener">link to static image</a>'

	#============================
	#============================
	#=======================
	def generate_molecule_info_table(self, molecule_data):
		if molecule_data is None:
			return None
		# Define the common style for table cells
		cell_style = "border: 1px solid #ddd; padding: 5px; font-size: 90%; "
		row_color = ["", "background-color: #f9e9e9;"]

		local_molecule_data = copy.copy(molecule_data)

		ratio = self.calculate_c_to_on_ratio(local_molecule_data['Molecular formula'])
		if ratio:
			local_molecule_data['C/(O+N) ratio'] = f'{ratio:.1f}'
		local_molecule_data['Image link'] = self.get_html_to_image(local_molecule_data['CID'])

		# Start the table with a header
		html_table = f"""
		<table style="border-collapse: collapse;">
			<tr>
				<th colspan="2"
				style="background-color: #806060; color: white; text-align: center; {cell_style}">
				Molecule Information</th>
			</tr>
		"""
		keys_to_use = ['Abbreviation', 'Full name', 'Molecular formula', 'Molecular weight',
			'Image link', 'Partition coefficient', 'C/(O+N) ratio']

		if local_molecule_data['Full name'].lower() == local_molecule_data['Abbreviation'].lower():
			keys_to_use.pop(0)

		# Iterate over items in the dictionary to create table rows
		for index, key in enumerate(keys_to_use):
			value = local_molecule_data.get(key)
			if value is None:
				continue
			if key == 'Molecular formula':
				value = self.format_molecular_formula(value)
			elif key == 'Molecular weight':
				value = f"{value:.2f} g/mol"
			elif key == 'Partition coefficient':
				value = f"{value:.1f} logP"
			html_table += f"""
			<tr style="{row_color[index % 2]}">
				<td style="{cell_style}">{key.replace('_', ' ')}</td>
				<td style="{cell_style}">{value}</td>
			</tr>
			"""

		# Close the table
		html_table += "</table>"
		html_table = html_table.replace('\n', ' ')
		html_table = html_table.replace('\t', ' ')
		while '  ' in html_table:
			html_table = html_table.replace('  ', ' ')
		return html_table

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
