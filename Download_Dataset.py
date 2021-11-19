from __future__ import unicode_literals
import youtube_dl
import csv
import os


cwd = os.getcwd()
next_file = cwd + "\Buraya vttlerin olduğu klasör verilcek"
os.chdir(next_file)
temp = os.listdir()

def get_url_from_filename(filename):
    url = filename[:-len('.tr.vtt')]
    url = url[len(url)-11:]
    url = "https://www.youtube.com/watch?v=" + url
    return url

url_list = []
for vtt in temp:
    temp_url = get_url_from_filename(vtt)
    print(temp_url)
    url_list.append(temp_url)

print(len(url_list))

ydl_opts = {
    'format': '135+140',
    'outtmpl': '%(id)s.mp4',
    'noplaylist' : True
}


with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    print(url_list)
    ydl.download(url_list)

print("FINISHED....")