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
    parser.add_argument('-t', '--tone',  dest='tone',  help='tone file', default='./tone/stripe_001.png', required=False)
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
    if '3.1.0' == cv2.__version__:
        im = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        screen = cv2.imread(args.tone, cv2.IMREAD_GRAYSCALE)
    else:
        im = cv2.imread(filename,cv2.CV_LOAD_IMAGE_GRAYSCALE)
        screen = cv2.imread(args.tone, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    width, height = im.shape
    width_screen, height_screen = screen.shape

    tmp = np.zeros_like(screen.shape, dtype=np.uint8)
    tmp = screen
    for i in xrange(int(width/width_screen)):
        tmp = cv2.hconcat([tmp, screen])
    tmp2 = np.zeros_like(tmp.shape, dtype=np.uint8)
    tmp2 = tmp 
    for j in xrange(int(height/height_screen)):
        tmp2 = cv2.vconcat([tmp2, tmp])
    screen = tmp2

    edge= cv2.Canny(im,80,120)
    nega = cv2.bitwise_not(edge)

    tmp = screen[0:width, 0:height]
    tmp[im<80] = 0
    tmp[im>160]=255

    alpha = 0.5
    result = cv2.addWeighted(nega,alpha,tmp,1-alpha,0.0)
    (thresh,result)=cv2.threshold(result,200,255,cv2.THRESH_BINARY)
    return result

###################################
## Main roop
###################################
if __name__ == "__main__":
    args = arg_parser()
    files = glob.glob(os.path.join(args.indir, '*.' + args.expansion))
    files.sort()

    for filename in files:
        result = filters(filename)
        outpath = os.path.join(args.outdir, os.path.basename(filename))
        cv2.imwrite(outpath, result)

