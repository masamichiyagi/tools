# -*- coding: UTF-8 -*-
# modify filename
# example 001.xxx 002.xxx 003.xxx
# --help
# python renban.py dirname
# example 
# python renban.py ./test

import os
import sys
import argparse
import re

#################################################
## Argument Parser Definition
#################################################
parser = argparse.ArgumentParser(description='OpenCV Filters: flip')
parser.add_argument('-i', '--indir',  dest='inputdir',  help='input directory', required=True)
args = parser.parse_args()

if (not os.path.exists(args.inputdir)):
    print ("input directory does not exists : " + args.inputdir)
    sys.exit(1)

os.chdir(args.inputdir)

listFiles = sorted(os.listdir("."))
for filename in listFiles:
    fn, ext = os.path.splitext(filename)
    # fn = re.sub(r'-.{11}$', '', fn)
    fn = re.sub(r'(-+)[^-]+$', '', fn)
    print(fn + ext)
    os.rename(filename, fn + ext)

