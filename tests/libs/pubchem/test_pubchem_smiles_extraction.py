
from lib_test_utils import import_from_repo_path


def test_pubchemlib_smiles_extraction_accepts_smiles_key():
	pubchemlib = import_from_repo_path("problems/biochemistry-problems/PUBCHEM/pubchemlib.py")
	pcl = object.__new__(pubchemlib.PubChemLib)

	resp = {
		'PropertyTable': {
			'Properties': [
				{
					'CID': 5950,
					'SMILES': 'C[C@@H](C(=O)O)N',
				}
			]
		}
	}
	assert pcl._extract_smiles_from_property_response(resp) == 'C[C@@H](C(=O)O)N'

