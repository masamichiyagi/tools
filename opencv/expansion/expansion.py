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
    parser.add_argument('-w', '--width',  dest='width',  help='width', default='1280', required=False)
    parser.add_argument('-he', '--height',  dest='height',  help='height', default='720', required=False)
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
def filters(filename, width, height):
    im = cv2.imread(filename, 1)

    tmp = np.zeros_like(im.shape, dtype=np.uint8)
    tmp = im
    for i in xrange(int(width/im.shape[1])):
        tmp = cv2.hconcat([tmp, im])
    tmp2 = np.zeros_like(tmp.shape, dtype=np.uint8)
    tmp2 = tmp 
    for j in xrange(int(height/im.shape[0])):
        tmp2 = cv2.vconcat([tmp2, tmp])
    im = tmp2

    result = np.zeros((height, width, 3), dtype=np.uint8)
    result = im[0:height, 0:width, :]
    #for h in xrange(height):
    #    for w in xrange(width):
    #        result[h,w] = im[h,w]
    return result

###################################
## Main roop
###################################
if __name__ == "__main__":
    args = arg_parser()
    width = int(args.width)
    height = int(args.height)
    files = glob.glob(os.path.join(args.indir, '*.' + args.expansion))
    files.sort()

    for filename in files:
        result = filters(filename, width, height)
        outpath = os.path.join(args.outdir, os.path.basename(filename))
        cv2.imwrite(outpath, result)

