#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import os, sys, glob, argparse
import numpy as np
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from xml.dom import minidom



###################################
## Argument Parser
###################################
def arg_parser():
    parser = argparse.ArgumentParser(description='Filter')
    parser.add_argument('-b', '--basedir',  dest='basedir',  help='base annotation file directory', required=True)
    parser.add_argument('-x', '--anndir',  dest='anndir',  help='append annotation file directory', required=True)
    parser.add_argument('-o', '--outdir',  dest='outdir',  help='output file directory', required=True)
    args = parser.parse_args()

    if (not os.path.exists(args.basedir)):
        print ("input directory does not exists : " + args.basedir)
        sys.exit(1)
    if (not os.path.exists(args.anndir)):
        print ("annotation directory does not exists : " + args.anndir)
        sys.exit(1)
    if (not os.path.exists(args.outdir)):
        print ("annotation directory does not exists : " + args.outdir)
        sys.exit(1)
    return args

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

###################################
## Filter function
###################################
def filters(basefname, xmlfname):
    basetree = ElementTree.parse(basefname)
    baseroot = basetree.getroot()
    tree = ElementTree.parse(xmlfname)
    root = tree.getroot()
    for object_iter in root.findall('object'):
        for obj_name_node in object_iter.findall('name'):
            #if "bike" == obj_name_node.text:
            #    baseroot.append(object_iter)
            #if "vehicle" == obj_name_node.text:
            #    baseroot.append(object_iter)
            #if "signal" == obj_name_node.text:
            #    baseroot.append(object_iter)
            if "person" == obj_name_node.text:
                baseroot.append(object_iter)
    return basetree

###################################
## Main roop
###################################
if __name__ == "__main__":
    args = arg_parser()
    files = glob.glob(os.path.join(args.basedir, '*.xml'))
    files.sort()
    print("file num: " + str(len(files)))

    for basefname in files:
        xmlfname, ext = os.path.splitext(os.path.basename(basefname))
        xmlfname = os.path.join(args.anndir, xmlfname + '.xml') 
        result = filters(basefname, xmlfname)
        outpath = os.path.join(args.outdir, os.path.basename(xmlfname))
        result.write(outpath)

