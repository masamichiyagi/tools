#!/usr/bin/python
import os, glob 
import sys
import itertools
import subprocess
import argparse

from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from xml.dom import minidom

parser = argparse.ArgumentParser(description='xml parser')
parser.add_argument('-a', '--anndir',  dest='anndir',  help='Annotations directory', required=True)
# example: outputimg/ 
parser.add_argument('-o', '--outputdir',  dest='output',  help='output img directory', required=True)
args = parser.parse_args()

if (not os.path.exists(args.anndir)):
    print ("image directory does not exists : " + args.anndir)
    sys.exit(1)


def parseXML(filepath, filterids = []):
    tree = ElementTree.parse(filepath)
    root = tree.getroot()
    for object_iter in root.findall('object'):
        for obj_name_node in object_iter.findall('name'):
            if "door" == obj_name_node.text:
                for obj_bndbox_node in object_iter.findall('bndbox'):
                    for obj_xmin_node in obj_bndbox_node.findall('xmin'):
                        if int(obj_xmin_node.text) < 500 : 
                            root.remove(object_iter)
    return tree


annFiles = sorted(glob.glob(os.path.join(args.anndir, '*.xml')))

for fname in annFiles:
    # filtering
    result = parseXML(fname)
    # save
    outpath = os.path.join(args.output, os.path.basename( fname ) )
    result.write(outpath)



