#!/usr/bin/python
import os, sys, glob, cv2
import itertools
import subprocess
import argparse

from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from xml.dom import minidom

###################################
## Argument Parser
###################################
def arg_parser():
    parser = argparse.ArgumentParser(description='OpenCV Filters')
    parser.add_argument('-i', '--indir',  dest='indir',  help='input file directory', required=True)
    parser.add_argument('-a', '--anndir',  dest='anndir',  help='Annotations directory', required=True)
    parser.add_argument('-o', '--outdir',  dest='outdir',  help='output file directory', required=True)
    parser.add_argument('-e', '--expansion',  dest='expansion',  help='expansion', default='jpg', required=False)
    args = parser.parse_args()

    if (not os.path.exists(args.indir)):
        print ("input directory does not exists : " + args.indir)
        sys.exit(1)
    if (not os.path.exists(args.anndir)):
        print ("annotation directory does not exists : " + args.anndir)
        sys.exit(1)
    if (not os.path.exists(args.outdir)):
        print ("output directory does not exists : " + args.outdir)
        sys.exit(1)
    return args



def parseXML(imgfname, xmlfname, filterids = []):
    im = cv2.imread(imgfname)
    height, width = im.shape[:2]
    tree = ElementTree.parse(xmlfname)
    root = tree.getroot()
    for object_iter in root.findall('object'):
        for obj_bndbox_node in object_iter.findall('bndbox'):
            for obj_xmax_node in obj_bndbox_node.findall('xmax'):
                if int(obj_xmax_node.text) > width :
                    print(xmlfname, "fixed: xmax ", obj_xmax_node.text, " to ", width)
                    obj_xmax_node.text = str(width)
            for obj_ymax_node in obj_bndbox_node.findall('ymax'):
                if int(obj_ymax_node.text) > height:
                    print(xmlfname, "fixed: ymax ", obj_ymax_node.text, " to ", height)
                    obj_ymax_node.text = str(height)
            for obj_xmin_node in obj_bndbox_node.findall('xmin'):
                if int(obj_xmin_node.text) < 0:
                    print(xmlfname, "fixed: xmin ", obj_xmin_node.text, " to 0")
                    obj_xmin_node.text = str(0)
            for obj_ymin_node in obj_bndbox_node.findall('ymin'):
                if int(obj_ymin_node.text) < 0:
                    print(xmlfname, "fixed: ymin ", obj_ymin_node.text, " to 0")
                    obj_ymin_node.text = str(0)

    return tree


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
        # filtering
        result = parseXML(imgfname, xmlfname)
        # save
        outpath = os.path.join(args.outdir, os.path.basename( xmlfname ) )
        result.write(outpath)

