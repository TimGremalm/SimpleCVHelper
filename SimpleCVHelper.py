# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from SimpleCV import Image
from numpy import rot90
import math

def tableImages(imageList, numCols=0, outWidth=0, outHeight=0):
	numImages = len(imageList)
	if numCols == 0:
		#A rough number of how many coloms could fit, if the images are equal in size this should work fine
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
	if outWidth == 0: #Check args, otherwise take the first image size
		outWidth = imageList[0].width
	if outHeight == 0:
		outHeight = imageList[0].height

	#Get the output scaling
	imgX, imgY = scaleSize(rows.width, rows.height, outWidth, outHeight)

	return(rows.resize(imgX, imgY))

def scaleSize(inputX, inputY, outputX, outputY):
	ratioXY = float(inputX) / float(inputY)
	ratioYX = float(inputY) / float(inputX)

	#Create two sizes
	sideAWidth = outputX
	sidaAHeight = outputX*ratioYX

	sideBWidth = outputY*ratioXY
	sideBHeight = outputY

	#Check which size will fit the output frame
	if sidaAHeight <= outputY:
		return(int(sideAWidth), int(sidaAHeight))
	else:
		return(int(sideBWidth), int(sideBHeight))

def testHaar(img, listHaar):
	outList = []
	for haarFile in listHaar:
		tmpImg = img.copy()
		tmpHaar = tmpImg.grayscale().findHaarFeatures(haarFile)
		tmpImg.draw(tmpHaar, width=3)
		tmpImg.save('tmp.png')
		tmpImg2 = Image('tmp.png')
		outList.append(tmpImg2)
	return(outList)

def testHog(img):
	hog = cv2.HOGDescriptor()
	hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
	imgOut = img.copy()
	found,foundweight = hog.detectMultiScale(img.grayscale().getNumpyCv2() , winStride=(4,4), padding=(8,8), scale=1.05)
	for x, y, w, h in found:
		#x = imgOut.width - x
		#y = imgOut.height - y
		#x,y = y,x
		imgOut.drawRectangle(x=x, y=y, w=w, h=h, width=3)
	return(imgOut)

