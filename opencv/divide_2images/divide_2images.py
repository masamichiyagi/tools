# -*- coding: utf-8 -*-
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


###################################
## Argument Parser
###################################
def arg_parser():
    parser = argparse.ArgumentParser(description='OpenCV Filters')
    parser.add_argument('-i', '--indir',  dest='indir',  help='input file directory', required=True)
    parser.add_argument('-o', '--outdir',  dest='outdir',  help='output file directory', required=True)
    parser.add_argument('-e', '--expansion',  dest='expansion',  help='expansion', default='jpg', required=False)
    args = parser.parse_args()

    if (not os.path.exists(args.indir)):
        print ("input directory does not exists : " + args.indir)
        sys.exit(1)
    if (not os.path.exists(args.outdir)):
        print ("annotation directory does not exists : " + args.outdir)
        sys.exit(1)
    return args


#################################################
## OpenCV filtering function
#################################################
def filtering(layer1filename):
    im = cv2.imread(layer1filename)
    height, width = im.shape[:2]
    canvas1 = np.zeros((int(height/2), width, 3), dtype=np.uint8)
    canvas2 = np.zeros((height - (int(height/2)), width, 3), dtype=np.uint8)
    canvas1 = im[:(int(height/2)),:,:]
    canvas2 = im[(int(height/2))+1:,:,:]

    return canvas1, canvas2


###################################
## Main roop
###################################
if __name__ == "__main__":
    args = arg_parser()

    # Get image file lists
    files = glob.glob(os.path.join(args.indir, '*.' + args.expansion))
    files.sort()

    i=0

    for fname in files:
        # OpenCV filtering function
        canvas1, canvas2= filtering(fname)

        # To save files, get output path
        outpath = os.path.join(args.outdir, "{0:08d}".format(i)+os.path.splitext(fname)[1])
        i += 1

        # Save files.
        # The case of Pillow
        #result.save(outpath, 'JPEG')
        # The case of OpenCV
        cv2.imwrite(outpath, canvas1)


        outpath = os.path.join(args.outdir, "{0:08d}".format(i)+os.path.splitext(fname)[1])
        i += 1
        cv2.imwrite(outpath, canvas2)

