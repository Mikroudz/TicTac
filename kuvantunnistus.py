import cv2
import numpy as np
import imutils
import urllib.request
from skimage import exposure
from skimage import io

def detectShape(c):
    shape = "empty or not found"
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.03 * peri, True)

    if len(approx) == 3:

        shape = "X"
    elif len(approx) > 6 and cv2.contourArea(c) > 40:
        shape = "O"
    else:
        shape = "tyhja"
    return shape

def grapURimage(url):

    resp = urllib.request.urlopen(url)

    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

def detectGame(playerType):
    #src = cv2.imread('testikuvat/current.jpg') #kuva tiedostosta
    src = grapURimage("http://192.168.100.10:4242/current.jpg?type=color")

    img = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    img = exposure.rescale_intensity(img, out_range = (0, 255))
    img = cv2.fastNlMeansDenoising(img, None, 9, 13)
    tresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,115,1)

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
        approx = cv2.approxPolyDP(c, 0.1 * peri, True)

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
    warp_gray = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)
    warp_gray = exposure.rescale_intensity(warp_gray, out_range = (0, 255))
    #warp_gray = cv2.bilateralFilter(warp_gray, 2, 100, 100)
    #warp_gray = cv2.threshold(warp_gray, 100, 255, cv2.THRESH_BINARY)[1]
    warp_gray = cv2.fastNlMeansDenoising(warp_gray, None, 9, 13)

    warp_tresh = cv2.adaptiveThreshold(warp_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,21,7)

    warp_laplacian = cv2.Laplacian(warp_tresh,cv2.CV_8U)

    warp_absd = cv2.convertScaleAbs(warp_laplacian)
    warp_edged = cv2.Canny(warp_tresh, 30,150, apertureSize = 3)

    kernel = np.ones((3,3),np.uint8)
    warp_edged = cv2.dilate(warp_edged,kernel, iterations = 1)
    kernel = np.ones((2,2),np.uint8)
    warp_edged = cv2.erode(warp_edged,kernel,iterations = 1)
    positions = [['','',''],
                  ['','',''],
                   ['','','']]
    places = []
    for i in range(3):
        for j in range(3):
            places.append(warp_absd[int(i*maxHeight/3):int((i+1)*maxHeight/3),int(j*maxWidth/3):int((j+1)*maxWidth/3)].copy())

    for i in range(9):
        cnts = cv2.findContours(places[i], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
        shape = []
        for c in cnts:
            if cv2.contourArea(c) > 40:
                shape.append(detectShape(c))
        count_x = shape.count('X')
        count_o = shape.count('O')

        circles = cv2.HoughCircles(places[i],cv2.HOUGH_GRADIENT, 1.5, 20)
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                cv2.circle(warp, (x+i % 3 * (maxWidth // 3), y+i // 3 * (maxHeight // 3)), r, (0, 255, 0), 4)

        if count_o > count_x and count_o > 1:
            shape = 'O'
            if playerType == 'O':
                positions[i // 3][i % 3] = 'O'
        elif count_o < count_x and count_x > 1:
            shape = 'X'
            if playerType == 'X':
                positions[i % 3][i // 3] = 'X'
        else:
            shape = 'Tyhja'
        tX = i % 3 * (maxWidth / 3) + (35 if shape[0] == "X" or shape[0] == "O" else 10)
        tY = i // 3 * (maxHeight / 3) + 50
        cv2.putText(warp, shape, (int(tX), int(tY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Play_area',warp)
    cv2.imshow('final',warp_absd)
    cv2.imshow('img',laplacian)
    return positions
print(detectGame('O'))
cv2.waitKey(0)
cv2.destroyAllWindows()
