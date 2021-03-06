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
    parser.add_argument('--xmin', dest='xmin', help='xmin', default='406', required=False)
    parser.add_argument('--xmax', dest='xmax', help='xmax', default='882', required=False)
    parser.add_argument('--ymin', dest='ymin', help='ymin', default='119', required=False)
    parser.add_argument('--ymax', dest='ymax', help='ymax', default='504', required=False)
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
def filters(filename, xmin, xmax, ymin, ymax):
    im = cv2.imread(filename, 1)
    result = im[ymin:ymax, xmin:xmax]
    return result

###################################
## Main roop
###################################
if __name__ == "__main__":
    args = arg_parser()
    xmin = int(args.xmin)
    xmax = int(args.xmax)
    ymin = int(args.ymin)
    ymax = int(args.ymax)
    files = glob.glob(os.path.join(args.indir, '*.' + args.expansion))
    files.sort()

    for filename in files:
        result = filters(filename, xmin, xmax, ymin, ymax)
        outpath = os.path.join(args.outdir, os.path.basename(filename))
        cv2.imwrite(outpath, result)

