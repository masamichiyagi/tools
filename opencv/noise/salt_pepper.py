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
def salt_filters(filename, amount):
    im = cv2.imread(filename, 1)

    sp_img = im.copy()

    # salt mode
    num_salt = np.ceil(amount * im.size * s_vs_p)
    coords = [np.random.randint(0, i-1 , int(num_salt)) for i in im.shape]
    sp_img[coords[:-1]] = (255,255,255)

    return sp_img

def pepper_filters(filename, amount):
    im = cv2.imread(filename, 1)
    sp_img = im.copy()
    # pepper mode
    num_pepper = np.ceil(amount* im.size * (1. - s_vs_p))
    coords = [np.random.randint(0, i-1 , int(num_pepper)) for i in im.shape]
    sp_img[coords[:-1]] = (0,0,0)
    return sp_img


###################################
## Main roop
###################################
if __name__ == "__main__":
    args = arg_parser()
    files = glob.glob(os.path.join(args.indir, '*.' + args.expansion))
    files.sort()

    s_vs_p = 0.5
    amount = 0.004

    filename = ""
    result = 0
    name = ""
    ext = ""
    outpath = ""
    for amount in np.arange(0.004, 0.02, 0.001):
        for filename in files:
            result_s = salt_filters(filename, amount)
            result_p = pepper_filters(filename, amount)
            ####################
            ## save one directory
            ####################
            name, ext = os.path.splitext(os.path.basename(filename))
            outpath_s = os.path.join(args.outdir, name + "_s{0:03d}".format(int(amount*1000)) + ext)
            outpath_p = os.path.join(args.outdir, name + "_p{0:03d}".format(int(amount*1000)) + ext)

            ####################
            ## save some directories
            ####################
            #outdir = os.path.join(args.outdir, "{0:03d}".format(int(sigma*10)))
            #if not (outdir)):
            #    os.mkdir(outdir)
            #outpath = os.path.join(outdir, os.path.basename(filename))
            cv2.imwrite(outpath_s, result_s)
            cv2.imwrite(outpath_p, result_p)


