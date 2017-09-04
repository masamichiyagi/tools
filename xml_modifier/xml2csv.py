#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, re, glob, shutil, struct, argparse, random
import numpy as np
import xml.etree.ElementTree as xml
import csv
from PIL import Image


## output path
ANNOTDIR = "/data1/docker_caffe/ftn/free_space/Annotations/"
DATASETS = ["front"]


## output csv data
csvlist = []
for dataset in DATASETS:
    xmlfiles = glob.glob(os.path.join(ANNOTDIR, dataset, '*.xml'))
    xmlfiles.sort()

    for xmlfile in xmlfiles:

        # print ("processing {}".format(xmlfile))
        try:
            dom = xml.parse(xmlfile)
        except:
            print 'Cannot parse ' + xmlfile
            sys.exit(1)
        csvlist.append(os.path.basename(xmlfile))

        root = dom.getroot()
        for e in root.findall('*'):
            if (e.tag == 'object'):
                for child in e.findall('*'):
                    if (child.tag == 'bndbox'):
                        xmin = child.find('xmin').text
                        xmax = child.find('xmax').text
                        ymin = child.find('ymin').text
                        ymax = child.find('ymax').text
                        csvlist.append(xmin)
                        csvlist.append(xmax)
                        csvlist.append(ymin)
                        csvlist.append(ymax)
                    else:
                        pass
            else:
                pass
        csvlist.append("\n")

#filename = os.path.basename(xmlfile).split(".")[0]+".csv"
filename = "10000000.csv"
myfile = open(filename, 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
wr.writerow(csvlist)



