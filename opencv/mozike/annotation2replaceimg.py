#!/usr/bin/env python
# coding:utf-8
import xml.etree.ElementTree as ET
import os, sys, glob, cv2
import argparse
import numpy as np

replace_img_path1 = "mozike_img/00000001.png"
replace_img_path2 = "mozike_img/00000002.png"

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


def filtering(imgFilePath, xmlFilePath, repImg1, repImg2):
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

        repImg = repImg1.copy()
        repImg = cv2.resize(repImg1,(int(abs(xmax-xmin)),int(abs(ymax-ymin))))
        print((int(abs(xmax-xmin)),int(abs(ymax-ymin))), ymin, ymax, xmin, xmax)
        mask = repImg[:,:,3]
        mask = cv2.cvtColor(mask, cv2.cv.CV_GRAY2BGR)
        mask = mask / 255.0
        repImg = repImg[:,:,:3]
        srcImg[ymin:ymax, xmin:xmax] = np.array(srcImg[ymin:ymax, xmin:xmax] * (1 - mask), dtype=np.uint8)
        srcImg[ymin:ymax, xmin:xmax] = np.array(srcImg[ymin:ymax, xmin:xmax] + repImg * mask, dtype=np.uint8)

    return srcImg

###################################
## Main roop
###################################
if __name__ == "__main__":
    args = arg_parser()

    # Get image file lists
    files = glob.glob(os.path.join(args.indir, '*.' + args.expansion))
    files.sort()

    repImg1 = cv2.imread(replace_img_path1, -1)
    repImg2 = cv2.imread(replace_img_path2, -1)

    for imgfname in files:
        xmlfname, ext = os.path.splitext(os.path.basename(imgfname))
        xmlfname = os.path.join(args.anndir, xmlfname + '.xml') 

        # OpenCV filtering function
        result = filtering(imgfname, xmlfname, repImg1, repImg2)

        # To save files, get output path
        outpath = os.path.join(args.outdir, os.path.basename(imgfname))

        # Save files.
        # The case of Pillow
        #result.save(outpath, 'JPEG')
        # The case of OpenCV
        cv2.imwrite(outpath, result)


