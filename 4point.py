import numpy as np
import cv2
from imutils.perspective import four_point_transform


def order_pts(pts):

    (tl, tr, br, bl) = pts
    print((tl, tr, br, bl))

    rect = np.zeros((4, 2), dtype="float32")
    print(rect)

    s = np.sum(pts, axis=1)
    print(s)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    print(rect)


pts = [[0, 0], [3, 1], [3, 0], [0, 1]]
order_pts(pts)
