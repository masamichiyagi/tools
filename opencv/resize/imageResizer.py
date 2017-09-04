# -*- coding: utf-8 -*-

import cv2
import numpy as np

# 拡張するサイズを指定する
width = 1280
height = 720

cv2Version = cv2.__version__
print("opencv:Version is", cv2Version)
# 画像を読み込む
if '3.1.0' == cv2Version:
	screen = cv2.imread("dot_03.bmp",cv2.IMREAD_GRAYSCALE)
else:
	screen = cv2.imread("dot_03.bmp",cv2.CV_LOAD_IMAGE_GRAYSCALE)

# screen を入力画像のサイズに合わせる
width_screen, height_screen = screen.shape
temp = np.zeros_like(screen.shape, dtype=np.uint8)
temp = screen
for i in xrange(int(width/width_screen)):
	temp = cv2.hconcat([temp, screen])

temp2 = np.zeros_like(temp.shape, dtype=np.uint8)
temp2 = temp 
for j in xrange(int(height/height_screen)):
	temp2 = cv2.vconcat([temp2, temp])
screen = temp2

result = np.zeros((height, width, 3), dtype=np.uint8)
for h in xrange(height):
	for w in xrange(width):
		result[h,w] = screen[h,w]

cv2.imwrite('screen.png', result)

