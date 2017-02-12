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
    parser.add_argument('-i', '--indir',  dest='indir',  help='input file directory', required=True)
    parser.add_argument('-x', '--anndir',  dest='anndir',  help='annotation file directory', required=True)
    parser.add_argument('-e', '--expansion',  dest='expansion',  help='expansion', default='jpg', required=False)
    args = parser.parse_args()

    if (not os.path.exists(args.indir)):
        print ("input directory does not exists : " + args.indir)
        sys.exit(1)
    if (not os.path.exists(args.anndir)):
        print ("annotation directory does not exists : " + args.anndir)
        sys.exit(1)
    return args

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

###################################
## Filter function
###################################
def filters(filename, xmlfname):
    im = cv2.imread(filename, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.1, 3)

    if len(faces) > 0:
        
        for (x, y, w, h) in faces:
            result = parseXML(xmlfname, x, y, w, h)
            #cv2.rectangle(im, (x,y), (x+w, y+h), (0,0,0), thickness=2)
    else:
        print "no face"
    return result

def parseXML(filepath, x, y, w, h, filterids = []):
    root = ElementTree.parse(filepath).getroot()
    obj  = Element('object')
    ElementTree.SubElement(obj, "name").text = "face"
    bndbox = ElementTree.SubElement(obj, "bndbox")
    ElementTree.SubElement(bndbox, "xmin").text = str(x)
    ElementTree.SubElement(bndbox, "ymin").text = str(y)
    ElementTree.SubElement(bndbox, "xmax").text = str(x+w)
    ElementTree.SubElement(bndbox, "ymax").text = str(y+h)
    #ElementTree.SubElement(doc, "name", name="name").text = "face"

    root.append(obj)
    return ElementTree.ElementTree(root)

###################################
## Main roop
###################################
if __name__ == "__main__":
    args = arg_parser()
    files = glob.glob(os.path.join(args.indir, '*.' + args.expansion))
    files.sort()

    for imgfname in files:
        xmlfname, ext = os.path.splitext(os.path.basename(imgfname))
        xmlfname = os.path.join(args.anndir, xmlfname + '.xml') 
        result = filters(imgfname, xmlfname)
        outpath = os.path.join(args.anndir, os.path.basename(xmlfname))
        result.write(outpath)

