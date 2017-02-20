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
def filters(filename, k):
    im = cv2.imread(filename, 1)
    # シャープ化するためのオペレータ
    shape_operator = np.array([[0,        -k, 0],
                              [-k, 1 + 4 * k, -k],
                              [ 0,        -k, 0]])
    im = cv2.filter2D(im, -1, shape_operator)
    return cv2.convertScaleAbs(im)


###################################
## Main roop
###################################
if __name__ == "__main__":
    args = arg_parser()
    files = glob.glob(os.path.join(args.indir, '*.' + args.expansion))
    files.sort()

    k = 0
    filename = ""
    result = 0
    name = ""
    ext = ""
    outpath = ""
    for k in np.arange(1, 10, 1):
        for filename in files:
            result = filters(filename, k)
            ####################
            ## save one directory
            ####################
            name, ext = os.path.splitext(os.path.basename(filename))
            outpath = os.path.join(args.outdir, name + "_b{0:03d}".format(k) + ext)

            cv2.imwrite(outpath, result)


