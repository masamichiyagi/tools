#!/bin/sh
python jpeg2video.py --imgdir imgdir/ --output out.avi --fps 30
python png2video.py  --imgdir imgdir/ --output out.avi --fps 30

python png2video_2disp.py --imgdir imgdir/ --originimgdir originimgdir/ --output out.avi 
