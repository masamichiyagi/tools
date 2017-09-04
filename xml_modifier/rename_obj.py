# -*- coding: utf-8 -*-
#/usr/bin/python
import os, glob 
import sys
import itertools
import subprocess
import argparse

from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from xml.dom import minidom

#################################################
## Argument Parser Definition
#################################################
parser = argparse.ArgumentParser(description='XML Filters: xml parser')
parser.add_argument('-a', '--anndir',  dest='anndir',  help='Annotations directory', required=True)
parser.add_argument('-o', '--outputdir',  dest='outdir',  help='output directory', required=True)
args = parser.parse_args()

if (not os.path.exists(args.anndir)):
    print ("Annotation directory does not exists : " + args.anndir)
    sys.exit(1)

#################################################
## Gloval Variables Definition
#################################################
obj_name = "person"
obj_rename = "bottle"


#################################################
## Filtering function
#################################################
def parseXML(filepath, filterids = []):
    tree = ElementTree.parse(filepath)
    root = tree.getroot()
    for object_iter in root.findall('object'):
        if(obj_name == object_iter.find('name').text):
            object_iter.find('name').text = obj_rename
    return tree



#################################################
## Main roop
#################################################
# Get file list
annFiles = sorted(glob.glob(os.path.join(args.anndir, '*.xml')))

for fname in annFiles:
    # Filtering
    result = parseXML(fname)

    # Save files
    outpath = os.path.join(args.outdir, os.path.basename( fname ) )
    result.write(outpath)



