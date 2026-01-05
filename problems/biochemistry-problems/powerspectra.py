#!/usr/bin/env python3

import numpy
import scipy.fftpack
import scipy.ndimage
from PIL import Image

def real_fft2d(*args, **kwargs):
	return scipy.fftpack.fft2(*args, **kwargs)

def inverse_real_fft2d(*args, **kwargs):
	return scipy.fftpack.ifft2(*args, **kwargs).real

def swap_quadrants(a):
	return numpy.fft.fftshift(a)

def center_mask(a, mask_radius):
	cy = a.shape[0] // 2
	cx = a.shape[1] // 2
	yy, xx = numpy.ogrid[:a.shape[0], :a.shape[1]]
	mask = (yy - cy) ** 2 + (xx - cx) ** 2 <= mask_radius ** 2
	a[mask] = 0
	return a

def clip_power(a, thresh):
	return numpy.clip(a, -thresh, thresh)

#=========================
def getImageInfo(im):
	"""
	prints out image information good for debugging
	"""
	avg1 = im.mean()
	stdev1 = im.std()
	min1 = im.min()
	max1 = im.max()

	return avg1,stdev1,min1,max1

#=========================
def printImageInfo(im):
	"""
	prints out image information good for debugging
	"""
	#print " ... size: ",im.shape
	#print " ... sum:  ",im.sum()
	avg1,stdev1,min1,max1 = getImageInfo(im)

	if len(im.shape) == 2:
		print(f"Image: {im.shape[0]} x {im.shape[1]} - type {im.dtype}")
	elif len(im.shape) == 1:
		print(f"Image: {im.shape[0]} - type {im.dtype}")
	#print " ... avg:  %.2e +- %.2e"%(avg1, stdev1)
	#print " ... range: %.2e <> %.2e"%(min1, max1)
	print(f" ... avg:  {avg1:.4f} +- {stdev1:.4f}")
	print(f" ... range: {min1:.4f} <> {max1:.4f}")

	return avg1,stdev1,min1,max1

#=========================
def normalizeImage(img, stdevLimit=3.0, minlevel=0.0, maxlevel=255.0, trim=0.0):
	"""
	Normalizes numpy to fit into an image format
	that is values between 0 (minlevel) and 255 (maxlevel).
	"""
	#mid = cutEdges(img,trim)
	imrange = maxlevel - minlevel
	#GET IMAGE STATS
	avg1 = img.mean()
	stdev1 = img.std()
	min1 = img.min()
	max1 = img.max()
	#print avg1, stdev1, min1, max1

	#IF MIN/MAX are too high set them to smaller values
	if (min1 < avg1-stdevLimit*stdev1):
		min1 = avg1-stdevLimit*stdev1
	if (max1 > avg1+stdevLimit*stdev1):
		max1 = avg1+stdevLimit*stdev1

	if min1 == max1:
		#case of image == constant
		return img - min1

	if abs(min1) < 0.01 and abs(max1 - 1.0) < 0.01:
		#we have a mask-like object
		return img * 255
	#print min1, max1

	img = (img - min1)/(max1 - min1)*imrange + minlevel
	img = numpy.where(img > maxlevel, 255.0, img)
	img = numpy.where(img < minlevel,   0.0, img)

	return img

shapes = []

def power(a, mask_radius=1.0, thresh=3):
	fft = real_fft2d(a)
	pow = numpy.absolute(fft)
	### neil half pixel shift or powerspectra are not centered!
	pow = scipy.ndimage.shift(pow, (-1, -1), order=1, mode='wrap')
	try:
		pow = numpy.log(pow)
	except OverflowError:
		pow = numpy.log(pow+1e-20)
	except:
		print('numpy.log failed, bypass')
		pass
	pow = swap_quadrants(pow)

	mask_radius = int(mask_radius / 100.0 * pow.shape[0])
	if mask_radius:
		center_mask(pow, mask_radius)

	return clip_power(pow,thresh)


def frame_constant(a, shape, cval=0):
	b = numpy.ones(shape, dtype=a.dtype)*cval
	delta = (numpy.array(b.shape) - numpy.array(a.shape))
	dy = delta[0] // 2
	dx = delta[1] // 2
	my = a.shape[0] + dy
	mx = a.shape[1] + dx
	b[dy:my, dx:mx] = a
	return b


if __name__ == '__main__':
	square = numpy.ones((128,128), dtype=numpy.float64)
	s = frame_constant(square, (256,256))
	printImageInfo(s)
	img = Image.fromarray(normalizeImage(s), 'RGB')
	img.show()	
	S = scipy.fftpack.fft2(s)
	
	img = Image.fromarray(S, 'RGB')
	img.show()
