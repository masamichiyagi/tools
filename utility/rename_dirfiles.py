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
import glob

#################################################
## Argument Parser Definition
#################################################
def arg_parser():
    parser = argparse.ArgumentParser(description='OpenCV Filters: flip')
    parser.add_argument('-i', '--indir',  dest='indir',  help='input directory', required=True)
    parser.add_argument('-b', '--before',  dest='before',  help='before', required=True)
    parser.add_argument('-a', '--after',  dest='after',  help='after', required=True)
    args = parser.parse_args()

    if (not os.path.exists(args.indir)):
        print ("input directory does not exists : " + args.indir)
        sys.exit(1)
    return args

###################################
## Main roop
###################################
def main():
    args = arg_parser()
    before = args.before
    after = args.after

    # Get file lists
    files = glob.glob(os.path.join(args.indir, '*'))

    for fname in files:
        # To save files, get output path
        after_name = re.sub(before, after, os.path.basename(fname))
        outpath = os.path.join(args.indir, after_name)

        print(fname + " to " + outpath)
        os.rename(fname, outpath)


    #os.chdir(args.inputdir)

    #listFiles = sorted(os.listdir("."))
    #for filename in listFiles:
    #    fn, ext = os.path.splitext(filename)
        # fn = re.sub(r'-.{11}$', '', fn)
    #    fn = re.sub(r'(-+)[^-]+$', '', fn)
    #    print(fn + ext)
    #    os.rename(filename, fn + ext)


if __name__ == '__main__':
    main()
