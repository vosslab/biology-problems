#!/usr/bin/env python3
import argparse
import zipfile
import os
import tempfile

#====================
def modify_partial_credit(data: str) -> str:
	"""
	Modifies the <bbmd_partialcredit> tags in a given data string.

	Parameters
	----------
	data : str
		The content of the DAT file as a string.

	Returns
	-------
	str
		The modified content of the DAT file.
	"""
	return data.replace('<bbmd_partialcredit></bbmd_partialcredit>',
						'<bbmd_partialcredit>true</bbmd_partialcredit>')

#====================
def process_zip(input_zip: str, output_zip: str) -> None:
	"""
	Processes the ZIP file to modify the res00001.dat file.

	Parameters
	----------
	input_zip : str
		Path to the input ZIP file.
	output_zip : str
		Path to the output ZIP file where modified content will be written.

	Returns
	-------
	None
	"""
	with tempfile.TemporaryDirectory() as temp_dir:
		# Extract the ZIP file
		with zipfile.ZipFile(input_zip, 'r') as zip_ref:
			zip_ref.extractall(temp_dir)

		dat_file_path = os.path.join(temp_dir, 'res00001.dat')

		# Modify the DAT file if it exists
		if os.path.exists(dat_file_path):
			with open(dat_file_path, 'r') as file:
				data = file.read()

			modified_data = modify_partial_credit(data)

			with open(dat_file_path, 'w') as file:
				file.write(modified_data)

		# Create a new ZIP file with modified content
		with zipfile.ZipFile(output_zip, 'w') as zip_ref:
			for folder_name, subfolders, filenames in os.walk(temp_dir):
				for filename in filenames:
					file_path = os.path.join(folder_name, filename)
					zip_ref.write(file_path, os.path.relpath(file_path, temp_dir))

#====================
def main():
	parser = argparse.ArgumentParser(description='Modify bbmd_partialcredit tags in res00001.dat within a ZIP file.')
	parser.add_argument('-i', '--input', dest='input_zip', required=True,
						help='Input ZIP file path')

	args = parser.parse_args()
	output_zip = "edited-"+args.input_zip.replace(' ', '_')

	process_zip(args.input_zip, output_zip)
	print(f"Modified ZIP file saved as {output_zip}")

if __name__ == "__main__":
	main()
