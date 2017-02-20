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
def filters(filename, sigma, mean):
    im = cv2.imread(filename, 1)
    gauss = np.random.normal(mean,sigma,im.shape)
    return im + gauss.reshape(im.shape)

###################################
## Main roop
###################################
if __name__ == "__main__":
    args = arg_parser()
    files = glob.glob(os.path.join(args.indir, '*.' + args.expansion))
    files.sort()

    mean = 0
    sigma = 0
    filename = ""
    result = 0
    name = ""
    ext = ""
    outpath = ""
    for sigma in np.arange(5, 15, 0.2):
        for filename in files:
            result = filters(filename, sigma, mean)
            ####################
            ## save one directory
            ####################
            name, ext = os.path.splitext(os.path.basename(filename))
            outpath = os.path.join(args.outdir, name + "_{0:03d}".format(int(sigma*10)) + ext)

            ####################
            ## save some directories
            ####################
            #outdir = os.path.join(args.outdir, "{0:03d}".format(int(sigma*10)))
            #if not (outdir)):
            #    os.mkdir(outdir)
            #outpath = os.path.join(outdir, os.path.basename(filename))
            cv2.imwrite(outpath, result)


