#!/bin/bash

#ffmpeg -i $1 -vcodec wmv2 -an -pass 1 -passlogfile "./pass.log" output.wmv
#ffmpeg -i $1 -vcodec wmv2 -an -b 3000k -pass 2 -passlogfile "./pass.log" output.wmv


ffmpeg -i $1 -vcodec wmv2 -vf fps=30 -an -b 6000k -pass 1 -passlogfile "./pass.log" $2
