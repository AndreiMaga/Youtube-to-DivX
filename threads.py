import threading
import subprocess
import os

class FFMPEGThread(threading.Thread):
    def __init__(self, file, thread_list, tqd, config):
        threading.Thread.__init__(self)
        self.file = file
        self.thread_list = thread_list
        self.tqd = tqd
        self.config = config

    def run(self):
        ffmpegargs = " -y -f avi -r 29.97 -vcodec libxvid -vtag xvid -vf scale=704:-1 -aspect 16:9 -maxrate 8000k -b:v 6000k -qmin 3 -qmax 5 -bufsize 4096 -mbd 2 -bf 2 -trellis 1 -flags +aic -cmp 2 -subcmp 2 -g 300 -acodec ac3 -ar 48000 -aq 2"
        inp = self.config["locations"]["download"] + self.file
        out = self.config["locations"]["convert"] + self.file.split(".")[0]+".divx"
        if not (os.path.exists(out) and os.path.getsize(out) > 0):     
            to_run = "{0} -i \"{1}\"".format(self.config["locations"]["ffmpeg"],
                                            inp) + ffmpegargs + " \"{0}\"".format(out)
            subprocess.call(to_run, stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
        os.remove(self.file)
        self.tqd.update(1)
        self.thread_list.remove(self)


class DownloadThread(threading.Thread):
    def __init__(self, url, thread_list, tqd, config):
        threading.Thread.__init__(self)
        self.url = url
        self.thread_list = thread_list
        self.tqd = tqd
        self.config = config

    def run(self):
        to_run = "{} --no-playlist {}".format(self.config["locations"]["youtube_dl"], self.url)
        subprocess.call(to_run, stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        self.tqd.update(1)
        self.thread_list.remove(self)
