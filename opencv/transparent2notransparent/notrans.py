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
    parser.add_argument('-e', '--expansion',  dest='expansion',  help='expansion', default='png', required=False)
    parser.add_argument('-t', '--trans',  dest='trans',  help='transparency', required=False, default="1")
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
def filters(filename, trans):
    im = cv2.imread(filename, -1)
    width, height, c = im.shape[:3]
    
    if ( c < 4):
        print("Image is not transparent type.")
        print("Channel is " + str(c))
        return im

    msk = np.zeros((width, height, 4), dtype=im.dtype)
    msk[:,:,0] = msk[:,:,1] = msk[:,:,2] = msk[:,:,3] = im[:, :, 3]
    im[msk<trans]=255
    return im[:,:,:3]
 

###################################
## Main roop
###################################
if __name__ == "__main__":
    args = arg_parser()
    trans = int(args.trans)
    files = glob.glob(os.path.join(args.indir, '*.' + args.expansion))
    files.sort()

    for filename in files:
        result = filters(filename, trans)
        outpath = os.path.join(args.outdir, os.path.basename(filename))
        cv2.imwrite(outpath, result)

