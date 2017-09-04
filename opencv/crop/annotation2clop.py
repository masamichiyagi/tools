#!/usr/bin/env python
# coding:utf-8
import xml.etree.ElementTree as ET
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
    parser.add_argument('-x', '--anndir',  dest='anndir',  help='annotation file directory', required=True)
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


def filtering(imgFilePath, xmlFilePath, i):
    xmlRoot = ET.parse(xmlFilePath).getroot()
    
    srcImg = cv2.imread(imgFilePath)
    for obj in xmlRoot.findall('.//object'):
        category = obj.find('./name').text
        xmin = obj.find('./bndbox/xmin').text 
        ymin = obj.find('./bndbox/ymin').text
        xmax =   obj.find('./bndbox/xmax').text
        ymax = obj.find('./bndbox/ymax').text

        # 小数点座標対策：一旦floatに変換
        xmin = int(float(xmin))
        ymin = int(float(ymin))
        xmax = int(float(xmax))
        ymax = int(float(ymax))

        cropImg = srcImg[ymin:ymax, xmin:xmax]

        outpath = os.path.join(args.outdir, category + "-%08d" % i + ".jpg") 
        cv2.imwrite(outpath, cropImg )
        i += 1
    return i

###################################
## Main roop
###################################
if __name__ == "__main__":
    args = arg_parser()

    # Get image file lists
    files = glob.glob(os.path.join(args.indir, '*.' + args.expansion))
    files.sort()

    i = 0
    for imgfname in files:
        xmlfname, ext = os.path.splitext(os.path.basename(imgfname))
        xmlfname = os.path.join(args.anndir, xmlfname + '.xml') 

        # OpenCV filtering function
        i = filtering(imgfname, xmlfname, i)

