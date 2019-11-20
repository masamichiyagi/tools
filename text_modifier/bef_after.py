# -*- coding: utf-8 -*-
import os
import sys
import glob
import argparse
import codecs

#################################################
## Gloval Variables Definition
#################################################


###################################
## Argument Parser
###################################
def arg_parser():
    parser = argparse.ArgumentParser(description='OpenCV Filters')
    parser.add_argument('-i', '--indir',  dest='indir',  help='input file directory', required=True)
    parser.add_argument('-o', '--outdir',  dest='outdir',  help='output file directory', required=True)
    parser.add_argument('-b', '--before',  dest='before',  help='before text', required=True)
    parser.add_argument('-a', '--after',  dest='after',  help='before text', required=True)
    parser.add_argument('-e', '--expansion',  dest='expansion',  help='expansion', default='txt', required=False)
    args = parser.parse_args()

    if (not os.path.exists(args.indir)):
        print ("input directory does not exists : " + args.indir)
        sys.exit(1)
    if (not os.path.exists(args.outdir)):
        print ("annotation directory does not exists : " + args.outdir)
        sys.exit(1)
    return args


#################################################
## OpenCV filtering function
#################################################
def filtering(filename, before, after):
    text = ''
    with codecs.open(filename, 'r', 'utf-8', 'ignore') as f:
        Allf = f.read()
        text = Allf.replace(before, after)
        f.close()
    return text


###################################
## Main roop
###################################
def main():
    args = arg_parser()
    before = args.before
    after = args.after

    # Get file lists
    files = glob.glob(os.path.join(args.indir, '*.' + args.expansion))
    files.sort()

    for fname in files:
        # OpenCV filtering function
        result = filtering(fname, before, after)

        # To save files, get output path
        outpath = os.path.join(args.outdir, os.path.basename(fname))

        # Save files.
        f = open(outpath,'w')
        f.write(result)
        f.close()


if __name__ == '__main__':
    main()
