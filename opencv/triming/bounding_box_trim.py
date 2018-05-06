#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import os, sys, glob, argparse
import numpy as np

###################################
## Argument Parser
###################################
def arg_parser():
    parser = argparse.ArgumentParser(description='Filter')
    parser.add_argument('-i', '--indir',  dest='indir',  help='input file directory', required=True)
    parser.add_argument('-o', '--outdir',  dest='outdir',  help='output file directory', required=True)
    parser.add_argument('-e', '--expansion',  dest='expansion',  help='expansion', default='jpg', required=False)
    args = parser.parse_args()

    if (not os.path.exists(args.indir)):
        print ("input directory does not exists : " + args.indir)
        sys.exit(1)
    if (not os.path.exists(args.outdir)):
        print ("output directory does not exists : " + args.outdir)
        sys.exit(1)
    return args


###################################
## Filter function
###################################
def filters(filename):
    im = cv2.imread(filename, 1)
    
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    #th1 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    th1 = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    #th1 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

    name, ext = os.path.splitext(os.path.basename(filename))
    outpath = os.path.join(args.outdir, name + ext)
    cv2.imwrite(outpath, th1)
    
    contours = cv2.findContours(th1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[1]
    for i in range(0, len(contours)):
        #if (i % 2 == 0):
        cnt = contours[i]
        x,y,w,h = cv2.boundingRect(cnt)
        # if you check bounding box
        #cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)

        dst = im.copy()
        dst = dst[y:(y+h), x:(x+w)]

        #name, ext = os.path.splitext(os.path.basename(filename))
        outpath = os.path.join(args.outdir, name + "{0:03d}".format(i) + ext)
        cv2.imwrite(outpath, dst)

    return im

###################################
## Main roop
###################################
if __name__ == "__main__":
    args = arg_parser()
    files = glob.glob(os.path.join(args.indir, '*.' + args.expansion))
    files.sort()

    for filename in files:
        result = filters(filename)
        #outpath = os.path.join(args.outdir, os.path.basename(filename))
        #cv2.imwrite(outpath, result)

