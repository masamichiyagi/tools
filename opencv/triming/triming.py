# -*- coding: utf-8 -*-
# Example of executing this file:
# python filter_flip_h.py -i /data/common/datasets/image/coco2014/images/val2014/ -o output/ -e jpg

#################################################
## Import Definition
#################################################
import os, sys, glob, cv2
import argparse
import numpy as np

# If you use PIL, you can remove comment.
#from PIL import Image
#from PIL import ImageEnhance

# If you use matplotlib, you can remove comment.
#from matplotlib import pylab as plt

#################################################
## Gloval Variables Definition
#################################################
xmin = 54
ymin = 560
#width = 100
#width = 1280 - x
#height = 100
#height = 1080 - y
xmax = 1365
ymax = 847

#################################################
## Argument Parser Definition
#################################################
parser = argparse.ArgumentParser(description='OpenCV Filters: flip')
parser.add_argument('-i', '--imgdir',  dest='imgdir',  help='img directory', required=True)
parser.add_argument('-o', '--outputdir',  dest='outdir',  help='output img directory', required=True)
parser.add_argument('-e', '--extension',  dest='extension',  help='filename extension', default='jpg', required=False)
args = parser.parse_args()

if (not os.path.exists(args.imgdir)):
    print ("image directory does not exists : " + args.imgdir)
    sys.exit(1)
if (not os.path.exists(args.outdir)):
    print ("output directory does not exists : " + args.outdir)
    sys.exit(1)


#################################################
## OpenCV filtering function
#################################################
def filtering(layer1filename):
    im = cv2.imread(layer1filename, 1)
    result = im[ymin:ymax, xmin:xmax]
    return result



#################################################
## Main roop
#################################################

# Get image file list
imgFiles = sorted(glob.glob(os.path.join(args.imgdir, '*.' + args.extension)))
# If you do not need 'file sorting', you can remove 'sorted' function.
#imgFiles = glob.glob(os.path.join(args.imgdir, '*.' + args.extension))



for fname in imgFiles:
    # OpenCV filtering function
    result = filtering(fname)

    # To save files, get output path
    outpath = os.path.join(args.outdir, os.path.basename( fname ) )

    # Save files.
    # The case of Pillow
    #result.save(outpath, 'JPEG')
    # The case of OpenCV
    cv2.imwrite(outpath, result)


