import cv2
import numpy as np
import imutils
from skimage import exposure

src = cv2.imread('testikuvat/current.jpg')

def detectShape(c):
    shape = "empty or not found"
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)

    if len(approx) == 3:
        shape = "triangle"
    elif len(approx) == 4:
        shape = "square"
    else:
        shape = "circle"
    return shape

img = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
img = cv2.fastNlMeansDenoising(img, None, 9, 13)
denoiced = cv2.GaussianBlur(img, (3, 3), 0).astype('uint8')
tresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

laplacian = cv2.Laplacian(tresh,cv2.CV_8U)

absd = cv2.convertScaleAbs(laplacian)

edged = cv2.Canny(absd, 30,150, apertureSize = 3)

kernel = np.ones((3,3),np.uint8)
edged = cv2.dilate(edged,kernel, iterations = 2)
kernel = np.ones((3,3),np.uint8)
edged = cv2.erode(edged,kernel,iterations = 1)

cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
print(len(cnts))
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
screenCnt = None

# loop over our contours
for c in cnts:
	# approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

	# if our approximated contour has four points, then
	# we can assume that we have found our screen
    if len(approx) == 4:
        screenCnt = approx
        break

#Piirtää alueen alkuperäiseen kuvaan
#cv2.drawContours(src, [screenCnt], -1, (0, 255, 0), 3)

pts = screenCnt.reshape(4, 2)
rect = np.zeros((4, 2), dtype = "float32")

s = pts.sum(axis = 1)
rect[0] = pts[np.argmin(s)]
rect[2] = pts[np.argmax(s)]

diff = np.diff(pts, axis = 1)
rect[1] = pts[np.argmin(diff)]
rect[3] = pts[np.argmax(diff)]

(tl, tr, br, bl) = rect
widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

maxWidth = max(int(widthA), int(widthB))
maxHeight = max(int(heightA), int(heightB))

dst = np.array([
	[0, 0],
	[maxWidth - 1, 0],
	[maxWidth - 1, maxHeight - 1],
	[0, maxHeight - 1]], dtype = "float32")

M = cv2.getPerspectiveTransform(rect, dst)
warp = cv2.warpPerspective(src, M, (maxWidth, maxHeight))
print(maxWidth)
print(maxHeight)

#Korjatun ja varpatun kuvan syynäyksen aloitus
warp = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)
warp = exposure.rescale_intensity(warp, out_range = (0, 255))
warp_tresh = cv2.adaptiveThreshold(warp,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,101,1)
warp_laplacian = cv2.Laplacian(warp_tresh,cv2.CV_8U)

warp_absd = cv2.convertScaleAbs(warp_laplacian)

x = []
for i in range(3):
    for j in range(3):
        x.append(warp_absd[int(i*maxHeight/3):int((i+1)*maxHeight/3),int(j*maxWidth/3):int((j+1)*maxWidth/3)].copy())

cnts = cv2.findContours(x[6].copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

for c in cnts:
    print(detectShape(c))

cv2.imshow('part',x[6])
cv2.imshow('gray',warp_tresh)
cv2.imshow('image',src)
cv2.waitKey(0)
cv2.destroyAllWindows()
