# -*- coding: utf-8 -*-
import cv2

if __name__=="__main__":
    capture = cv2.VideoCapture(0)
    if capture.isOpened() is False:
        raise("IO Error")
    cv2.namedWindow("Capture", cv2.WINDOW_AUTOSIZE)

    while(capture.isOpened()):
        ret, image = capture.read()
        if ret==True:
            cv2.imshow("Capture", image)
            # any key
            if cv2.waitKey(33) >= 0:
                break
        else:
            break
    capture.release()
    cv2.destroyAllWindows()

