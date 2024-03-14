# -*- coding: utf-8 -*-
import os
import sys
import argparse
import pandas as pd
import re
from datetime import datetime, timedelta

#####################################################################
## Usage: python rhythmicalyrics2ass.py -i lyrics.txt -s settings.ini
#####################################################################

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

# timedelta to "HH:MM:SS.ff"
def elapsed_time_str(time_delta):
    mseconds = time_delta.total_seconds()
    h = int(mseconds // 3600)
    m = int((mseconds - h * 3600) // 60)
    s = int(mseconds - h * 3600 - m * 60)
    mi = int((mseconds - h * 3600 - m * 60 - s) * 100)
    return "{:02}:{:02}:{:02}.{:02}".format(h, m, s, mi)

def filtering(filename, settings):
    ##########################
    # Variables initialization
    ##########################
    settings_ini = settings # ASS setting filename
    lyrics = "" # Header and body of lyrics
    f = open(filename)
    lines = f.readlines()
    f.close()

    ##########################
    # Read setting file
    ##########################
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

    ##########################
    # Write lyrics header
    ##########################
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

    ##########################
    # Variables initialization
    ##########################
    res_x = int(res_x)
    res_y = int(res_y)
    fontsize = int(fontsize)
    outline = int(outline)

    start_minus_flg = 0
    row_start_sec = 0
    row_start_time = 0
    row_end_sec = 0
    row_end_time = 0
    row = 0
    track = 1 # Multi line flag
    ASStable = []
    
    lyrics += "[Events]\r\n"
    lyrics += "Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text\r\n"

    ##########################
    # While read lines
    ##########################
    for line in lines:
        ##########################
        # Variables Initialization
        ##########################
        lyrics_a="" # lyrics of line
        words=""
        track = 1
        multiline = 0
        column_count = 0
        comu_sec = 0 # elapsed time
        columns = re.split('[\[\]]', line)

        ################################
        # Karaoke text file error check
        ################################
        if re.match('(^\r\n$|^\n$)',line): # Only new line
            continue
        elif not re.match('(^\r\n$|^\n$|^$)',columns[len(columns)-1]):
            print(columns, columns[len(columns)-1])
            print("Error : {}行目に終了タグがありません".format(row+1))
            sys.exit(1)
        elif not re.match('^$',columns[0]):
            print(columns, columns[len(columns)-1])
            print("Error : {}行目に開始タグがありません".format(row+1))
            sys.exit(1)
        if len(columns) <= 1:
            print("Error : 時間タグがありません")
            sys.exit(1)
        if re.match('^[0-9][0-9]:[0-9][0-9]:[0-9][0-9]$' ,columns[1]):
            time = datetime.strptime(columns[1], '%M:%S:%f')
            time_delta = timedelta(minutes=time.minute, seconds=time.second, microseconds=time.microsecond)
            comu_sec = int(time_delta.total_seconds()*100)

        row_start_sec = comu_sec - before_sec # Start time
        if row_start_sec < 0:
            row_start_sec = 0
            start_minus_flg = 1
        time_delta = timedelta(milliseconds=row_start_sec*10)
        row_start_time = elapsed_time_str(time_delta)

        #########################
        # While read columns
        #########################
        for column in columns:
            if column_count <= 1:
                column_count +=1
                continue
            if column_count == (len(columns)-1):
                break
            if re.match('^[0-9][0-9]:[0-9][0-9]:[0-9][0-9]$' ,column):
                time = datetime.strptime(column, '%M:%S:%f')
                time_delta = timedelta(minutes=time.minute, seconds=time.second, microseconds=time.microsecond)
                interval_sec = int(time_delta.total_seconds()*100) - comu_sec
                comu_sec = int(time_delta.total_seconds()*100)
                row_end_sec = int(time_delta.total_seconds()*100) + after_sec
                row_end_time = elapsed_time_str(timedelta(milliseconds=(row_end_sec)*10))
                lyrics_a += "{\\K" + "{:02}".format(interval_sec) + "}"
                lyrics_a += words
            else:
                words = column
            column_count +=1

        ASStable.append({
            'startsec' : str(row_start_sec),
            'start' : str(row_start_time),
            'endsec' : str(row_end_sec),
            'end' : str(row_end_time),
            'before' : str(before_sec),
            'cont' : str(lyrics_a),
            'track' : track,
            'multi' : 0
        })
        if start_minus_flg == 1:
            time = datetime.strptime(columns[1], '%M:%S:%f')
            time_delta = timedelta(minutes=time.minute, seconds=time.second, microseconds=time.microsecond)
            comu_sec = int(time_delta.total_seconds()*100)
            ASStable[row]['before'] = str(comu_sec)
            start_minus_flg = 0

        # End Time one lines earlier
        if row >= 1 :
            row1_end_sec = int(ASStable[row-1]['endsec'])
        else :
            row1_end_sec = 0

        if (row_start_sec - row1_end_sec) < 0 :
            multiline = 1
            if ASStable[row-1]['multi'] == 0 :
                track = 2
                ASStable[row-1]['multi'] = 1
            else :
                if ASStable[row-1]['track'] == 1 :
                    track = 2
                elif ASStable[row-1]['track'] == 2 :
                    track = 1
            # End Time two lines earlier
            if row >= 2:
                row2_end_sec = int(ASStable[row-2]['endsec'])
                # If the start time is greater than the end time of the previous phrase,
                # modify the end time of the previous phrase
                if (row_start_sec - row2_end_sec) < 0 :
                    row2_end_sec = row_start_sec - 15
                    row2_end_time = elapsed_time_str(timedelta(milliseconds=(row2_end_sec)*10))
                    ASStable[row-2]['endsec'] = str(row2_end_sec)
                    ASStable[row-2]['end'] = str(row2_end_time)
        
        ASStable[row]['multi'] = multiline
        ASStable[row]['track'] = track

        # Position X, Y
        if ASStable[row]['track'] == 1 :
            ASStable[row]['pos_x'] = str((res_x - (fontsize + outline * 2) ) / 4 - marginside)
            ASStable[row]['pos_y'] = str(res_y - marginbottom)
        else :
            ASStable[row]['pos_x'] = str(marginside)
            ASStable[row]['pos_y'] = str(res_y - (fontsize + outline * 2) - lineheight)
        row += 1

    # Write lyrics body
    for row in range(len(ASStable)):
        lyrics += "Dialogue: 110," + ASStable[row]['start'] + "," + ASStable[row]['end'] +",Kanji1,,0000,0000,0000,Karaoke,{\\q2}{\\pos("+ ASStable[row]['pos_x'] +","+ ASStable[row]['pos_y'] +")}{\\K" + ASStable[row]['before'] +"}" + ASStable[row]['cont'] + "\r\n"

    return lyrics

###################################
## Main roop
###################################
def main():
    #DRUG_DROP = True
    DRUG_DROP = False
    if DRUG_DROP :
        paths = sys.argv[1:]
        for path in paths:
            if '-i' == path:
                continue
            elif '-s' == path:
                continue
            else:
                filename = path
            settings = "settings.ini"
    else:
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
