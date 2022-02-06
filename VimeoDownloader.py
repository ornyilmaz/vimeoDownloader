# Author: Orhan YILMAZ
# Description: Vimeo Video Downloader
# Date: 07.02.2022

import requests, json
import base64

video_JSON_URL = "https://<blabla url address>/master.json?query_string_ranges=1&base64_init=1" # master.json URL

video_JSON = requests.get(video_JSON_URL).json()
url = video_JSON_URL[0:(len(video_JSON_URL) - len(video_JSON_URL.split('/')[len(video_JSON_URL.split('/'))-2]) - len(video_JSON_URL.split('/')[-1])-7)] + video_JSON["base_url"][6:-1]
#url = video_JSON_URL + video_JSON["base_url"]      # Çalışıyor fakat yavaş iniyor. (its work but slow)

cookies = dict(MoodleSession='<blablablaCookie>') # cookie her defasında browser içindeki değerle güncellenmeli (Cookie updated from web browser pages) for ex: MoodleSession=<blablablaCookie>

init_segment = video_JSON["video"][-1]["init_segment"] # init_segment'i al ( get init_segment)

decoded = base64.b64decode(init_segment)    #base64 decode et.

output_file = open('video.mp4', 'wb') #video dosyası binary yazma şeklinde aç (create a binary video file)
output_file.write(decoded) #init_segment yazıldı

print("Video init yazıldı.")

r = requests.get( url + "/" + video_JSON["video"][-1]["index_segment"], allow_redirects=True, cookies=cookies) #index_segment'i al
output_file.write(r.content) #index_segment yazıldı

print("Video index yazıldı")

for i,raw in enumerate(video_JSON["video"][-1]["segments"]):
    r = requests.get( url + "/" + raw["url"], allow_redirects=True, cookies=cookies) #segmentleri sırayla indir ve yaz
    output_file.write(r.content)
    print("Video " +str(i)+".part yazıldı.")

output_file.close()
print("Video indirme işlemi tamamlandı.")

