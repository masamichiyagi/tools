# -*- coding: utf-8 -*-
import os
import sys
import glob
import argparse
from PIL import Image

parser = argparse.ArgumentParser(description='Faster R-CNN')
parser.add_argument('-b', '--bottomimgdir',  dest='bottomimgdir',  help='origin img directory', required=True)
parser.add_argument('-t', '--topimg',  dest='topimg',  help='top img', required=True)
# example: outputimg/ 
parser.add_argument('-o', '--outputdir',  dest='output',  help='output img directory', required=True)
parser.add_argument('-e', '--extension',  dest='extension',  help='filename extension', default='jpg', required=False)
args = parser.parse_args()

def filtering(layer1filename, layer2filename):
    try:
        layer1img = Image.open( layer1filename )
        layer2img = Image.open( layer2filename )
        layer1img = layer1img.convert('RGBA')
        layer2img = layer2img.convert('RGBA')
        layer1img.paste(layer2img, (0, 0), layer2img)
    except:
        print('Cant load ', layer1filename, layer2filename)
        sys.exit(1)
    return layer1img 

if (not os.path.exists(args.topimg)):
    print ("image file does not exists : " + args.topimg)
    sys.exit(1)
if (not os.path.exists(args.output)):
    print ("output directory does not exists : " + args.output)
    sys.exit(1)

# input image file list
topImgFile = args.topimg
bottomImgFiles = sorted(glob.glob(os.path.join(args.bottomimgdir, '*.*')))


for i in range(len(bottomImgFiles)):
    # filtering
    result = filtering(bottomImgFiles[i], topImgFile)
    # save
    outpath = os.path.join(args.output, os.path.basename( bottomImgFiles[i] ))
    # Save. The case of Pillow
    #result.save(outpath, 'JPEG')
    #cv2.imwrite(outpath, result)
    if 'jpg' == args.extension:
        result.save(outpath, 'JPEG')
    if 'png' == args.extension:
        result.save(outpath, 'PNG')


