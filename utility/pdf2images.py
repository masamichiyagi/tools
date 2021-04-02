# -*- coding: utf-8 -*-
from pdf2image import convert_from_path
from pdf2image import convert_from_bytes
import os
import sys
import glob
import argparse


###################################
## Argument Parser
###################################
def arg_parser():
    parser = argparse.ArgumentParser(description='Filters')
    parser.add_argument('-i', '--infile',  dest='infile',  help='input file', required=True)
    parser.add_argument('-e', '--expansion',  dest='expansion',  help='expansion', default='png', required=False)
    args = parser.parse_args()

    if (not os.path.exists(args.infile)):
        print ("input file does not exists : " + args.infile)
        sys.exit(1)
    return args


###################################
## Main roop
###################################
def main():
    args = arg_parser()

    images = convert_from_path(args.infile, 300) #300=DPI
    print(images)
    #images = convert_from_bytes(open(args.infile, 'rb').read())
    for i in range(len(images)):
        images[i].save(args.infile + "-{0:03d}".format(i) + "." + args.expansion, args.expansion)

if __name__ == '__main__':
    main()
