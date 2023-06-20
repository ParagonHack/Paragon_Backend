from pytube import YouTube

import os
import shutil
import math
import datetime

with open("./data/YT_links.txt") as f: 
    links =  [item.strip() for item in f.read().split('\n')]




video = YouTube(links[0], use_oauth=True, allow_oauth_cache=True)


obj = video.streams.filter(only_audio=True).first()


print(True)