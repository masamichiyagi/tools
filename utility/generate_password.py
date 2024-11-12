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
import glob
import random
import string

###################################
## Argument Parser
###################################
def arg_parser():
    parser = argparse.ArgumentParser(description='Filter')
    parser.add_argument('-l', '--length',  dest='length',  help='password length', default='8', required=False)
    args = parser.parse_args()

    return args


###################################
## Main roop
###################################
if __name__ == "__main__":
    args = arg_parser()
    length = int(args.length)
    randlst = [random.choice(string.ascii_letters + string.digits + '_') for i in range(length)]
    print(''.join(randlst))

