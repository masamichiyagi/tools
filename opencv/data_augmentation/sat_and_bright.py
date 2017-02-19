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
def saturation_filters(filename, value):
    im = cv2.imread(filename, 1)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    #hsv[:,:,0] # Hue 0-180
    #hsv[:,:,1] # Saturation 0-255
    #hsv[:,:,2] # Value 0-255 
    weight = np.zeros(im.shape, dtype=np.uint8)
    weight[:,:,1] = abs(value)
    if (0 < value):
        im = cv2.add(im, weight)
    else:
        im = cv2.subtract(im, weight)
    im = cv2.cvtColor(im, cv2.COLOR_HSV2BGR)
    return im

def brightness_filters(im, value):
    dst = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    #hsv[:,:,0] # Hue 0-180
    #hsv[:,:,1] # Saturation 0-255
    #hsv[:,:,2] # Value 0-255 
    weight = np.zeros(im.shape, dtype=np.uint8)
    weight[:,:,2] = abs(value)
    if (0 < value):
        dst = cv2.add(dst, weight)
    else:
        dst = cv2.subtract(dst, weight)
    dst = cv2.cvtColor(dst, cv2.COLOR_HSV2BGR)
    return dst 



###################################
## Main roop
###################################
if __name__ == "__main__":
    args = arg_parser()
    files = glob.glob(os.path.join(args.indir, '*.' + args.expansion))
    files.sort()

    i = 0
    j = 0
    for i in np.arange(-10, 10, 1):
        for filename in files:
            result = saturation_filters(filename, i*10) # saturation change

            ###################
            ## save file path
            ###################
            outdir = os.path.join(args.outdir, "{0:03d}".format(10+i))

            for j in np.arange(-10, 10, 1):
                dst = brightness_filters(result, j*10) # brightness change

                ###################
                ## save file path
                ###################
                outdir_2 = outdir + "{0:03d}".format(10+j)
                if not (os.path.isdir(outdir_2)):
                    os.mkdir(outdir_2)
                outpath = os.path.join(outdir_2, os.path.basename(filename))
                ###################
                ## save file
                ###################
                cv2.imwrite(outpath, dst)


