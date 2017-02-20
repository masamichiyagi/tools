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


###################################
## Main roop
###################################
if __name__ == "__main__":
    args = arg_parser()
    files = glob.glob(os.path.join(args.indir, '*.' + args.expansion))
    files.sort()

    avg = 0
    filename = ""
    result = 0
    name = ""
    ext = ""
    outpath = ""
    for avg in np.arange(3, 25, 2):
        for filename in files:
            im = cv2.imread(filename, 1)
            result_b = cv2.blur(im, (avg,avg))
            result_g = cv2.GaussianBlur(im,(avg,avg),1)
            result_m = cv2.medianBlur(im,avg)
            ####################
            ## save one directory
            ####################
            name, ext = os.path.splitext(os.path.basename(filename))
            outpath_b = os.path.join(args.outdir, name + "_b{0:03d}".format(avg) + ext)
            outpath_g = os.path.join(args.outdir, name + "_g{0:03d}".format(avg) + ext)
            outpath_m = os.path.join(args.outdir, name + "_m{0:03d}".format(avg) + ext)

            cv2.imwrite(outpath_b, result_b)
            cv2.imwrite(outpath_g, result_g)
            cv2.imwrite(outpath_m, result_m)


