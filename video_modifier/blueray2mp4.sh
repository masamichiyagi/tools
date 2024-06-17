#!/bin/bash
#ffmpeg_v3.2.2 -i $1 -vcodec libx264 -vf subtitles=$1 -acodec aac ~/Desktop/movie/${1%.*}.mp4

## quority 1
#ffmpeg_v3.2.2 -i $1 -vcodec libx264 -q:v 1 -acodec aac -map 0:v -map 0:a -map_chapters -1 -metadata title=$2 ~/Desktop/movie/${1%.*}.mp4

## no quority option
#ffmpeg_v3.2.2 -i $1 -vcodec libx264 -acodec aac -map 0:v -map 0:a -map_chapters -1 -metadata title=$2 ~/Desktop/movie/${1%.*}.mp4

## resize option
ffmpeg_v3.2.2 -i $1 -vcodec libx264 -vf scale=1280:-1 -acodec aac -map 0:v -map 0:a -map_chapters -1 -metadata title=$2 ~/Desktop/movie/${1%.*}.mp4
