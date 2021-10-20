
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
		print(".....")
		print(self.band_tree)
		print(subindex)
		sub_band_tree = self.indexToSubSet(self.band_tree, subindex)
		print(sub_band_tree)
		print(".....")
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
		subindex = random.sample(range(setsize), subsize)
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

class GelClassHtml(GelClass):
	def setTextColumn(self, biggesttext):
		pass
	def initImage(self):
		pass

	def tableWidths(self):
		space_width = 10
		colgroup = '<table cellspacing="0" border="0"> '
		colgroup += '<colgroup width="{0}"></colgroup> '.format(space_width)
		colgroup += '<colgroup></colgroup> '
		for band in self.band_tree:
			w = int(band['width']*1.5 + 2)
			colgroup += '<colgroup width="{0}"></colgroup> '.format(space_width)
			colgroup += '<colgroup width="{0}"></colgroup> '.format(w)
		colgroup += '<colgroup width="{0}"></colgroup> '.format(space_width)
		return colgroup


	def tdBlock(self, fill_color="#E0E0E0", border_color="#E0E0E0"):
		return '  <td style="border-top: 1px solid {0}; border-bottom: 1px solid {0}; border-left: 1px solid {0}; border-right: 1px solid {0}" bgcolor="{1}"><br/></td> '.format(border_color, fill_color)

	def blankLane(self):
		total_bands = len(self.band_tree)
		lane = '<tr> '
		lane += '  <td style="border-top: 1px solid {0}; border-bottom: 1px solid {0}; border-left: 1px solid {0}; border-right: 1px solid {0}" colspan="{1:d}" bgcolor="{0}" height="10"></td> '.format("#E0E0E0", 2*total_bands+3)
		lane += '</tr> '
		return lane

	def drawLane(self, subindex, text=""):
		#sub_band_tree = self.indexToSubSet(self.band_tree, subindex)
		subindex = list(subindex)
		#print(subindex)
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
		lane += self.tdBlock()
		lane += '</tr>'
		return lane

	def saveImage(self, filename):
		pass

