import os
import sys
import threading
import subprocess
import tqdm

max_FFMPEG_thread_count = 4
max_download_thread_count = 4

location = os.getcwd()
down_location = location + "\\download\\"
if not os.path.isdir(down_location):
    os.mkdir(down_location)
conv_location = location + "\\converted\\"
if not os.path.isdir(conv_location):
    os.mkdir(conv_location)
ffmpeg_location = location + "\\ffmpeg.exe"

youtubedl_path = '\\'.join(sys.executable.split(
    "\\")[:-1]) + "\\Scripts\\youtube-dl.exe"


class FFMPEGThread(threading.Thread):
    def __init__(self, file, thread_list, tqd):
        threading.Thread.__init__(self)
        self.file = file
        self.thread_list = thread_list
        self.tqd = tqd

    def run(self):
        ffmpegargs = " -y -f avi -r 29.97 -vcodec libxvid -vtag xvid -vf scale=704:-1 -aspect 16:9 -maxrate 8000k -b:v 6000k -qmin 3 -qmax 5 -bufsize 4096 -mbd 2 -bf 2 -trellis 1 -flags +aic -cmp 2 -subcmp 2 -g 300 -acodec ac3 -ar 48000 -aq 2"
        inp = down_location + self.file
        out = conv_location + self.file.split(".")[0]+".divx"
        to_run = "{0} -i \"{1}\"".format(ffmpeg_location,
                                         inp) + ffmpegargs + " \"{0}\"".format(out)
        subprocess.call(to_run, stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        os.remove(self.file)
        self.tqd.update(1)
        self.thread_list.remove(self)


class DownloadThread(threading.Thread):
    def __init__(self, url, thread_list, tqd):
        threading.Thread.__init__(self)
        self.url = url
        self.thread_list = thread_list
        self.tqd = tqd

    def run(self):
        to_run = "{} --no-playlist {}".format(youtubedl_path, self.url)
        subprocess.call(to_run, stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        self.tqd.update(1)
        self.thread_list.remove(self)


def run_threads(input, thread, thread_count):
    threads = []
    current_index = 0
    tqd = tqdm.tqdm(total=len(input))
    while len(input) > current_index:
        if len(threads) < thread_count:
            T = thread(input[current_index], threads, tqd)
            current_index += 1
            T.start()
            threads.append(T)

    while any([T.isAlive() for T in threads]):
        continue
    tqd.close()


def convert():
    files = os.listdir(down_location)
    run_threads(files, FFMPEGThread, max_FFMPEG_thread_count)


def download_from_file():
    os.chdir(down_location)
    urls = []
    with open("..\\download.txt", "r") as url_file:
        urls = url_file.readlines()
    urls = [url.strip("\n") for url in urls]
    run_threads(urls, DownloadThread, max_download_thread_count)


if __name__ == "__main__":
    if not os.path.exists(ffmpeg_location):
        print("FFMPEG.exe needs to be in the same folder as this script.")
        sys.exit(1)

    if not os.path.exists(youtubedl_path):
        print("You need to run pip install youtube-dl")
        sys.exit(1)
    print("Downloading")
    download_from_file()
    print("Converting")
    convert()
