from yt_dlp import YoutubeDL
import argparse

###################################
## Argument Parser
###################################
def arg_parser():
    parser = argparse.ArgumentParser(description='Tools')
    parser.add_argument('-u', '--url',  dest='url',  help='input file URL', required=True)
    parser.add_argument('-d', '--download',  dest='download',  help='download flag', required=False, default=True)
    args = parser.parse_args()
    return args



args = arg_parser()

option = {
    #'js-runtimes' : r"deno:C:\Users\yagi.masamichi\.deno\bin\deno.exe",
    'format' : 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
    'remote_components' : {'ejs:npm':'npm'}
}

def print_metadata(meta):
    print('upload date : %s' %(meta['upload_date']))
    print('ext : %s' %(meta['ext']))
    print('id : %s' %(meta['id']))
    print('format : %s' %(meta['format']))
    print('title : %s' %(meta['title']))

with YoutubeDL(option) as ydl:
    if False == args.download:
        meta = ydl.extract_info(args.url, download=False)
        print_metadata(meta)
    else:
        res = ydl.extract_info(args.url)
