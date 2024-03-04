TITLE=`yt-dlp -e $1`
OUT_FNAME=`echo "$2_${TITLE}.mp4" | sed "s@/@_@g"`

OPTION_RESULT=$(yt-dlp $1 -F)
VIDEO_OPTION=$(echo $OPTION_RESULT | grep "137 mp4" | wc -l)
if [ ${VIDEO_OPTION} = 1 ]; then
  VIDEO_OPTION=137
else
  VIDEO_OPTION=$(echo $OPTION_RESULT | grep "136 mp4" | wc -l)
  if [ ${VIDEO_OPTION} = 1 ]; then
    VIDEO_OPTION=136
  else
    VIDEO_OPTION=$(echo $OPTION_RESULT | grep "135 mp4" | wc -l)
    if [ ${VIDEO_OPTION} = 1 ]; then
      VIDEO_OPTION=135
    else
      VIDEO_OPTION=134
    fi
  fi
fi
AUDIO_OPTION=$(echo $OPTION_RESULT | grep "22 m4a" | wc -l)
if [ ${AUDIO_OPTION} = 1 ]; then
  AUDIO_OPTION=22
  WORK2FNAME=work2.mp4
else
  AUDIO_OPTION=140
  WORK2FNAME=work2.m4a
fi


#VIDEO_OPTION=$(yt-dlp $1 -F | grep "137 mp4" | wc -l)
#if [ ${VIDEO_OPTION} = 1 ]; then
#  VIDEO_OPTION=137
#else
#  VIDEO_OPTION=$(yt-dlp $1 -F | grep "136 mp4" | wc -l)
#  if [ ${VIDEO_OPTION} = 1 ]; then
#    VIDEO_OPTION=136
#  else
#    VIDEO_OPTION=135
#  fi
#fi
#AUDIO_OPTION=$(yt-dlp $1 -F | grep "22 m4a" | wc -l)
#if [ ${AUDIO_OPTION} = 1 ]; then
#  AUDIO_OPTION=22
#  WORK2FNAME=work2.mp4
#else
#  AUDIO_OPTION=140
#  WORK2FNAME=work2.m4a
#fi
echo "TITLE: $2_${TITLE}.mp4"
echo "AUDIO OPTION: ${AUDIO_OPTION}"
echo "VIDEO OPTION: ${VIDEO_OPTION} is downloading."
yt-dlp $1 -f ${VIDEO_OPTION} -o work1.mp4
if [ ${AUDIO_OPTION} = 22 ]; then
  WORK2FNAME=work2.mp4
else
  WORK2FNAME=work2.m4a
fi
echo "AUDIO OPTION: ${AUDIO_OPTION}, ${WORK2FNAME} is downloading."
yt-dlp $1 -f ${AUDIO_OPTION} -o ${WORK2FNAME}
echo "${WORK2FNAME} is downloaded."

ffmpeg -i work1.mp4 -i ${WORK2FNAME} -map 0:v -map 1:a -vcodec copy -acodec copy "${OUT_FNAME}"
echo "${OUT_FNAME} is completed."

echo "remove work file."
rm work1.mp4
rm ${WORK2FNAME}
