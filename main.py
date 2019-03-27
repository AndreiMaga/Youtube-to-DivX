import os
import sys
location = os.getcwd()
down_location = location + "\\download\\"
if not os.path.isdir(down_location):
    os.mkdir(down_location)
conv_location = location + "\\converted\\"
if not os.path.isdir(conv_location):
    os.mkdir(conv_location)
ffmpeg_location = location + "\\ffmpeg.exe"

if not os.path.exists(ffmpeg_location):
    print("FFMPEG.exe needs to be in the same folder as this script.")
    sys.exit(1)

def download(url):
    from pytube import YouTube
    yt = YouTube(url).streams.first().download(output_path=down_location)


def convert():
    ffmpegargs = " -f avi -r 29.97 -vcodec libxvid -vtag xvid -vf scale=704:-1 -aspect 16:9 -maxrate 8000k -b:v 6000k -qmin 3 -qmax 5 -bufsize 4096 -mbd 2 -bf 2 -trellis 1 -flags +aic -cmp 2 -subcmp 2 -g 300 -acodec ac3 -ar 48000 -aq 2"
    for i in os.listdir(down_location):
        inp = down_location + i
        out = conv_location+(i.split(".")[0]+".divx")
        to_run = "{0} -i \"{1}\"".format(ffmpeg_location, inp)+ ffmpegargs + " \"{0}\"".format(out)
        os.system(to_run)

def download_from_file():
    lines = []
    with open("download.txt") as f:
        lines = f.readlines()

    for line in lines:
        download(line)


download_from_file()
convert()
