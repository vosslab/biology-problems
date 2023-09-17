

import sys
import copy
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class RFLPClass:
	#=====================================
	"""Initialize RFLPClass"""
	def __init__(self, num_bands):
		self.num_bands = num_bands
		self.allbands = set(range(self.num_bands))
		self.people = {}
		self.debug = True

	#=====================================
	def create_family(self):
		"""
		This function aims to create unique DNA bands for a family consisting of a mother, a father, and a child.
		The function should adhere to specific criteria to ensure variability and similarity where required.

		Variables:
		- mother: set, DNA bands for the mother
		- father: set, DNA bands for the father
		- child: set, DNA bands for the child
		- allbands: set, all possible DNA bands
		- bothparents: set, intersection of bands between mother and father

		Derived Sets:
		- musthave: set, bands present in child but not in mother
		- ignore: set, bands common between mother and child
		- parent_diffs: set, bands unique to the father when compared to the mother

		Returns:
		- Tuple (mother, father, child) if all criteria are met
		- None otherwise
		"""
		# Sample sizes for mother and father sets. The child set will be derived from these.
		mother_size = int(self.num_bands * random.uniform(0.3, 0.4))
		father_size = int(mother_size * random.uniform(0.9, 1.1))

		# Populate 'mother' and 'father'
		mother = frozenset(random.sample(list(self.allbands), mother_size))
		father = set(random.sample(list(mother), mother_size//2))
		father.update(random.sample(list(self.allbands - mother), father_size - len(father)))
		father = frozenset(father)

		# Generate 'child' using the 'have_baby' function
		child = self.have_baby(mother, father, forced_unique=2)

		# Calculate derived sets
		musthave = child - mother
		ignore = mother.intersection(child)
		parent_diffs = father - mother

		# Check criteria
		if len(musthave) <= 2:
			if self.debug is True:
				print(".. mother=", len(mother), mother)
				print(".. child=", len(child), child)
				print(".. musthave=", len(musthave), musthave)
				print("The child and mother are too similar.")
			return None

		if len(ignore) <= 2:
			if self.debug is True:
				print(".. mother=", len(mother), mother)
				print(".. child=", len(child), child)
				print(".. ignore=", len(ignore), ignore)
				print("The child and mother are too disimilar.")
			return None

		if len(parent_diffs) <= 4:
			if self.debug is True:
				print(".. mother=", len(mother), mother)
				print(".. father=", len(father), father)
				print(".. parent_diffs=", len(parent_diffs), parent_diffs)
				print("The mother and father are too similar.")
			return None

		if abs(len(mother) - len(father)) / len(mother) >= 0.25:
			if self.debug is True:
				print(".. mother=", len(mother), mother)
				print(".. father=", len(father), father)
				print("The mother and father sets have lengths that differ by more than 25%.")
			return None

		if abs(len(mother) - len(child)) / len(mother) >= 0.25:
			if self.debug is True:
				print(".. mother=", len(mother), mother)
				print(".. child=", len(child), child)
				print("The mother and child sets have lengths that differ by more than 25%.")
			return None

		if self.debug is True:
			print(".. mother=", len(mother), mother)
			print(".. father=", len(father), father)
			print(".. child=", len(child), child)

		self.people['mother'] = mother
		self.people['father'] = father
		self.people['child'] = child
		self.people['musthave'] = musthave
		self.people['ignore'] = ignore

		return mother, father, child

	#====================================
	def have_baby(self, mother, father, forced_unique=2):
		child = set()
		# Adding bands from mother and father with 0.5 probability
		child.update(random.sample(list(mother), len(mother)//2))
		child.update(random.sample(list(father), len(father)//2))
		# Removing random bands from child
		removal_count = forced_unique*2
		child -= set(random.sample(list(child), min(removal_count, len(child)-1)))

		# Adding extra unique bands from both parents
		unique_from_mother = random.sample(list(mother - father), forced_unique)
		unique_from_father = random.sample(list(father - mother), forced_unique)
		child.update(unique_from_mother)
		child.update(unique_from_father)
		return frozenset(child)

	#====================================
	def create_additional_males(self, num_males=7):
		# Generate additional male DNA bands
		males_set = set()
		males_set.add(self.people.get('father'))
		musthave = self.people.get('musthave')
		print(".. musthave=", len(musthave), musthave)
		for i, exclude_band in enumerate(list(musthave)):
			male_type_1 = self.create_male_type_1(exclude_band)
			if male_type_1 is not None:
				males_set.add(male_type_1)
				if self.debug is True:
					print(".. exclude_band=", exclude_band)
					print(f".. type 1 male {i+1}=", len(male_type_1), male_type_1)
		print(f"Created {len(males_set)} type 1 males")

		# Generate additional males with random changes in DNA bands
		while len(males_set) < num_males:
			male_type_2 = self.create_male_type_2()
			if male_type_2 is not None:
				males_set.add(male_type_2)
				if self.debug is True:
					print(f".. type 2 male {len(males_set)+1}=", len(male_type_2), male_type_2)
		print(f"Created {len(males_set)} total males")
		males_list = list(males_set)
		random.shuffle(males_list)
		random.shuffle(males_list)
		if self.check_males(males_list) is False:
			return None
		self.people['males_list'] = males_list
		return males_list

	#====================================
	def check_males(self, males_list):
		dadcount = 0
		for i, male in enumerate(males_list):
			if self.is_father(male) is True:
				dadcount += 1
		if dadcount == 0:
			print("no fathers in list")
			return False
		elif dadcount > 1:
			print(f"too many fathers in list: {dadcount}")
			return False
		return True

	#====================================
	def create_male_type_1(self, exclude_band):
		# contains all but one of the must have bands
		musthave = self.people.get('musthave')
		child = self.people.get('child')
		male_type_1 = set(copy.copy(musthave))
		male_type_1.update(random.sample(list(child), len(child)//2+1))
		male_type_1.update(random.sample(list(self.allbands), len(child)//2+1))
		male_type_1.remove(exclude_band)
		if self.is_father(male_type_1) is True:
			return None
		return frozenset(male_type_1)

	#====================================
	def create_male_type_2(self):
		musthave = self.people.get('musthave')
		male_type_2 = set(copy.copy(musthave))
		for i in range(len(self.people.get('child'))+1):
			male_type_2.add(random.choice(list(self.allbands)))
		male_type_2.remove(random.choice(list(musthave)))
		if self.is_father(male_type_2) is True:
			return None
		return frozenset(male_type_2)

	#================
	def make_unknown_males_PNG_image(self):
		# Initialization
		gel_class = GelClass()
		gel_class.createBandTree(self.num_bands)
		gel_class.setTextColumn("Must Have")
		gel_class.drawLane(self.allbands, "allbands")
		gel_class.blankLane()
		gel_class.drawLane(self.people.get('mother'), "Mother")
		gel_class.drawLane(self.people.get('child'), "Child")
		males_list = self.people.get('males_list')
		dadcount = 0
		for i, male in enumerate(males_list):
			if self.is_father(male) is True:
				dadcount += 1
				answer_index = i
			#print(("Male #%d: %s -- %s"%(i+1, str(sorted(male)), isfather)))
			gel_class.drawLane(male, "Male %d"%(i+1))
		if dadcount != 1:
			print("wrong number of fathers")
			sys.exit(1)
		gel_class.blankLane()
		gel_class.drawLane(self.people.get('musthave'), "Must Have")
		gel_class.drawLane(self.people.get('ignore'), "Ignore")
		gel_class.saveImage("males.png")
		print("open males.png")
		return answer_index

	#================
	def make_unknown_males_HTML_table(self):
		# Initialization
		gel_class = GelClassHtml()
		gel_class.createBandTree(self.num_bands)
		gel_class.setTextColumn("musthave")

		mother = self.people.get('mother')
		child = self.people.get('child')
		table = ""
		table += gel_class.tableWidths()
		#table += gel_class.drawLane(list(allbands), "allbands")
		table += gel_class.blankLane()
		table += gel_class.drawLane(sorted(mother), "Mother")
		table += gel_class.drawLane(sorted(child), "Child")
		males_list = self.people.get('males_list')
		dadcount = 0
		for i, male in enumerate(males_list):
			if self.is_father(male) is True:
				dadcount += 1
				answer_index = i
			#print(("Male #%d: %s -- %s"%(i+1, str(sorted(male)), isfather)))
			table += gel_class.drawLane(male, "Male %d"%(i+1))
		if dadcount != 1:
			print("wrong number of fathers")
			return None
		table += gel_class.blankLane()
		if self.debug is True:
			table += gel_class.drawLane(self.people.get('musthave'), "musthave")
			table += gel_class.drawLane(self.people.get('ignore'), "ignore")
		table += "</table>"
		return table, answer_index

	#====================================
	def is_father(self, male):
		#1. Everyone of the child's bands must come from a parent; Account for each band in the child
		#2. Only some bands from each parent are present in the child; A parent's band presence doesn't guarantee it's in the child
		#3. If the child has a band that the mother is missing, it must come from the father
		# Check if the male is the father based on the set difference
		if len(self.people.get('musthave') - male) == 0:
			return True
		return False

	#====================================
	def is_killer(self, blood, victim, suspect):
		#1. All bands in the crime scene sample must come from the victim or the criminal; Account for each band in the blood sample
		#2. All bands from both the criminal and victim are present in the crime scene sample; Suspect is innocent if their band is absent in the sample
		#3. If a band from the crime scene isn't present in the victim, the criminal must have that band

		#killer must have all bands
		if (blood - victim) == (suspect - victim):
			return True
		return False


class GelClass:
	"""Initialize GelClass attributes."""
	def __init__(self):
		self.row = 0
		self.img = None
		self.factor = 13
		self.max_distance = None
		self.xshift = None
		self.basefontsize = 18
		self.fontfile = '/Users/vosslab/Library/Fonts/LiberationSansNarrow-Regular.ttf'
		#self.fontfile = '/Applications/LibreOffice.app/Contents/Resources/fonts/truetype/LiberationSansNarrow-Regular.ttf'

	def setTextColumn(self, biggesttext):
		"""Set the text column based on the biggest text."""
		# Create a dummy image and draw object to measure text size
		img = Image.new('RGB', (1, 1), color='white')
		draw = ImageDraw.Draw(img)

		# Specify the font and size
		fnt = ImageFont.truetype(self.fontfile, self.basefontsize * self.factor)

		# Get bounding box dimensions
		bbox = draw.textbbox((0, 0), biggesttext, font=fnt)
		text_width = bbox[2] - bbox[0]  # Calculate width based on bounding box

		# Set the xshift based on the calculated text width
		self.xshift = text_width + self.factor * 4

	def initImage(self):
		"""Initialize image dimensions."""
		if self.max_distance is not None:
			width = int(round((self.max_distance + 10) * self.factor + self.xshift))
		else:
			width = 2048
		gray = 230
		self.img = Image.new("RGB", (width,4096), (gray,gray,gray))

	def configureLane(self, band_tree, subindex):
		"""Configure sub-band tree based on index."""
		return [band_tree[i] for i in subindex]

	def drawLane(self, subindex, text=""):
		if self.img is None:
			self.initImage()
		sub_band_tree = self.configureLane(self.band_tree, subindex)
		self._draw_lane_graphics(sub_band_tree, text)

	def _draw_lane_graphics(self, sub_band_tree, text):
		"""Helper method to handle lane graphics."""
		self.row += 1  # Increment the row count
		height = 24 * self.factor
		rowgap = 5 * self.factor

		draw1 = ImageDraw.Draw(self.img, "RGB")
		min_y = int((self.row - 1) * height + rowgap)
		max_y = int(self.row * height)

		# Specify the font and size
		font = ImageFont.truetype(self.fontfile, self.basefontsize * self.factor)

		# Get the bounding box dimensions for the text
		bbox = draw1.textbbox((0, 0), text, font=font)

		# Extract height and width from the bounding box
		text_height = bbox[3] - bbox[1]
		text_width = bbox[2] - bbox[0]  # Not used, but can be if needed

		# Calculate the y-shift needed for vertical centering
		#y_shift = (height - text_height) // 2  # Changed from negative to positive for clarity
		y_shift = (height - text_height*2)  # Changed from negative to positive for clarity

		# Calculate the x-shift
		x_shift = self.xshift - text_width  # Derived from bounding box dimensions

		#print("shifts=", x_shift, min_y, y_shift)
		# Draw the text
		draw1.text((x_shift, min_y + y_shift), text, font=font, fill="black")

		for band_dict in sub_band_tree:
			start_x = self.xshift + band_dict['start'] * self.factor
			end_x = start_x + band_dict['width'] * self.factor
			# Draw outline
			w = self.factor // 2
			draw1.rectangle(((start_x - w, min_y - w), (end_x + w, max_y + w)), fill="white")
			# Draw inner box
			cornflower_blue = (80, 119, 190)
			draw1.rectangle(((start_x, min_y), (end_x, max_y)), fill=cornflower_blue)

	def createBandTree(self, total_bands=12):
		"""Create a random band tree."""
		self.band_tree = []
		start_point = 2
		for _ in range(total_bands):
			band_info = self._random_band(start_point)
			start_point += band_info['width'] + band_info['gap']
			self.band_tree.append(band_info)
		self.max_distance = start_point

	def _random_band(self, start):
		"""Generate random band information."""
		min_band_width, max_band_width = 3, 7
		min_gap, max_gap = 3, 12
		width = random.randint(min_band_width, max_band_width)
		gap = random.randint(min_gap, max_gap)
		return {'width': width, 'start': start + gap, 'gap': gap}


	def blankLane(self):
		self.row += 0.3

	def saveImage(self, filename):
		self.img.save(filename, "PNG")

	def getRandomSubSet(self, setsize, subsize):
		subindex = random.sample(range(setsize), subsize)
		return set(subindex)

	def indexToSubSet(self, mylist, indices):
		newlist = []
		for i in indices:
			newlist.append(mylist[i])
		return newlist



class GelClassHtml(GelClass):
	# Override function in parent class
	def setTextColumn(self, biggesttext):
		pass
	# Override function in parent class
	def initImage(self):
		pass
	# Override function in parent class
	def saveImage(self, filename):
		pass

	# Generate colgroup element for HTML table with column widths
	def tableWidths(self):
		space_width = 10
		# Initialize table and first colgroup
		colgroup = '<table cellspacing="0" border="0"> '
		colgroup += '<colgroup width="{0}"></colgroup> '.format(space_width)

		# Generate colgroups based on band widths
		for band in self.band_tree:
			w = int(band['width'] * 1.5 + 2)
			colgroup += '<colgroup width="{0}"></colgroup> '.format(space_width)
			colgroup += '<colgroup width="{0}"></colgroup> '.format(w)
		# Add final colgroup
		colgroup += '<colgroup width="{0}"></colgroup> '.format(space_width)
		return colgroup

	# Create a table cell block with given fill and border color
	def tdBlock(self, fill_color="#E0E0E0", border_color="#E0E0E0"):
		td_block =  f' <td style="border-top: 1px solid {border_color}; '
		td_block += f'border-bottom: 1px solid {border_color}; '
		td_block += f'border-left: 1px solid {border_color}; '
		td_block += f'border-right: 1px solid {border_color}" '
		td_block += f'bgcolor="{fill_color}"><br/></td> '
		return td_block

	# Create a blank lane for the gel with proper column span
	def blankLane(self, fill_color='#E0E0E0'):
		total_bands = len(self.band_tree)
		lane = '<tr> '
		lane += f'  <td style="border-top: 1px solid {fill_color};'
		lane += f' border-bottom: 1px solid {fill_color};'
		lane += f' border-left: 1px solid {fill_color};'
		lane += f' border-right: 1px solid {fill_color}"'
		lane += f' colspan="{2 * total_bands + 3}"'
		lane += f' bgcolor="{fill_color}" height="10"></td> '
		lane += '</tr> '
		return lane

	# Draw a single lane of the gel based on band subset indices
	def drawLane(self, subindex, text=""):
		subindex = list(subindex)
		lane = '<tr> '
		lane += self.tdBlock()
		lane += '  <td>{0}</td> '.format(text)
		total_bands = len(self.band_tree)

		for i in range(total_bands):
			if i in subindex:
				lane += self.tdBlock()
				lane += self.tdBlock("#6495ED")
			else:
				lane += self.tdBlock()
				lane += self.tdBlock()

		# Finalize lane with a blank cell block
		lane += self.tdBlock()
		lane += '</tr>'
		return lane
