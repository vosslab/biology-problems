
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

### ugly code, but works

class GelClass(object):
	def __init__(self):
		self.row = 0
		self.initImage()
		pass

	def initImage(self):
		self.img = Image.new("RGB", (2048,2048), (212,212,212))

	def drawLane(self, subindex, text=""):
		self.row += 1
		sub_band_tree = self.indexToSubSet(self.band_tree, subindex)
		factor = 9
		height = 22 * factor
		rowgap = 5 * factor
		draw1 = ImageDraw.Draw(self.img, "RGB")
		miny = int((self.row-1)*height + rowgap)
		maxx = int((self.row)*height)
		xshift = 300
		fnt = ImageFont.truetype('/Users/vosslab/Library/Fonts/LiberationSansNarrow-Regular.ttf', 72)
		draw1.text((rowgap, miny+20), text, font=fnt, fill="black")
		for band_dict in sub_band_tree:
			start = xshift+band_dict['start']*factor
			end = start + band_dict['width']*factor
			draw1.rectangle(((start, miny), (end, maxx)), fill="blue", outline="black")

	def blankLane(self):
		self.row += 0.3

	def saveImage(self, filename):
		self.img.save(filename, "PNG")

	def getRandomSubSet(self, setsize, subsize):
		subindex = random.sample(xrange(setsize), subsize)
		return set(subindex)

	def indexToSubSet(self, mylist, indices):
		newlist = []
		for i in indices:
			newlist.append(mylist[i])
		return newlist

	def createBandTree(self, total_bands=12):
		min_band_width = 2
		max_band_width = 10
		min_gap = 2
		max_gap = 6
		self.band_tree = []
		start_point = 2
		for i in range(total_bands):
			width = random.randint(min_band_width, max_band_width+1)
			gap = random.randint(min_gap, max_gap+1)
			start_point += gap
			band_dict = {
				'width': width,
				'start': start_point,
			}
			start_point += width
			self.band_tree.append(band_dict)
		return self.band_tree