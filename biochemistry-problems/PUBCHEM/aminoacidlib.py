

alanine = '[NH3+][C@@H][CH3](C(=O)[O-])'

amino_acid = '[NH3+][C@@H][R1](C(=O)[O-])'
dipeptide = '[NH3+][C@@H][R1](C(=O)N[C@@H][R2](C(=O)[O-]))'
tripeptide = '[NH3+][C@@H][R1](C(=O)N[C@@H][R2](C(=O)N[C@@H][R3](C(=O)[O-]))'
tetrapeptide = '[NH3+][C@@H][R1](C(=O)N[C@@H][R2](C(=O)N[C@@H][R3](C(=O)N[C@@H][R4](C(=O)[O-]))'

side_chains = {
	#smallest
	'gly': 'H',         # Glycine
	'ala': 'CH3',       # Alanine
	#polar
	'ser': 'CH2OH',        # Serine
	'thr': '[C@H](OH)CH3',    # Threonine
	'asn': 'CH2C(=O)NH2',    # Asparagine
	'gln': 'CH2CH2C(=O)NH2', # Glutamine
	#negative charge
	'asp': 'CH2C(=O)[O-]',    # Aspartate
	'glu': 'CH2CH2C(=O)[O-]', # Glutamate
	#positive charge
	'lys': 'CH2CH2CH2CH2NH3+',        # Lysine
	'arg': 'CH2CH2CH2NHC(=NH2+)NH2',  # Arginine
	'his': 'CH2C1H=CH([N]CH=N1H)',    # Histidine
	'his+': 'CH2C1H=CH([NH+]CH=N1H)', # Histidine
	#branch chain
	'val': 'CH(CH3)CH3',       # Valine
	'leu': 'CH2CH(CH3)CH3',    # Leucine
	'ile': '[C@H](CH3)CH2CH3', # Isoleucine
	'met': 'CH2CH2SCH3',       # Methionine
	#aromatic
	'phe': 'CH2c1HcHcHcHcHc1H',  # Phenylalanine
	'tyr': 'CH2c1Hc(OH)cHcHcHc1H', # Tyrosine
	'trp': 'CH2c1c[nH]c2c1cccc2', # Tryptophan
	#special
	'pro': 'C1H2CH2CH2', # Proline
	'cys': 'CH2SH',      # Cysteine
}

