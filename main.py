import os
import sys
import tqdm
from threads import FFMPEGThread, DownloadThread


config = {}


def run_threads(input, thread, thread_count):
    threads = []
    current_index = 0
    tqd = tqdm.tqdm(total=len(input))
    while len(input) > current_index:
        if len(threads) < thread_count:
            T = thread(input[current_index], threads, tqd, config)
            current_index += 1
            T.start()
            threads.append(T)

    while any([T.isAlive() for T in threads]):
        continue
    tqd.close()


def convert():
    files = os.listdir(config["locations"]["download"])
    run_threads(files, FFMPEGThread,
                config["threads"]["ffmpeg"])


def download_from_file():
    os.chdir(config["locations"]["download"])
    urls = []
    with open("..\\download.txt", "r") as url_file:
        urls = url_file.readlines()
    urls = [url.strip("\n") for url in urls]
    run_threads(urls, DownloadThread,
                config["threads"]["download"])


def load_config():
    global config
    location = os.getcwd()
    from json import load
    with open("config.json") as config_file:
        config = load(config_file)
    config["locations"] = {}
    config["locations"]["download"] = location + "\\download\\"
    config["locations"]["convert"] = location + "\\converted\\"
    config["locations"]["ffmpeg"] = location + "\\ffmpeg.exe"
    config["locations"]["youtube_dl"] = '\\'.join(
        sys.executable.split("\\")[:-1]) + "\\Scripts\\youtube-dl.exe"

    if not os.path.isdir(config["locations"]["download"]):
        os.mkdir(config["locations"]["download"])
    if not os.path.isdir(config["locations"]["convert"]):
        os.mkdir(config["locations"]["convert"])


def download_and_unzip_ffmpeg():
    import urllib.request
    from zipfile import ZipFile
    from shutil import copyfileobj
    req = urllib.request.Request(
        config["ffmpeg"]["url"],
        headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0"
        }
    )
    response = urllib.request.urlopen(req)
    with open ("ffmpeg.zip", "wb") as f:
        copyfileobj(response, f)
    with ZipFile("ffmpeg.zip") as zip_file:
        source = zip_file.open("ffmpeg-4.2.2-win64-static/bin/ffmpeg.exe")
        target = open("ffmpeg.exe", "wb")
        copyfileobj(source, target)
        source.close()
        target.close()

    response.close()
    os.remove("ffmpeg.zip")


def ffmpeg():
    if os.path.exists(config["locations"]["ffmpeg"]):
        return

    answer = input(
        "You need to have ffmpeg.exe in the same folder as this script.\nDo you want me to download it for you? [Y]/n:")
    if(answer.lower() == "n"):
        print("The url you're looking for is https://www.ffmpeg.org/download.html")

    print("Warning! This script will download the ffmepg {} , if you have an older version of Windows please download it manually.".format(
        config["ffmpeg"]["version"]))
    answer = input("Do you wish to continue? [Y]/n:")
    if(answer.lower() == "n"):
        print("The url you're looking for is https://www.ffmpeg.org/download.html")
        sys.exit(1)
    download_and_unzip_ffmpeg()


def youtube_dl():
    if os.path.exists(config["locations"]["youtube_dl"]):
        return

    answer = input(
        "You don't have youtube-dl installed. \nDo you want me to install it for you? [Y]/n:")
    if(answer.lower() == "n"):
        print("Install it by running \"pip install youtube-dl\"")
        sys.exit(1)

    print("Installing youtube-dl")
    to_run = "pip install youtube-dl"
    import subprocess
    subprocess.call(to_run)


if __name__ == "__main__":
    load_config()
    ffmpeg()
    youtube_dl()
    print("Downloading")
    download_from_file()
    print("Converting")
    convert()
