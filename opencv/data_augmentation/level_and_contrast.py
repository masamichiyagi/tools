#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import os, sys, glob, argparse
import numpy as np
from math import exp

###################################
## Argument Parser
###################################
def arg_parser():
    parser = argparse.ArgumentParser(description='Filter')
    parser.add_argument('-i', '--indir',  dest='indir',  help='input file directory', required=True)
    parser.add_argument('-o', '--outdir',  dest='outdir',  help='output file directory', required=True)
    parser.add_argument('-e', '--expansion',  dest='expansion',  help='expansion', default='jpg', required=False)
    args = parser.parse_args()

    if (not os.path.exists(args.indir)):
        print ("input directory does not exists : " + args.indir)
        sys.exit(1)
    if (not os.path.exists(args.outdir)):
        print ("output directory does not exists : " + args.outdir)
        sys.exit(1)
    return args

###################################
## Main roop
###################################
if __name__ == "__main__":
    args = arg_parser()
    files = glob.glob(os.path.join(args.indir, '*.' + args.expansion))
    files.sort()

    lut = np.zeros((256, 1), dtype = 'uint8')
    #for i in range(256):
    #    lut[i][0] = 255 * pow(float(i) / 255, 1.0 / gamma)
    to256 = np.array(range(256), dtype = 'float')

    gamma = 0
    gamma_c = 0 
    j = 0
    outdir = ""
    outpath = ""
    for gamma in np.arange(0.4, 4.0, 0.2):
        lut = np.uint8((255 * ((to256 / 255) ** (1.0 / gamma))).reshape(-1,1))
        # equivalent to under line
        #lut = np.uint8((255 * ((to256 / 255) ** (1.0 / gamma))).reshape(256,1))
        
        for filename in files:
            result = cv2.imread(filename, 1)
            result = cv2.LUT(result, lut) # level change

            ###################
            ## save file path
            ###################
            outdir = os.path.join(args.outdir, "{0:03d}".format(int(gamma*10)))

            for gamma_c in np.arange(0.4, 10, 0.2):
                for j in range(256):
                    lut[j][0] = 255 / (1+exp(-gamma_c*(j-128)/255))

                dst = cv2.LUT(result, lut) # contrast change

                ###################
                ## save file path
                ###################
                outdir_2 = outdir + "{0:03d}".format(int(gamma_c*10))
                if not (os.path.isdir(outdir_2)):
                    os.mkdir(outdir_2)
                outpath = os.path.join(outdir_2, os.path.basename(filename))
                ###################
                ## save file
                ###################
                cv2.imwrite(outpath, dst)


