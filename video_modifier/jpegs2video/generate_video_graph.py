#!/usr/bin/env python

import numpy as np
import os, sys, glob, cv2, colorsys
import argparse
import xml.etree.ElementTree as xml
import matplotlib.pyplot as plt


LABEL_COLOR_NUM = 100

FONTFACES = (
    cv2.FONT_HERSHEY_SIMPLEX,
    cv2.FONT_HERSHEY_PLAIN,
    cv2.FONT_HERSHEY_DUPLEX,
    cv2.FONT_HERSHEY_COMPLEX,
    cv2.FONT_HERSHEY_TRIPLEX,
    cv2.FONT_HERSHEY_COMPLEX_SMALL,
    cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
    cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
    cv2.FONT_ITALIC );


def labelToColor(label):
    hseed = hash(label)
    h = hseed % LABEL_COLOR_NUM / float(LABEL_COLOR_NUM)
    rgba = [int(x * 255) for x in colorsys.hsv_to_rgb(*(h, 0.8, 0.5))]
    return rgba

parser = argparse.ArgumentParser(description='Generate Video')
parser.add_argument('-x', '--xmldir',
                    dest='xmldir',
                    help='xml directory',
                    required=True)
parser.add_argument('-i', '--imgdir',
                    dest='imgdir',
                    help='img directory',
                    required=True)
parser.add_argument('-o', '--output',
                    dest='output',
                    help='output filename',
                    required=True)
parser.add_argument('-f', '--fps',
                    dest='fps',
                    help='frame rate',
                    required=False)
parser.add_argument('-g', '--graph',
                    dest='graph',
                    help='draw graph flag',
                    required=False)
parser.add_argument('-c', '--category',
                    dest='category',
                    default='person',
                    help='category',
                    required=False)

args = parser.parse_args()


fontface = FONTFACES[0] | FONTFACES[8]
fontsize = 0.8 
fonttick = 1

fourcc = cv2.cv.CV_FOURCC(*'XVID')
fwidth = 1920
fheight = 1080
fps = 30 
if not (args.fps):
    fps = 30
else:
    fps = int(args.fps)

out = None # cv2.VideoWriter(args.output, fourcc, 30, (int(fwidth), int(fheight)))


def draw_annotation(im, cls, score, bbox, color):
    xmin, ymin, xmax, ymax = bbox.astype(int)
    ## draw bbox & text
    ## text = '{:s}:{:d}%'.format(cls, score)
    text = '{:s}'.format(cls)
    tw, th = cv2.getTextSize(text, fontface, fontsize, fonttick)[0]
    tmargin = 6
    cv2.rectangle(im, (xmin, ymin), (xmax, ymax), color, 7)
    cv2.rectangle(im, (xmin, ymin - th - tmargin), (xmin + tw + tmargin, ymin), color, -1)
    cv2.putText(im, text, (xmin + 4, ymin - 4), fontface, fontsize, (255,255,255), fonttick, cv2.CV_AA)
    return im

def draw_class_count(im, count, max_count):
    fontsize = 4
    h_index = 720
    v_index = 240
    v2_index = 95 
    cv2.rectangle(im, (im.shape[1]-h_index, 0), (im.shape[1], v2_index), (255,255,255), thickness=cv2.cv.CV_FILLED)
    #cv2.putText(im, args.category + " count: " + str(count), (im.shape[1]-h_index+20, v_index-20), fontface, fontsize, (0,0,0), fonttick, cv2.CV_AA)
    cv2.putText(im, "count: " + str(count), (im.shape[1]-h_index+20, v2_index), fontface, fontsize, (0,0,0), fonttick, cv2.CV_AA)
    #cv2.putText(im, "max: " + str(max_count), (im.shape[1]-h_index+20, v_index-20), fontface, fontsize, (0,0,0), fonttick, cv2.CV_AA)
    return im

class GraphRenderer():
    def __init__(self):
        self.fig, self.ax = plt.subplots(1, 1)
        self.ax.spines['right'].set_color('None')
        self.ax.spines['left'].set_color('None')
        self.ax.spines['top'].set_color('None')
        self.ax.spines['bottom'].set_color('None')
        self.ax.tick_params(axis='x', which='both', top='off', bottom='off', labelbottom='off')
        self.ax.tick_params(axis='y', which='both', left='on', right='off', labelleft='on')
        self.ax.set_ylim((0, 71))
        plt.rcParams['font.size'] = 60 
        self.x = np.arange(120)
        self.y = np.zeros(120)
        self.lines, = self.ax.plot(self.x, self.y)

        self.alpha = 0.0

    def draw_graph(self, im, count):
        self.x = np.delete(self.x, 0)
        self.x = np.append(self.x, np.max(self.x) + 1)
        self.y = np.delete(self.y, 0)
        self.y = np.append(self.y, count)
        self.ax.set_xlim((self.x.min(), self.x.max()))
        self.lines.set_data(self.x, self.y)
        plt.fill_between(self.x, 0, self.y, facecolor='y', alpha=0.5)
        plt.savefig("graph.png", dpi=40)

        graph = cv2.imread("graph.png", 1)
        g_height,g_width ,channels = graph.shape
        height, width = im.shape[:2]
        overlay = im.copy()
        overlay[95:95+g_height, width-g_width:width] = graph
        im = cv2.addWeighted(im, self.alpha, overlay, 1-self.alpha, 0)
        return im
    
flist = []
if (os.path.exists(args.xmldir)):
    xmlfiles = glob.glob(os.path.join(args.xmldir, '*.xml'))
    flist = [int(os.path.splitext(os.path.basename(f))[0]) for f in xmlfiles]
    flist.sort()
else:
    print ("xmldir does not exists : " + args.xmldir)
    sys.exit(1)

gr = GraphRenderer()
max_count = 0
    
for fid in flist:
    imgfile = os.path.join(args.imgdir, "{:08d}.jpg".format(fid))
    print "load imgfile: " + imgfile
    try:
        im = cv2.imread(imgfile)
        if not (out):
            fheight, fwidth, channels = im.shape
            out = cv2.VideoWriter(args.output, fourcc, fps, (int(fwidth), int(fheight)))
    except:
        print 'Cannot load ' + imgfile
    
    xmlfile = os.path.join(args.xmldir, "{:08d}.xml".format(fid))
    print "load xmlfile: " + xmlfile
    try:
        dom = xml.parse(xmlfile)
    except:
        print 'Cannot parse ' + xmlfile

    count = 0
    root = dom.getroot()
    for obj in root.findall('object'):
        idlist = [int(objid.text) for objid in obj.findall('objid')]
        cls    = obj.find('name').text

        #############################
        ## Added by yagi. 20170211
        #############################
        if args.category == cls:
            count += 1

        score  = 0 # obj.find('accuracy').text
        bbox = obj.find("bndbox")
        xmin = int(bbox.find("xmin").text)
        ymin = int(bbox.find("ymin").text)
        xmax = int(bbox.find("xmax").text)
        ymax = int(bbox.find("ymax").text)

        box = np.array([xmin, ymin, xmax, ymax])
        # if (cls in COLORS):
        #     color = (COLORS[cls][2], COLORS[cls][1], COLORS[cls][0])
        # else:
        color = labelToColor(cls) # (128, 128, 128)
        im = draw_annotation(im, cls, int(score), box, color)
    #############################
    ## draw overlay graph(counter)
    #############################
    if (args.graph):
        if (max_count < count):
            max_count = count
        im = draw_class_count(im, count, max_count)
        im = gr.draw_graph(im, count)

  # cv2.putText(im, '{:d}/{:d}'.format(fid, max(flist)), (25, 25), fontface, 0.8, (159, 35, 89), fonttick, cv2.CV_AA)
  # cv2.putText(im, '{:d}/{:d}'.format(fid, max(flist)), (25, 25), fontface, 0.8, (159, 35, 89), fonttick, cv2.CV_AA)

    out.write(im)

    
out.release()

sys.exit()


    
