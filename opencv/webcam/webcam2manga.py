# -*- coding: utf-8 -*-
import cv2
import numpy

def filters(inputImg):
    edge= cv2.Canny(inputImg,80,120)
    nega = cv2.bitwise_not(edge)

    result = screen.copy()
    result[inputImg<80] = 0
    result[inputImg>160]=255
    alpha = 0.5
    result = cv2.addWeighted(nega,alpha,result,1-alpha,0.0)
    (thresh,result)=cv2.threshold(result,200,255,cv2.THRESH_BINARY)
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
    cv2.namedWindow("Manga Capture", cv2.WINDOW_AUTOSIZE)

    i = 0
    while True:
        ret, im = capture.read()
        if ret == False:
            continue

        result = filters(cv2.cvtColor(im, cv2.COLOR_RGB2GRAY))
        cv2.imshow("Manga Capture", result)
        #cv2.imwrite("output/{0:08d}.png".format(i), result)
        #i += 1
        if cv2.waitKey(33) >= 0:
            break
    capture.release()
    cv2.destroyAllWindows()

