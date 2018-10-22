
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

### ugly code, but works

class GelClass(object):
	def __init__(self):
		self.row = 0
		self.img = None
		self.factor = 13
		self.max_distance = None
		self.xshift = None
		self.basefontsize = 18
		self.fontfile = '/Users/vosslab/Library/Fonts/LiberationSansNarrow-Regular.ttf'
		pass

	def setTextColumn(self, biggesttext):
		fnt = ImageFont.truetype(self.fontfile, self.basefontsize*self.factor)
		textsize = fnt.getsize(biggesttext)
		self.xshift = textsize[0] + self.factor*4

	def initImage(self):
		if self.max_distance is not None:
			width = (self.max_distance + 10) * self.factor + self.xshift 
		else:
			width = 2048
		gray = 230
		self.img = Image.new("RGB", (width,4096), (gray,gray,gray))

	def drawLane(self, subindex, text=""):
		if self.img is None:
			self.initImage()
		self.row += 1
		sub_band_tree = self.indexToSubSet(self.band_tree, subindex)
		height = 24 * self.factor
		rowgap = 5 * self.factor
		draw1 = ImageDraw.Draw(self.img, "RGB")
		miny = int((self.row-1)*height + rowgap)
		maxx = int((self.row)*height)
		fnt = ImageFont.truetype(self.fontfile, self.basefontsize*self.factor)
		textsize = fnt.getsize(text)
		yshift = -(height - textsize[1])//2
		#print "y", height, yshift, textsize
		xshift = self.xshift - textsize[0]
		#print "x", self.xshift, xshift, textsize
		draw1.text((xshift, miny+yshift), text, font=fnt, fill="black")
		for band_dict in sub_band_tree:
			start = self.xshift+band_dict['start']*self.factor
			end = start + band_dict['width']*self.factor
			#outline
			w = self.factor//2
			draw1.rectangle(((start-w, miny-w), (end+w, maxx+w)), fill="white")
			#inner box
			cornflower_blue = (80,119,190)
			draw1.rectangle(((start, miny), (end, maxx)), fill=cornflower_blue)

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
		min_band_width = 3
		max_band_width = 7
		min_gap = 3
		max_gap = 12
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
			self.max_distance = start_point + gap
			self.band_tree.append(band_dict)
		return self.band_tree





