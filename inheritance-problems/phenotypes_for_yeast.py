


phenotype_description_dict = {
	'amber':     'cells develop a rich yellow-orange pigmentation, giving the colony a warm, amber hue.',
	'bubbly':    'produces excessive gas bubbles during growth, causing foamy appearance of the media.',
	'clumpy':    'grows in dense, irregular clusters, with cells clumping together rather than spreading smoothly.',
	'doubled':   'cells display double or multiple budding, with several buds emerging simultaneously.',
	'elephant':  'cells absorb excessive amounts of liquid, resulting in giant, swollen cells.',
	'fuzzy':     'colonies are covered in soft, fine filaments, giving them a fuzzy, cotton-like texture.',
	'gloomy':    'produces dark, matte colonies with a shadowy and somber appearance.',
	'hairy':     'cells develop long, thread-like filaments that extend outward, creating a hairy, shaggy texture on the colony.',
	'ivory':    'forms pale, off-white colonies that stand out from the typical beige yeast color.',
	'jeweled':   'colonies appear dotted with tiny, iridescent spots that sparkle under light.',
	'knotted':   'cells grow in twisted, coiled shapes, resulting in a knotted or gnarled appearance.',
	'lavender':  'colonies are light purple, with a soft lavender hue that is unusual for yeast.',
	'militant':  'colonies are small, dense, and secrete compounds that inhibit the growth of nearby colonies.',
	'nude':      'cells have an unusually smooth surface with no visible external features or textures.',
	'opal':      'colonies are a distinct green color with a subtle, opalescent sheen.',
	'pebble':    'produces colonies with a rough, uneven surface that resembles a collection of tiny pebbles.',
	'quilt':     'cells arrange themselves in a patchy, quilt-like pattern across the colony, creating a mosaic effect.',
	'rusty':     'colonies develop a reddish-brown pigmentation, reminiscent of rusted metal.',
	'stringy':   'produces a sticky, stretchy biofilm that forms thin, stringy connections between cells.',
	'toxic':     'secretes a toxic compound that inhibits or kills other microbial colonies nearby.',
	'uncut':     'buds remain attached to the parent cells, forming a large, interconnected colony network.',
	'vacuolex': 'cells contain unusually large, dark-stained vacuoles that occupy most of the cell.',
	'webbed':    'colonies produce delicate, web-like strands that connect neighboring colonies in a cobweb pattern.',
	'xenon':   'cells emit a faint glow under UV light, as if they were fluorescent.',
	'yolk':      'cells develop a dense, yellowish core that resembles an egg yolk when viewed under a microscope.',
	'zippy':     'exhibits accelerated growth at elevated temperatures, outpacing other strains under warm conditions.',
}


#====================================
# Generate a dictionary of phenotype names by the first letter
#====================================

# Create a list of phenotype names by extracting the keys from phenotype_description_dict.
phenotype_names = list(phenotype_description_dict.keys())

# Initialize an empty dictionary to map the first letter of each phenotype name to the full name.
phenotype_dict = {}
for name in phenotype_names:
	# Map each phenotype name to its first letter in phenotype_dict.
	# If multiple phenotypes start with the same letter, this will keep the last one due to overwriting.
	phenotype_dict[name[0]] = name

# Clean up the temporary list to free up memory, as it's no longer needed after creating phenotype_dict.
del phenotype_names
