# Youtube-to-DivX

Takes a file with youtube urls and downloads them in mp4 and then coverts them in divx using ffmpeg.

## Installation

### Step 1

Download and install any ```3.X``` python versions.

### Step 2

Run the following command in the command prompt.

```bash
pip install youtube-dl tqdm
```

### Step 3

Download and extract [ffmpeg.exe](https://ffmpeg.org/) in the same directory as main.py

## Usage

If you know your computer is old, change the **```max_..._thread_count```** variables to **```1```** or **```2```**.

Add your links in **```download.txt```** one per line.

Run the script.

The script will then download each video in **```mp4```** format in the **```download```** directory.

After the download is complete, the script will then convert each one of them to **```divx```** with **```mp3```** audio encoding, and put all the converted files in the **```converted```** directory. This will also delete the **```mp4```** file from the **```download```** directory.

## Author Andrei Maga
