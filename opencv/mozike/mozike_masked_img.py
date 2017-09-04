# -*- coding: utf-8 -*-
# example python randampic.py --imgdir /data/customers/ipc/inputs/20161020/2016/THLTestGPS16062016/IPA-SV003-PC/Pic/20160616/20160616142327/0/ --outputdir output/ --overlayimg circle/001.PNG
import os, sys, glob, cv2, colorsys, random
import argparse
import numpy as np
from PIL import Image
from PIL import ImageEnhance
from matplotlib import pylab as plt

parser = argparse.ArgumentParser(description='OpenCV Filter')
parser.add_argument('--imgdir',  dest='imgdir',  help='img directory', required=True)
# example: outputimg/ 
parser.add_argument('--outputdir',  dest='output',  help='output img directory', required=True)
parser.add_argument('--maskimg',  dest='mask',  help='mask image', required=True)
parser.add_argument('--extension',  dest='extension',  help='filename extension', default='jpg', required=False)
args = parser.parse_args()

def filtering(layer1filename):
    im = cv2.imread(layer1filename)
    mask = cv2.imread(args.mask, -1)
    alpha = mask[:,:,3]
    alpha = cv2.cvtColor(alpha, cv2.cv.CV_GRAY2BGR)  # 3色分に増やす。
    mask = mask[:,:,:3]

    im_masked = im.copy()
    im_masked[mask>0] = 255
    origsize = im_masked.shape[:2][::-1]
    im_masked = cv2.resize(im_masked, (origsize[0]/20, origsize[1]/20))
    im_masked = cv2.resize(im_masked, origsize, interpolation=cv2.cv.CV_INTER_NN)
    im_masked[mask>0] = 255

    im[mask==0] = 0
    im += im_masked * alpha

    return im

if (not os.path.exists(args.imgdir)):
    print ("image directory does not exists : " + args.imgdir)
    sys.exit(1)
if (not os.path.exists(args.output)):
    print ("output directory does not exists : " + args.output)
    sys.exit(1)
if (not os.path.exists(args.mask)):
    print ("output directory does not exists : " + args.output)
    sys.exit(1)


# input image file list
imgFiles = sorted(glob.glob(os.path.join(args.imgdir, '*.' + args.extension)))

for fname in imgFiles:
    # filtering
    result = filtering(fname)
    # save
    outpath = os.path.join(args.output, os.path.basename( fname ) )
    # Save. The case of Pillow
    #result.save(outpath, 'JPEG')
    cv2.imwrite(outpath, result)


