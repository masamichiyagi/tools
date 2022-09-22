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
    ymax, xmax = im.shape[:2]
    xmid = int(xmax/2)
    left = im[0:ymax, 0:xmid]
    right = im[0:ymax, xmid:xmax]
    return [left,right]

###################################
## Main roop
###################################
if __name__ == "__main__":
    args = arg_parser()
    files = glob.glob(os.path.join(args.indir, '*.' + args.expansion))
    files.sort()

    for filename in files:
        results = filters(filename)
        bwe = os.path.splitext(os.path.basename(filename))[0] # basename without expansion
        l_outpath = os.path.join(args.outdir, os.path.basename(bwe + '_1l.' + args.expansion))
        r_outpath = os.path.join(args.outdir, os.path.basename(bwe + '_0r.' + args.expansion))
        cv2.imwrite(l_outpath, results[0])
        cv2.imwrite(r_outpath, results[1])

