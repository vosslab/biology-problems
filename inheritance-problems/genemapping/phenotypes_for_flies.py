

#====================================
# Dictionary to describe hypothetical fruit fly phenotypes
#====================================

# Dictionary that maps various hypothetical phenotypes of fruit flies to their descriptions.
# Each key in the dictionary is a unique, quirky name describing a phenotype, and each value is a description
# that elaborates on the visual or behavioral characteristics of that phenotype.
phenotype_dict = {
	'artsy':   'has wings that are colorful and distinctive patterns.',
	'bumpy':   'has a skin texture that is not smooth, but rough with small bumps all over.',
	'chummy':  'shows behavior where it always maintains a close distance to other flies.',
	'dewy':    'appears moist, with its body covered in tiny droplets of water.',
	'eery':    'appears to have something off, crooked limbs and other twisted appendages.',
	'fuzzy':   'is covered in a dense layer of hairs, giving it a soft appearance.',
	'gooey':   'is coated with a thick, sticky substance, suggestive of a viscous bodily secretion.',
	'horsey':  'is quite big and strong-looking, much larger than your typical fruit fly.',
	'icy':     'has a frosted appearance, with a sheen like a layer of frost.',
	'jerky':   'moves in rapid and sudden movements, displaying an unpredictable flight pattern.',
	'kidney':  'has a body shape that is curved, similar to a kidney bean.',
	'leafy':   'has wings that resemble the shape and pattern of leaves.',
	'mushy':   'feels soft to the touch and unusually squishy, unlike the usual firmness.',
	'nerdy':   'has large, prominent eyes that stand out, much like thick-rimmed glasses.',
	'okra':    'features a long, slender body, resembling the shape of an okra pod.',
	'prickly': 'is covered with sharp bristles, giving it a spiky texture.',
	'quacky':  'emits sounds that oddly mimic the quack of a duck.',
	'rusty':   'has a reddish-brown color, much like rusted iron metal.',
	'spicy':   'has chemical defense giving a tingling sensation, similar to spicy food.',
	'tipsy':   'moves in an erratic path, suggesting a lack of coordination, as if intoxicated.',
	'ugly':    'has dull colors and uneven features different from the typical fruit fly.',
	'valley':  'shows deep grooves along its body, creating a landscape of peaks and troughs.',
	'waxy':    'has a thick protective layer that is water resistant and opague.',
	'xanthic': 'has a fluorescent bright yellow coloring.',
	'yucky':   'gives off an unpleasant odor and has a generally unappealing look.',
	'zippy':   'zooms around quickly, darting from one place to another.',

	'common name': 'fruit fly',
	'genus species': 'Drosophila melanogaster',
}



#====================================
# Generate a dictionary of phenotype names by the first letter
#====================================

# have to get names first, because keys will change
phenotype_names = list(phenotype_dict.keys())

# Initialize an empty dictionary to map the first letter of each phenotype name to the full name.
for name in phenotype_names:
	if name in ('common name', 'genus species'):
		continue
	# Map each phenotype name to its first letter in phenotype_dict.
	# If multiple phenotypes start with the same letter, this will keep the last one due to overwriting.
	first_letter = name[0]
	phenotype_dict[first_letter] = name

