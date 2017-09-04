#!/usr/bin/env python

import numpy as np
import os, sys, glob, colorsys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2
import argparse

LABEL_COLOR_NUM = 10

FONTFACES = (
    cv2.FONT_HERSHEY_SIMPLEX,
    cv2.FONT_HERSHEY_PLAIN,
    cv2.FONT_HERSHEY_DUPLEX,
    cv2.FONT_HERSHEY_COMPLEX,
    cv2.FONT_HERSHEY_TRIPLEX,
    cv2.FONT_HERSHEY_COMPLEX_SMALL,
    cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
    cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
    cv2.FONT_ITALIC );


def labelToColor(label):
    hseed = hash(label)
    h = hseed % LABEL_COLOR_NUM / float(LABEL_COLOR_NUM)
    rgba = [int(x * 255) for x in colorsys.hsv_to_rgb(*(h, 0.8, 0.5))]
    return rgba

parser = argparse.ArgumentParser(description='Faster R-CNN')
parser.add_argument('-i', '--imgdir',  dest='imgdir',  help='img directory', required=True)
parser.add_argument('-o', '--output',  dest='output',  help='output filename', required=True)
parser.add_argument('-f', '--fps',  dest='fps',  help='frame rate', required=False)
args = parser.parse_args()

fontface = FONTFACES[0] | FONTFACES[8]
fontsize = 0.6
fonttick = 1

# open cv 3.1 has no "cv2.cv" -> please define CV_AA.
fourcc = cv2.cv.CV_FOURCC(*'XVID')
#fourcc = cv2.VideoWriter_fourcc(*'XVID')

fwidth = 1920
fheight = 1080
fps = 30
if not (args.fps):
    fps = 30
else:
    fps = int(args.fps)

out = None # cv2.VideoWriter(args.output, fourcc, 30, (int(fwidth), int(fheight)))
    
imgFiles = glob.glob(os.path.join(args.imgdir, '*.jpg'))
imgFiles.sort()

for imgfile in imgFiles:
    try:
        im = cv2.imread(imgfile)
        if not (out):
            fheight, fwidth, channels = im.shape
            out = cv2.VideoWriter(args.output, fourcc, fps, (int(fwidth), int(fheight)))
    except:
        print 'Cannot load ' + imgfile
    out.write(im)

out.release()

sys.exit()


