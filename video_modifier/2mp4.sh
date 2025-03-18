#!/bin/bash
#ffmpeg -i $1 -an $1".mp4"
#ffmpeg -i $1 -pix_fmt yuv420p -an $1".mp4"
#ffmpeg -i $1 -pix_fmt yuv420p -vf setpts=PTS/8.0 -an $1".mp4"
#ffmpeg -i $1 -pix_fmt yuv420p -s 640x400 -aspect 16:9 -vf setpts=PTS/2.0  -an $1".mp4"
## mkv2mp4, flv2mp4
#ffmpeg -i $1 -q:v 1 -vcodec libx264 -acodec aac $1.mp4
## blue-ray mkv2mp4
#ffmpeg_v3.2.2 -i $1 -q:v 1 -vcodec libx264 -acodec aac -map 0:0 -map 0:1 -map_chapters -1 -metadata title=$2 $1.mp4


################################################
## Option: Play Power Point -> -pix_fmt yuv420p
################################################
## Option: h265
# -vcodec h265 -tag:v hvc1
################################################

################################################
## Option: a n-speed -> -vf setpts=PTS/n.0
################################################

################################################
## Option: No audio -> -an
################################################

################################################
## image to mp4
################################################
# ffmpeg -r 60 -loop 1 -i input.png -t 2.0 -vcodec libx264 -pix_fmt yuv420p output.mp4
# ffmpeg -r 30000/1001 -loop 1 -i input.png -t 2.0 -vcodec libx264 -pix_fmt yuv420p output.mp4
# ffmpeg -loop 1 -i input.png -t 0:0:6 -vcodec libx264 -pix_fmt yuv420p out.mp4
# ffmpeg -f lavfi -i color=c=black:s=1920x1080:r=30000/1001 -t 0:0:5 a.mp4
# ffmpeg -f lavfi -i color=c=black:s=960x540:r=30000/1001 -t 0:0:5 a.mp4

################################################
## mp4 to image
################################################
# ffmpeg -ss 0:0:0 -i input.mp4 -vcodec png -r 1 -t 0:0:1 img%03d.png
# ffmpeg -i input.mp4 -ss 0:0:0 -vcodec png -r 1 -t 0:0:1 img%03d.png

################################################
## Option: resize 1920x1080, 1280x720, 1024x576, 960x540
## -s 1920x1080 -aspect 16:9 -acodec copy
################################################
## crop
################################################
# ffmpeg -i $1 -vf crop=960:600:0:0 -acodec copy $1".mp4"

################################################
## hiritsu change
################################################
# ffmpeg -i in.mp4 -vf scale=1920:-1 out.mp4
# ffmpeg -i in.mp4 -vf scale=1280:-1 out.mp4

################################################
## Option: -q:v 1 quority
################################################
################################################
## -crf 18 ...High Quority
## -crf 23 ...Default
## -crf 28 ...Low Quority
## -b:v 40000k ...High Quority
################################################

################################################
## Option: -vf yadif
## deinterlace. for dvd option. Reduce the visibility of stripes
################################################

################################################
## 0.5倍
################################################
# ffmpeg -i input.mp4 -vf setpts=PTS/0.5 -af atempo=0.5 output_x0.5.mp4

################################################
# concat mp4 files
################################################
## mylist.txt
## file /path/to/fileA.mp4
## file /path/to/fileB.mp4
################################################
## ffmpeg -f concat -safe 0 -i mylist.txt -c copy output.mp4
################################################
# -c:s copy -map 0:v -map 0:a -map 0:s?

################################################
# concat flv files
################################################
## mylist.txt
## file fileA.flv
## file fileB.flv
################################################
## ffmpeg -f concat -i mylist.txt -vcodec libx264 -acodec aac output.mp4
################################################
### mkv2mp4
# ffmpeg -i $1 -vcodec libx264 -acodec aac $1.mp4

################################################
# concat mp4, aac files
################################################
#ffmpeg -i video.mp4 -i audio.wav -vcodec copy -acodec aac -map 0:v:0 -map 1:a:0 output.mp4

################################################
# bitmap jimaku overlay: hard encoding is needed
################################################
# ffmpeg -i in.mkv -filter_complex "[0:v][0:s]overlay[v]" -map "[v]" -map 0:1 -acodec aac out.mp4
# NG step1: ffmpeg -i in.mp4 -i in.ass -vcodec copy -acodec aac -scodec mov_text out.mp4
# NG step2: ffmpeg -i in.mp4 -i in.ass -filter_complex "[0:v][1:s]overlay[v]" -map "[v]" -map 0:1 -acodec aac out.mp4
# OK: ffmpeg -i in.mp4 -i in.ass -map 0:v -map 0:a -map 1 -metadata:s:s:0 language=jpn -vcodec copy -acodec copy -scodec copy out.mkv
################################################
# text jimaku overlay: hard encoding is needed
################################################
# ffmpeg -i in.mp4 -vf subtitles=subtitles.ass out.mp4
# ffmpeg -i in.mp4 -vf subtitles=1.ass,subtitles=2.ass out.mp4 # 2 subtitles encode
# ffmpeg -i in.mkv -vf subtitles=in.mkv out.mp4
# ffmpeg -i in.mp4 -vf "subtitles=jimaku.srt:force_style='Fontsize=26,FontName=Meiryo UI'"
## background color black
# OutlineColour=&H80000000,BorderStyle=3,Outline=1,Shadow=0,MarginV=20

################################################
## chapter split
## -t: kiridashi sec.msec
## -ss 30.0 -t 10.1 : 30.0sec to 40.1sec
################################################
# ffmpeg -ss 0.000000 -i in.mkv -vcodec libx264 -acodec aac -t 1168.959458 out.mp4
# -scodec copy, -scodec mov_text (mp4), -scodec ass(mkv)

################################################
## chapter delete
################################################
# -map_chapters -1 

################################################
## check max dB
################################################
## -af volumedetect -f null -
## output sample: -11dB -> you can tuning as if "-af volume=11dB"

################################################
## audio volume up
################################################
## -af volume=10dB
## -af volume=-5dB

################################################
## audio 320kbps
# -ab 320k
# -ab 256k
## audio 44100 Hz
# -ar 44100
## audio flac
# -acodec flac -f flac
################################################

################################################
## yohaku tuika
################################################
# ffmpeg -i input -vf pad=iw+462:0:231:0:black output

################################################
## multi filter, filter chain
## -vf "filter_a=aaa,filter_b,filter_c=xxx"
################################################
# ffmpeg -i input -vf "pad=iw+462:0:231:0:black,scale=1920:-1" output

################################################
## fps change
## -r 10 : 10fps
################################################

################################################
## title change
## -metadata "title"="hogehoge"
################################################

################################################
## audio language change
## -metadata:s:a:0 language=jpn
################################################

################################################
## audio stream swap, audio stream change
## -vcodec copy -acodec copy -map 0:v -map 0:a:1 -map 0:a:0 
################################################

################################################
## audio default stream change
## -disposition:a:0 default -disposition:a:1 0
## 0 is deleting default.
################################################

################################################
## audio offset insert
################################################
# ffmpeg -y -i movie.mp4 -itsoffset 00:00:03 -i audio.m4a -vcodec copy -bsf:a aac_adtstoasc -async 1 -strict -2 out.mp4

################################################
## audio 7.1ch to 5.1ch
################################################
# ffmpeg -i input.mkv -vn -ac 6 -c:a aac 6ch.m4a

################################################
## video offset insert
################################################
## start offset 10 frame, color black
# -vf tpad=start=10
## start offset 10 sec, color white
# -vf tpad=start_duration=10:color=white
## end offset 10 frame, color last picture
# -vf tpad=stop=10:stop_mode=clone

################################################
## mirror
################################################
# ffmpeg -i input -vf vflip out.mp4
# ffmpeg -i input -vf hflip out.mp4

################################################
## left right marge hikaku
################################################
# ffmpeg -i right.mp4 -vf "[in] pad=2*iw:ih:iw:0 [right];movie=left.mp4[left];[right][left] overlay" out.mp4
# ffmpeg -i up.mp4 -vf "[in] pad=iw:2*ih [up];movie=down.mp4[down];[up][down] overlay=0:H/2" out.mp4


################################################
## overlay
## input1: bottom, input2: top
################################################
# ffmpeg -i input1 -i input2 -filter_complex "overlay=x=512:y=0" output
################################################
## overlay 途中に差し込み
## delay : setpts=PTS-STARTPTS+time/TB[hoge]
################################################
# ffmpeg -i input1 -i input2 -filter_complex "[1:v]setpts=PTS-STARTPTS+22.89/TB[top];[0:v][top]overlay=x=512:y=0:enable='between(t,22.89,40.28)'" output
################################################
## すかしを消す
## crop -> overlay
################################################
# ffmpeg -i bottom.mp4 -i top.mp4 -filter_complex "[1:v]fps=25,scale=1280:-1,crop=154:50:1106:644,setpts=PTS-STARTPTS-0.04[top];[1:v]fps=25,scale=1280:-1,crop=154:50:1106:644[top3];[0:v][top]overlay=x=1108:y=646:enable='between(t,0,28.72)'[top2];[top2][top3]overlay=x=1108:y=646:enable='between(t,34.88,177.31)'" -b:v 5400k  -an output.mp4

################################################
## transparent :
## colorkey=green
## colorkey=0x00FF00:0.01:0
## colorkey=0x00FF00:0.01:0.5
## colorkey=0x00FF00:0.01:1
################################################

################################################
## クロマキー合成: green screen transparent
## -filter_complex "[1:v]colorkey=0x00FF00:0.01:1[top];[0:v][top]overlay=x=0:y=0" -preset ultrafast
################################################

################################################
## 画像半透明化合成
## -i bottom.mp4 -i top.png -filter_complex "[1:v]lut=a='val*0.5',[0:v]overlay=x=0:y=0" 
################################################

################################################
## multi filter complex
## sample : 画像半透明化合成、字幕合成
## -i bottom.mp4 -i top.png -filter_complex "[1:v]lut=a='val*0.5'[top];[0:v][top]overlay=x=0:y=0[j];[j]subtitles=jimaku.srt" 
################################################



################################################
## to VOB(DVD)
################################################
# -target ntsc-dvd output.vob
# sample : ffmpeg -i input.mp4 -acodec copy -target ntsc-dvd output.vob


################################################
## Sync
################################################
# ffmpeg -i input.mp4 -c:v copy temp.h264 -c:a copy temp.aac
# ffmpeg -r 30000/1001 -i temp.h264 -i temp.aac -c copy output.mp4

#/bin/bash
# -fv crop=newwidth:newheight:cut left:cut top
# crop: -vf crop=640:360:0:60
# audio copy: -acodec copy
# no audio: -an
# for power point : -pix_fmt yuv420p     :or: -vf format=yuv420p

ffmpeg -i $1 -vcodec libx264 -an -movflags faststart output.mp4

################################################
## Download web movie
################################################
# url m3u8 to mp4
ffmpeg -i $1 -c copy -bsf:a aac_adtstoasc -movflags faststart $2

################################################
## AES-128 Encryption
### video.keyinfo
#### key file name
#### path to the key file
#### for example vim video.keyinfo
################################################
#### key.bin
#### ./key.bin
################################################
ffmpeg -i input.mp4 -c:v copy -c:a copy -f hls -hls_key_info_file video.keyinfo -hls_time 9 -hls_playlist_type vod -hls_segment_filename "stream%3d.ts" stream.m3u8

################################################
## AES-128 Decryption
################################################
ffmpeg -allowed_extensions ALL -i stream.m3u8 -c copy output.mp4

################################################
## fade out
## -vf fade=t=out:st=4:d=1
################################################

