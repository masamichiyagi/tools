# -*- coding: utf-8 -*-
import cv2
import numpy as np

def filters(inputImg):
    kernel = np.ones((15,3), np.uint8)
    erosion = cv2.erode(inputImg,kernel, iterations = 1)
    dilation = cv2.dilate(erosion, kernel, iterations = 1)
    kernel = np.ones((3,15), np.uint8)
    erosion = cv2.erode(dilation, kernel, iterations = 1)
    result = cv2.dilate(erosion, kernel, iterations = 1)

    return result

if __name__ == "__main__":
    print("opencv:Version is", cv2.__version__)
    if '3.1.0' == cv2.__version__:
        screen = cv2.imread("screen.png",cv2.IMREAD_GRAYSCALE)
    else:
        screen = cv2.imread("screen.png",cv2.CV_LOAD_IMAGE_GRAYSCALE)

    capture = cv2.VideoCapture(0)
    if capture.isOpened() is False:
        raise("IO Error")
    cv2.namedWindow("Capture", cv2.WINDOW_AUTOSIZE)
    i = 0
    while True:
        ret, image = capture.read()
        if ret == False:
            continue
        result = filters(image)
        cv2.imshow("Capture", result)
        #cv2.imwrite("output/{0:08d}.png".format(i), result)
        #i += 1
        if cv2.waitKey(33) >= 0:
            break
    capture.release()
    cv2.destroyAllWindows()

