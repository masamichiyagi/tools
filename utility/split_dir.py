#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, glob, argparse
import shutil
import numpy as np

###################################
## Argument Parser
###################################
def arg_parser():
    parser = argparse.ArgumentParser(description='Filter')
    parser.add_argument('-i', '--indir',  dest='indir',  help='input file directory', required=True)
    parser.add_argument('-o', '--outdir',  dest='outdir',  help='output file directory', required=True)
    parser.add_argument('-s', '--index',  dest='index',  help='start index', default='0', required=False)
    args = parser.parse_args()

    if (not os.path.exists(args.indir)):
        print ("input file does not exists : " + args.indir)
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
    index = int(args.index)
    print("index is : ", index)
    files = glob.glob(os.path.join(args.indir, '*.*'))
    files.sort()

    for filename in files:
        if 0 == index%2:
            basename_ = os.path.basename(filename)
            outpath = os.path.join(args.outdir, basename_)
            shutil.copyfile(filename, outpath);
        index += 1

