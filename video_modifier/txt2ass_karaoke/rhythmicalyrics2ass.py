# -*- coding: utf-8 -*-
import os
import sys
import argparse
import pandas as pd
import re
from datetime import datetime, timedelta

#################################################
## Gloval Variables Definition
#################################################

###################################
## Argument Parser
###################################
def arg_parser():
    parser = argparse.ArgumentParser(description='Tools')
    parser.add_argument('-i', '--infile',  dest='infile',  help='input file', required=True)
    parser.add_argument('-s', '--settings',  dest='settings',  help='settings file', default='settings.ini', required=False)
    args = parser.parse_args()

    return args


#################################################
## Functions
#################################################
def elapsed_time_str(time_delta):
    mseconds = time_delta.total_seconds()
    h = int(mseconds // 3600)
    m = int((mseconds - h * 3600) // 60)
    s = int(mseconds - h * 3600 - m * 60)
    mi = int((mseconds - h * 3600 - m * 60 - s) * 100)
    return "{:02}:{:02}:{:02}.{:02}".format(h, m, s, mi)

def filtering(filename, settings):
    #########################
    # Variables Definition
    #########################
    settings_ini = settings
    lyrics = ""
    f = open(filename)
    lines = f.readlines()
    f.close()

    #########################
    # Read setting file
    #########################
    df = pd.read_csv(settings_ini)
    primarycolour = df[df['key'].isin(['primarycolour'])].iloc[0,1]
    secondarycolour = df[df['key'].isin(['secondarycolour'])].iloc[0,1]
    outlinecolour = df[df['key'].isin(['outlinecolour'])].iloc[0,1]
    backcolour = df[df['key'].isin(['backcolour'])].iloc[0,1]
    backcolour_opacity = df[df['key'].isin(['backcolour_opacity'])].iloc[0,1]
    font = df[df['key'].isin(['font'])].iloc[0,1]
    before_sec = int(df[df['key'].isin(['before_sec'])].iloc[0,1])
    after_sec = int(df[df['key'].isin(['after_sec'])].iloc[0,1])
    res_x = df[df['key'].isin(['res_x'])].iloc[0,1]
    res_y = df[df['key'].isin(['res_y'])].iloc[0,1]
    fontsize = df[df['key'].isin(['fontsize'])].iloc[0,1]
    outline = df[df['key'].isin(['outline'])].iloc[0,1]
    outline_ruby = df[df['key'].isin(['outline_ruby'])].iloc[0,1]
    lineheight = int(df[df['key'].isin(['lineheight'])].iloc[0,1])
    marginbottom = int(df[df['key'].isin(['marginbottom'])].iloc[0,1])
    marginside = int(df[df['key'].isin(['marginside'])].iloc[0,1])

    #########################
    # Write lyrics header
    #########################
    lyrics = "[Script Info]\r\n"
    lyrics += "; [Song Info]\r\n"
    lyrics += "; Artist: \r\n"
    lyrics += "; Lyrics: \r\n"
    lyrics += "; Compose: \r\n"
    lyrics += "; Arrange: \r\n"
    lyrics += "; Year:\r\n"
    lyrics += "; Album: \r\n"
    lyrics += "Title: default\r\n"
    lyrics += "Original Script: \r\n"
    lyrics += "ScriptType: v4.00+\r\n"
    lyrics += "PlayResX: "+ res_x +"\r\n"
    lyrics += "PlayResY: "+ res_y +"\r\n"
    lyrics += "Timer: 100.0000\r\n"
    lyrics += "WrapStyle: 2\r\n"
    lyrics += "\r\n"

    lyrics += "[V4+ Styles]\r\n"
    lyrics += "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\r\n"
    lyrics += "Style: Kanji1,"+font+"," + fontsize +","+ primarycolour +","+ secondarycolour + ","+ outlinecolour +"," + backcolour + ",-1,0,0,0,100,100,0,0,1,"+ outline + ",3,1,50,50,30,128\r\n"
    lyrics += "\r\n"

    #########################
    # Variables Definition
    #########################
    res_x = int(res_x)
    res_y = int(res_y)
    fontsize = int(fontsize)
    outline = int(outline)

    start_minus_flg = 0
    gyo_start_sec = 0
    gyo_start_time = 0
    gyo_end_sec = 0
    gyo_end_time = 0
    gyo = 0
    track = 1
    ASStable = []
    
    lyrics += "[Events]\r\n"
    lyrics += "Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text\r\n"

    #########################
    # while read lines
    #########################
    for line in lines:
        #########################
        # Variables Definition
        #########################
        lyrics_a="" # lyrics of line
        words=""
        track = 1
        multiline = 0
        row_count = 0
        comu_sec = 0 # time tag
        rows = re.split('[\[\]]', line)

        #########################
        # Error check
        #########################
        if re.match('^\r\n$',line): # Only new line
            continue
        elif not re.match('(^\r\n$|^$)',rows[len(rows)-1]):
            print(rows, rows[len(rows)-1])
            print("Error : {}行目に終了タグがありません".format(gyo+1))
            sys.exit(1)
        elif not re.match('^$',rows[0]):
            print(rows, rows[len(rows)-1])
            print("Error : {}行目に開始タグがありません".format(gyo+1))
            sys.exit(1)
        if len(rows) <= 1:
            print("Error : 時間タグがありません")
            sys.exit(1)
        if re.match('^[0-9][0-9]:[0-9][0-9]:[0-9][0-9]$' ,rows[1]):
            time = datetime.strptime(rows[1], '%M:%S:%f')
            time_delta = timedelta(minutes=time.minute, seconds=time.second, microseconds=time.microsecond)
            comu_sec = int(time_delta.total_seconds()*100)

        # Start Time
        gyo_start_sec = comu_sec - before_sec
        if gyo_start_sec < 0:
            gyo_start_sec = 0
            start_minus_flg = 1
        time_delta = timedelta(milliseconds=gyo_start_sec*10)
        gyo_start_time = elapsed_time_str(time_delta)

        #########################
        # while read rows
        #########################
        for row in rows:
            if row_count <= 1:
                row_count +=1
                continue
            if row_count == (len(rows)-1):
                break
            if re.match('^[0-9][0-9]:[0-9][0-9]:[0-9][0-9]$' ,row):
                time = datetime.strptime(row, '%M:%S:%f')
                time_delta = timedelta(minutes=time.minute, seconds=time.second, microseconds=time.microsecond)
                interval_sec = int(time_delta.total_seconds()*100) - comu_sec
                comu_sec = int(time_delta.total_seconds()*100)
                gyo_end_sec = int(time_delta.total_seconds()*100) + after_sec
                gyo_end_time = elapsed_time_str(timedelta(milliseconds=(gyo_end_sec)*10))
                lyrics_a += "{\\K" + "{:02}".format(interval_sec) + "}"
                lyrics_a += words
            else:
                words = row
            row_count +=1

        

        ASStable.append({
            'startsec' : str(gyo_start_sec),
            'start' : str(gyo_start_time),
            'endsec' : str(gyo_end_sec),
            'end' : str(gyo_end_time),
            'before' : str(before_sec),
            'cont' : str(lyrics_a),
            'track' : track,
            'multi' : 0
        })
        if start_minus_flg == 1:
            time = datetime.strptime(rows[1], '%M:%S:%f')
            time_delta = timedelta(minutes=time.minute, seconds=time.second, microseconds=time.microsecond)
            comu_sec = int(time_delta.total_seconds()*100)
            ASStable[gyo]['before'] = str(comu_sec)
            start_minus_flg = 0



        # 1行前の End Time
        if gyo >= 1 :
            gyo1_end_sec = int(ASStable[gyo-1]['endsec'])
        else :
            gyo1_end_sec = 0

        if (gyo_start_sec - gyo1_end_sec) < 0 :
            multiline = 1
            if ASStable[gyo-1]['multi'] == 0 :
                track = 2
                ASStable[gyo-1]['multi'] = 1
            else :
                if ASStable[gyo-1]['track'] == 1 :
                    track = 2
                elif ASStable[gyo-1]['track'] == 2 :
                    track = 1
            if gyo >= 2:
                gyo2_end_sec = int(ASStable[gyo-2]['endsec'])
                if (gyo_start_sec - gyo2_end_sec) < 0 :
                    gyo2_end_sec = gyo_start_sec - 20
                    gyo2_end_time = elapsed_time_str(timedelta(milliseconds=(gyo2_end_sec)*10))
                    ASStable[gyo-2]['endsec'] = str(gyo2_end_sec)
                    ASStable[gyo-2]['end'] = str(gyo2_end_time)
        
        ASStable[gyo]['multi'] = multiline
        ASStable[gyo]['track'] = track

        # Position X, Y
        if ASStable[gyo]['track'] == 1 :
            ASStable[gyo]['pos_x'] = str((res_x - (fontsize + outline * 2) ) / 4 - marginside)
            ASStable[gyo]['pos_y'] = str(res_y - marginbottom)
        else :
            ASStable[gyo]['pos_x'] = str(marginside)
            ASStable[gyo]['pos_y'] = str(res_y - (fontsize + outline * 2) - lineheight)
        gyo += 1

    # Write lyrics body
    for gyo in range(len(ASStable)):
        lyrics += "Dialogue: 110," + ASStable[gyo]['start'] + "," + ASStable[gyo]['end'] +",Kanji1,,0000,0000,0000,Karaoke,{\\q2}{\\pos("+ ASStable[gyo]['pos_x'] +","+ ASStable[gyo]['pos_y'] +")}{\\K" + ASStable[gyo]['before'] +"}" + ASStable[gyo]['cont'] + "\r\n"

    return lyrics

###################################
## Main roop
###################################
def main():
    args = arg_parser()

    # Get file lists
    filename = args.infile
    settings = args.settings

    # Function
    result = filtering(filename, settings)

    # To save files, get output path
    outpath = os.path.splitext(os.path.basename(filename))[0] + '.ass'

    # Save files.
    f = open(outpath,'w')
    f.write(result)
    f.close()

if __name__ == '__main__':
    main()
