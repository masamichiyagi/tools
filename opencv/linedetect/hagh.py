# -*- coding: utf-8 -*-
import os, sys, glob, cv2
import argparse
import numpy as np
from pylsd.lsd import lsd

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
    parser.add_argument('-t', '--threshold',  dest='threshold',  help='threshold', default='4', required=False)
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
def filtering(layer1filename, th=0):
    im = cv2.imread(layer1filename)
    im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
    height, width = im.shape[:2]
    channels = 1
    if th < 0:
        th = np.min([height, width]) // 10
    print("height: {}, width: {}, channel: {}".format(height, width, channels))
    print("dtype: {}".format(im.dtype))
    print("threshold: {}".format(th))


    im = cv2.GaussianBlur(im, (5,5),5)
    im = cv2.Canny(im,50,150,apertureSize = 3)
    lines = cv2.HoughLinesP(im, rho=1, theta=np.pi/360, threshold=50, minLineLength=50, maxLineGap=10)

    result = np.zeros((height, width, channels), dtype=np.uint8)

    for line in lines:
        x1, y1, x2, y2 = line[0]
        if np.abs(x2-x1) + np.abs(y2-y1) > th:
            #result = cv2.line(result, (x1,y1), (x2,y2), (0,0,255), channels)
            result = cv2.line(result, (x1,y1), (x2,y2), 255, channels)
    return result


###################################
## Main roop
###################################
def main():
    args = arg_parser()
    threshold = int(args.threshold)

    # Get file lists
    files = glob.glob(os.path.join(args.indir, '*.' + args.expansion))
    files.sort()

    for fname in files:
        # OpenCV filtering function
        result = filtering(fname, th=threshold)

        # To save files, get output path
        outpath = os.path.join(args.outdir, os.path.basename(fname))

        # Save files.
        # The case of Pillow
        #result.save(outpath, 'JPEG')
        # The case of OpenCV
        cv2.imwrite(outpath, result)

if __name__ == '__main__':
    main()
