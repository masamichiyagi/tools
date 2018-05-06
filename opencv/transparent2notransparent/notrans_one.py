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
    parser.add_argument('-i', '--fname',  dest='fname',  help='file name', required=True)
    parser.add_argument('-o', '--outdir',  dest='outdir',  help='output file directory', required=True)
    parser.add_argument('-t', '--trans',  dest='trans',  help='transparency', required=False, default="1")
    args = parser.parse_args()

    if (not os.path.exists(args.fname)):
        print ("input directory does not exists : " + args.fname)
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

    result = filters(args.fname, trans)
    outpath = os.path.join(args.outdir, os.path.basename(args.fname))
    cv2.imwrite(outpath, result)

