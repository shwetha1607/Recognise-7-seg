import cv2
from imutils.perspective import four_point_transform
import imutils
import numpy as np
from imutils import contours


def loc_four_point_transform(image, pts):
    rect = pts
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    src = np.array(rect)

    m = cv2.getPerspectiveTransform(src, dst)
    ret_warped = cv2.warpPerspective(image, m, (maxWidth, maxHeight))

    return ret_warped


#video = cv2.VideoCapture(0)

#check, frame = video.read()
#cv2.imshow("webcam", frame)
#cv2.imwrite("webcam2.jpg", frame)
#cv2.waitKey(0)

frame = cv2.imread("webcam2.jpg")

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (11, 11), 0)
thresh = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY)[1]

thresh = cv2.erode(thresh, None, iterations=4)
thresh = cv2.dilate(thresh, None, iterations=10)
thresh = cv2.erode(thresh, None, iterations=2)
cv2.imshow("final thresh", thresh)
cv2.waitKey(0)

find_contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
all_contours = imutils.grab_contours(find_contours)
all_points = []
print("no of contours : " + str(len(all_contours)))
digitCnts = []

for c in all_contours:
    # compute the bounding box of the contour
    (x, y, w, h) = cv2.boundingRect(c)
    cnt = cv2.rectangle(thresh, (x, y), (x+w, y+h), (255, 255, 255), 3)
    cv2.imshow("counter wise", cnt)
    cv2.waitKey(0)
    print(x, y, w, h)

    if w >= 50 and h >= 100:
        digitCnts.append(c)


digitCnts = contours.sort_contours(digitCnts, method="left-to-right")[0]

for c in digitCnts:
    (x, y, w, h) = cv2.boundingRect(c)
    all_points.extend([(x, y), (x + w, y), (x + w, y + h), (x, y + h)])


points = [all_points[0], all_points[5], all_points[6], all_points[7]]
print(points)
cv2.rectangle(frame, points[0], points[2], (0, 255, 0), 3)
cv2.imshow("with box", frame)
cv2.waitKey(0)
points = np.array(points)

warped = four_point_transform(frame, points)
cv2.imshow("top view", warped)
cv2.waitKey(0)

cv2.destroyAllWindows()

#video.release()



