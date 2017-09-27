# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from SimpleCV import Image
from numpy import rot90
import math
import time

def tableImages(imageList, numCols=0, outWidth=0, outHeight=0):
	numImages = len(imageList)
	if numCols == 0:
		numCols = math.ceil(math.sqrt(numImages))

	imgCount = 0
	rows = None
	currentRow = None
	for img in imageList:
		imgCount = imgCount + 1
		if imgCount % numCols == 1 or numCols == 1: #new row
			currentRow = img
		else: #fill up row
			currentRow = currentRow.sideBySide(img)
		if imgCount % numCols == 0 or imgCount == numImages: #end of row
			if imgCount == numCols: #first row
				rows = currentRow
			else:
				rows = rows.sideBySide(currentRow, side='bottom')
	if outWidth == 0:
		outWidth = imageList[0].width
	if outHeight == 0:
		outHeight = imageList[0].height
	print('{} {}'.format(outWidth, outHeight))

	return(rows.adaptiveScale((outWidth, outHeight), fit=True))

