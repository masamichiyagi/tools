# -*- coding: utf-8 -*-
import os
import sys
import glob
import argparse
import codecs
import re

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
    parser.add_argument('-r', '--replace',  dest='replace',  help='replae word', default=r'', required=False)
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
def filtering(filename, dst=r''):
    text = ''
    with codecs.open(filename, 'r', 'utf-8', 'ignore') as f:
        Allf = f.read()
        text = re.sub(r'\[\d\]|\[\d{2}\]', dst, Allf, flags=re.MULTILINE)
        #text = Allf.replace('\[\d\]|\[\d{2}\]','')
        #text = Allf.replace('\[[0-9]\]','')
        f.close()
    return text


###################################
## Main roop
###################################
def main():
    args = arg_parser()
    replace_word = args.replace

    # Get file lists
    files = glob.glob(os.path.join(args.indir, '*.' + args.expansion))
    files.sort()

    for fname in files:
        # OpenCV filtering function
        result = filtering(fname, replace_word)

        # To save files, get output path
        outpath = os.path.join(args.outdir, os.path.basename(fname))

        # Save files.
        f = open(outpath,'w')
        f.write(result)
        f.close()


if __name__ == '__main__':
    main()
