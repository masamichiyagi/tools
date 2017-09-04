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

#################################################
## Argument Parser Definition
#################################################
parser = argparse.ArgumentParser(description='OpenCV Filters: flip')
parser.add_argument('-i', '--indir',  dest='inputdir',  help='input directory', required=True)
parser.add_argument('-s', '--index',  dest='index',  help='start index', default='0', required=False)
parser.add_argument('-p', '--prefix',  dest='prefix',  help='prefix', default='', required=False)
args = parser.parse_args()

if (not os.path.exists(args.inputdir)):
    print ("input directory does not exists : " + args.inputdir)
    sys.exit(1)

os.chdir(args.inputdir)
i = int(args.index)
print("index is : ", i)

listFiles = sorted(os.listdir("."))
for filename in listFiles:
    os.rename(filename, args.prefix + "{0:08d}".format(i)+os.path.splitext(filename)[1])
    i += 1

