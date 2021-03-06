import cv2
import numpy as np
import imutils
from imutils import contours

DIGITS_LOOKUP = {
    (1, 1, 1, 0, 1, 1, 1): 0,
    (0, 0, 1, 0, 0, 1, 0): 1,
    (1, 0, 1, 1, 1, 0, 1): 2,
    (1, 0, 1, 1, 0, 1, 1): 3,
    (0, 1, 1, 1, 0, 1, 0): 4,
    (1, 1, 0, 1, 0, 1, 1): 5,
    (1, 1, 0, 1, 1, 1, 1): 6,
    (1, 0, 1, 0, 0, 1, 0): 7,
    (1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 1): 9,
}

image = cv2.imread('/home/pi/Pictures/trail/20190223-153407.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("gray", gray)
cv2.waitKey(0)

thresh = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY)[1]
cv2.imshow("thresh", thresh)
cv2.waitKey(0)

thresh = cv2.dilate(thresh, None, iterations=1)
thresh = cv2.erode(thresh, None, iterations=1)
cv2.imshow("bright", thresh)
cv2.waitKey(0)

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

digitCnts = []

for c in cnts:
	# compute the bounding box of the contour
	(x, y, w, h) = cv2.boundingRect(c)
	print(x, y, w, h)
	cv2.rectangle(thresh, (x, y), (x+w, y+h), (0, 0, 0), 1)
	cv2.imshow("box", thresh)
	cv2.waitKey(0)
	# if the contour is sufficiently large, it must be a digit
	# first condition for digit 1
	if (3 <= w <= 6) and (14 <= h <= 25):
		digitCnts.append(c)
	if (5 <= w <= 15) and (14 <= h <= 25):
		digitCnts.append(c)

digitCnts = contours.sort_contours(digitCnts, method="left-to-right")[0]
digits = []

for c in digitCnts:
	(x, y, w, h) = cv2.boundingRect(c)
	print(x, y, w, h)
	if (3 <= w <= 6) and (14 <= h <= 25):
		on = [0, 0, 1, 0, 0, 1, 0]
	else:
		roi = thresh[y:y+h, x:x+w]
		cv2.imshow("roi", roi)
		cv2.waitKey(0)
		(roiH, roiW) = roi.shape
		print(roiH, roiW)

		(dW, dH) = (int(roiW * 0.3), int(roiH * 0.2))
		dHC = int(roiH * 0.1)

		segments = [
			((0, 0), (w, dH)),  # top
			((0, 0), (dW, h // 2)),  # top-left
			((w - dW, 0), (w, h // 2)),  # top-right
			((0, (h // 2) - dHC), (w, (h // 2) + dHC)),  # center
			((0, h // 2), (dW, h)),  # bottom-left
			((w - dW, h // 2), (w, h)),  # bottom-right
			((0, h - dH), (w, h))  # bottom
		]

		on = [0] * len(segments)

		for (i, ((xs, ys), (xf, yf))) in enumerate(segments):

	                segRoi = roi[ys:yf, xs:xf]
        	        cv2.imshow("segroi", segRoi)
                	cv2.waitKey(0)
	                no_of_pixels = cv2.countNonZero(segRoi)
        	        area = (xf - xs) * (yf - ys)

                	if no_of_pixels / float(area) >= 0.5:
                        	on[i] = 1

	                print(on)

	digit = DIGITS_LOOKUP.get(tuple(on), -1)
	digits.append(digit)
	cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
	cv2.putText(image, str(digit), (x - 10, y - 10),
		cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)

print(u"{}{}".format(*digits))
cv2.imshow("final", image)
cv2.waitKey(0)

cv2.destroyAllWindows()
