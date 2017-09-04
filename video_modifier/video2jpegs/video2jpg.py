#!/usr/bin/env python

import numpy as np
import os, sys
import argparse
sys.path.append("/usr/lib//python2.7/dist-packages/")
import cv2

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--in', dest='infile', help='input file', required=True)
parser.add_argument('-o', '--out', dest='outdir', help='output dir', required=True)
args = parser.parse_args()

if not os.path.isdir(args.outdir): os.makedirs(args.outdir)

cap = cv2.VideoCapture(args.infile)
fwidth  = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
fheight = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
fcount  = cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
fps     = cap.get(cv2.cv.CV_CAP_PROP_FPS)
print ("CV_CAP_PROP_FRAME_WIDTH  : " + str(fwidth))
print ("CV_CAP_PROP_FRAME_HEIGHT : " + str(fheight))
print ("CV_CAP_PROP_FRAME_COUNT  : " + str(fcount))
print ("CV_CAP_PROP_FPS          : " + str(fps))

fid = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret: break
    imgfile = os.path.join(args.outdir, "{:08d}".format(fid) + ".jpg")
    cv2.imwrite(imgfile, frame)
    print ('saved: ' + imgfile)
    fid += 1
cap.release()
