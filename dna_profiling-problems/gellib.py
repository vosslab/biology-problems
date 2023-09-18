

import sys
import copy
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class GelClass:
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


class GelClassImage(GelClass):
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

	def blankLane(self):
		self.row += 0.3

	def saveImage(self, filename):
		self.img.save(filename, "PNG")


class GelClassHtml(GelClass):
	"""Initialize GelClass attributes."""
	def __init__(self):
		self.table = None
		self.row = 0

	# Generate colgroup element for HTML table with column widths
	def tableWidths(self):
		space_width = 5
		# Initialize table and first colgroup
		colgroup = '<table cellspacing="0" border="0"> '
		colgroup += '<colgroup width="{0}"></colgroup> '.format(space_width)
		# Add flexible line for text labels
		colgroup += '<colgroup></colgroup> '
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
