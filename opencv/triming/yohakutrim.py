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
    parser.add_argument('-i', '--indir', dest='indir',  help='input file directory', required=True)
    parser.add_argument('-o', '--outdir', dest='outdir',  help='output file directory', required=True)
    parser.add_argument('-e', '--expansion', dest='expansion',  help='expansion', default='jpg', required=False)
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
    gray = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)[1]
    contours = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    for i in range(1, len(contours)):
        ret = cv2.boundingRect(contours[i])
        x1.append(ret[0])
        y1.append(ret[1])
        x2.append(ret[0] + ret[2])
        y2.append(ret[1] + ret[3])
    xmin = min(x1)
    ymin = min(y1)
    xmax = max(x2)
    ymax = max(y2)
    result = im[ymin:ymax, xmin:xmax]
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

