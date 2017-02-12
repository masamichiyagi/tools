# -*- coding: utf-8 -*-
import cv2
import matplotlib.pyplot as plt
import numpy as np

class DrawGraph:
    def __init__(self):
        self.fig, self.ax = plt.subplots(1, 1)
        self.ax.spines['right'].set_color('None')
        self.ax.spines['left'].set_color('None')
        self.ax.spines['top'].set_color('None')
        self.ax.spines['bottom'].set_color('None')
        self.ax.tick_params(axis='x', which='both', top='off', bottom='off', labelbottom='off')
        self.ax.tick_params(axis='y', which='both', left='on', right='off', labelleft='on')
        self.ax.set_ylim((0, 21))
        plt.rcParams['font.size'] = 60 
        self.x = np.arange(120)
        self.y = np.zeros(120)
        self.lines, = self.ax.plot(self.x, self.y)
        self.alpha = 0.3
        print(self.x)
     
    def draw_graph(self, im, count):
        self.x = np.delete(self.x, 0)
        self.x = np.append(self.x, np.max(self.x) + 1)
        self.y = np.delete(self.y, 0)
        self.y = np.append(self.y, count)
        self.ax.set_xlim((self.x.min(), self.x.max()))
        self.lines.set_data(self.x, self.y)
        plt.fill_between(self.x, 0, self.y, facecolor='y', alpha=0.5)
        plt.savefig("graph.png", dpi=25)

        graph = cv2.imread("graph.png", 1)
        g_height,g_width ,channels = graph.shape
        height, width = im.shape[:2]
        overlay = im.copy()
        overlay[20:20+g_height, width-g_width:width] = graph
        im = cv2.addWeighted(im, self.alpha, overlay, 1-self.alpha, 0.0)
        return im

if __name__=="__main__":
    capture = cv2.VideoCapture(0)
    if capture.isOpened() is False:
        raise("IO Error")
    cv2.namedWindow("Capture", cv2.WINDOW_AUTOSIZE)

    dg = DrawGraph()
    i = 0.1

    while(capture.isOpened()):
        ret, image = capture.read()
        if ret==True:
            image = dg.draw_graph(image, 11+ 10* np.sin(i))
            i += 0.1
            cv2.imshow("Capture", image)
            # any key
            if cv2.waitKey(33) >= 0:
                break
        else:
            break
    capture.release()
    cv2.destroyAllWindows()

