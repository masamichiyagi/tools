# -*- coding: utf-8 -*-
#!/usr/bin/env python

import numpy as np
import sys, os, glob
import argparse
import commands

#################################################
## Argument Parser Definition
#################################################
def arg_parser():
    parser = argparse.ArgumentParser(description='Filter')
    parser.add_argument('-i', '--indir',  dest='indir',  help='input file directory', required=True)
    parser.add_argument('-c', '--copyfile',  dest='copyfile',  help='copy file', default='00000000.xml', required=False)
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
    files = glob.glob(os.path.join(args.indir, '*'))
    flen = len(files)
    print("input file directory length: " + str(flen))
 
    for i in range(flen):
        filename = '{0:08d}'.format(i) + ".xml"
        print("copy "+ args.copyfile+ " to "+ filename)
        commands.getstatusoutput('cp ' + args.copyfile + ' ' + filename);

