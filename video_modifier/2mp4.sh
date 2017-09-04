#/bin/bash
# -fv crop=newwidth:newheight:cut left:cut top
# crop: -vf crop=640:360:0:60
# audio copy: -acodec copy
# no audio: -an
# for power point : -pix_fmt yuv420p     :or: -vf format=yuv420p

ffmpeg -i $1 -movflags faststart -vcodec libx264 -an output.mp4
