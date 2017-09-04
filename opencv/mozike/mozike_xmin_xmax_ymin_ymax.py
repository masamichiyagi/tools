# -*- coding: utf-8 -*-
import os, sys, glob, cv2, colorsys, random
import argparse
import numpy as np
from PIL import Image
from PIL import ImageEnhance
from matplotlib import pylab as plt


xmin = 115
ymin = 32

xmax = 252
ymax = 50

#################################################
## Argument Parser Definition
#################################################
parser = argparse.ArgumentParser(description='OpenCV Filters')
parser.add_argument('-i', '--imgdir',  dest='imgdir',  help='img directory', required=True)
parser.add_argument('-o', '--outputdir',  dest='outdir',  help='output img directory', required=True)
parser.add_argument('-e', '--extension',  dest='extension',  help='filename extension', default='jpg', required=False)
args = parser.parse_args()

if (not os.path.exists(args.imgdir)):
    print ("image directory does not exists : " + args.imgdir)
    sys.exit(1)
if (not os.path.exists(args.outdir)):
    print ("output directory does not exists : " + args.output)
    sys.exit(1)



#################################################
## filtering function
#################################################
def filtering(layer1filename):
    im = cv2.imread(layer1filename)
    cut_img = im[ymin:ymax,xmin:xmax]
    cut_tmp = cut_img.shape[:2][::-1]
    cut_img = cv2.resize(cut_img, (cut_tmp[0]/20, cut_tmp[0]/20))
    cut_img = cv2.resize(cut_img, cut_tmp, interpolation = cv2.cv.CV_INTER_NN)
    im[ymin:ymax,xmin:xmax] = cut_img

    return im

#################################################
## Main roop
#################################################

# Get file lists
imgFiles = sorted(glob.glob(os.path.join(args.imgdir, '*.' + args.extension)))

for fname in imgFiles:
    # filtering function
    result = filtering(fname)

    # Save files
    outpath = os.path.join(args.outdir, os.path.basename( fname ) )
    cv2.imwrite(outpath, result)

