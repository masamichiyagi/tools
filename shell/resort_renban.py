#!/usr/bin/env python
# coding: UTF-8
import os, sys, glob, argparse

###################################
## Argument Parser
###################################
def arg_parser():
    parser = argparse.ArgumentParser(description='Filter')
    parser.add_argument('-i', '--indir',  dest='indir',  help='input file directory', required=True)
    parser.add_argument('-s', '--index',  dest='index',  help='start index', default='0', required=False)
    parser.add_argument('-p', '--prefix',  dest='prefix',  help='prefix', default='', required=False)
    args = parser.parse_args()

    if (not os.path.exists(args.indir)):
        print ("input directory does not exists : " + args.indir)
        sys.exit(1)
    return args


###################################
## Main roop
###################################
if __name__ == "__main__":
    args = arg_parser()
    index = int(args.index)
    files = glob.glob(os.path.join(args.indir, '*.*'))
    files.sort()
    files.reverse()

    for filename in files:
        name, ext = os.path.splitext(os.path.basename(filename))
        outpath = os.path.join(args.indir, args.prefix + "{0:08d}".format(index) + ext)
        print(filename + " to " + outpath)
        os.rename(filename, outpath)
        index += 1

