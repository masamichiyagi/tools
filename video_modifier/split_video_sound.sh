#!/bin/sh

# copy sound
ffmpeg -i input.mov

# Audiocodec is xxx
ffmpeg -i input.mov -acodec copy -map 0:1 destination.m4a

# Video codec is xxx
ffmpeg -i input.mov -vcodec copy -map 0:0 destination.mov

