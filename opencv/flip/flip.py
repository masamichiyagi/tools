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
    parser.add_argument('-d', '--direction',  dest='direction',  help='-1: Half turn, 0: flip vertical, 1: flip horizontal', default='1', required=False)
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
def filters(filename, direction):
    im = cv2.imread(filename, 1)
    return cv2.flip(im, direction)

###################################
## Main roop
###################################
if __name__ == "__main__":
    args = arg_parser()
    direction = int(args.direction)
    files = glob.glob(os.path.join(args.indir, '*.' + args.expansion))
    files.sort()

    for filename in files:
        result = filters(filename, direction)
        outpath = os.path.join(args.outdir, os.path.basename(filename))
        cv2.imwrite(outpath, result)

