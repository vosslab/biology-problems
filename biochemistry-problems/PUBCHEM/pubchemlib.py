import requests
import time
import random

BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

def api_call(endpoint):
    """Make a common API call, and sleep for a random short duration afterwards."""
    response = requests.get(endpoint)
    time.sleep(random.random())  # Sleep for 0 to 1 second
    return response.json()

def get_cid(molecule_name):
    """Get the CID of a molecule from its name."""
    response_json = api_call(f"{BASE_URL}/compound/name/{molecule_name}/cids/JSON")
    if 'IdentifierList' in response_json:
        return response_json['IdentifierList']['CID'][0]
    else:
        return None

def get_smiles(cid):
    """Get the SMILES notation for a molecule given its CID."""
    response_json = api_call(f"{BASE_URL}/compound/cid/{cid}/property/IsomericSMILES/JSON")
    return response_json['PropertyTable']['Properties'][0]['IsomericSMILES']

def get_cids_for_formula(formula):
    """Retrieve compound CIDs from PubChem for a given formula using api_call."""
    endpoint = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastformula/{formula}/cids/JSON"
    response = api_call(endpoint)
    if response and 'IdentifierList' in response:
        return response['IdentifierList']['CID']
    return []

def get_chemical_name(cid):
    """Retrieve the chemical name for a given CID."""
    endpoint = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/synonyms/JSON"
    response = api_call(endpoint)
    if response and 'InformationList' in response:
        # Return the first name (usually the most common name)
        return response['InformationList']['Information'][0]['Synonym'][0]
    return None


def main():
    molecules = ['Ethanol', 'NAD+', 'Acetaldehyde']
    
    for molecule in molecules:
        cid = get_cid(molecule)
        if cid:
            smiles = get_smiles(cid)
            print(f"SMILES for {molecule}: {smiles}")
        else:
            print(f"Could not find SMILES for {molecule}")

if __name__ == "__main__":
    main()
