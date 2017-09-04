#!/usr/bin/env python

import numpy as np
import os, sys, glob, colorsys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2
import argparse
from PIL import Image
from PIL import ImageEnhance



LABEL_COLOR_NUM = 10

FONTFACES = (
    cv2.FONT_HERSHEY_SIMPLEX,
    cv2.FONT_HERSHEY_PLAIN,
    cv2.FONT_HERSHEY_DUPLEX,
    cv2.FONT_HERSHEY_COMPLEX,
    cv2.FONT_HERSHEY_TRIPLEX,
    cv2.FONT_HERSHEY_COMPLEX_SMALL,
    cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
    cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
    cv2.FONT_ITALIC );


def labelToColor(label):
    hseed = hash(label)
    h = hseed % LABEL_COLOR_NUM / float(LABEL_COLOR_NUM)
    rgba = [int(x * 255) for x in colorsys.hsv_to_rgb(*(h, 0.8, 0.5))]
    return rgba


def renderimage(layer1filename, layer2filename):
    try:
        layer1img = Image.open( layer1filename )
        layer2img = Image.open( layer2filename )
        layer1img = layer1img.convert('RGBA')
        layer2img = layer2img.convert('RGBA')

        canvas_size = (layer1img.size[0] * 2, layer1img.size[1])
        #layer2img = layer2img.resize(canvas_size)
        #layer1img = layer1img.resize(canvas_size)

        canvas = Image.new('RGBA', canvas_size, (255, 255, 255, 0))
        canvas.paste(layer2img, (0, 0), layer2img)
        canvas.paste(layer1img, (layer1img.size[0], 0), layer1img)
    except:
        print('Cant load ', layer1filename, layer2filename)
        sys.exit(1)
    return canvas




parser = argparse.ArgumentParser(description='Faster R-CNN')
parser.add_argument('--rightimgdir',  dest='rightimgdir',  help='img directory', required=True)
parser.add_argument('--leftimgdir',  dest='leftimgdir',  help='origin img directory', required=True)
parser.add_argument('--output',  dest='output',  help='output filename', required=True)
parser.add_argument('--fps',  dest='fps',  help='frame rate', required=False)
args = parser.parse_args()

fontface = FONTFACES[0] | FONTFACES[8]
fontsize = 0.6
fonttick = 1

# open cv 3.1 has no "cv2.cv" -> please define CV_AA.
fourcc = cv2.cv.CV_FOURCC(*'XVID')
#fourcc = cv2.VideoWriter_fourcc(*'XVID')

fwidth = 1920
fheight = 1080
fps = 30
if not (args.fps):
    fps = 30
else:
    fps = int(args.fps)

out = None # cv2.VideoWriter(args.output, fourcc, 30, (int(fwidth), int(fheight)))
    
imgFiles = glob.glob(os.path.join(args.rightimgdir, '*.jpg'))
#imgFiles = glob.glob(os.path.join(args.rightimgdir, '*.png'))
imgFiles.sort()
originImgFiles = glob.glob(os.path.join(args.leftimgdir, '*.jpg'))
originImgFiles.sort()


#for imgfile in imgFiles:
for i in range(len(imgFiles)):
    try:
        result = renderimage(imgFiles[i], originImgFiles[i])
        result.save('./tmp.jpg', 'JPEG')
        im = cv2.imread('./tmp.jpg')
        if not (out):
            fheight, fwidth, channels = im.shape
            out = cv2.VideoWriter(args.output, fourcc, fps, (int(fwidth), int(fheight)))
    except:
        print('Cannot load ' + imgFiles[i])
    out.write(im)

out.release()

sys.exit()


