# -*- coding: utf-8 -*-
import os, sys, glob, cv2, colorsys, random
import argparse
import numpy as np
from PIL import Image
from PIL import ImageEnhance
from matplotlib import pylab as plt


#################################################
## Gloval Variables Definition
#################################################
#face_cascade = cv2.CascadeClassifier('haarcascade_frontalcatface_extended.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


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

    gray = cv2.cvtColor(im,cv2.COLOR_RGB2GRAY)
    #faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))
    faces = face_cascade.detectMultiScale(gray,1.3,5)

    if 0 < len(faces):
        for (x,y,w,h) in faces:
            cut_img = im[y:y+h,x:x+w]
            cut_face = cut_img.shape[:2][::-1]
            cut_img = cv2.resize(cut_img, (cut_face[0]/10, cut_face[0]/10))
            cut_img = cv2.resize(cut_img, cut_face, interpolation = cv2.cv.CV_INTER_NN)
            im[y:y+h,x:x+w] = cut_img

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

