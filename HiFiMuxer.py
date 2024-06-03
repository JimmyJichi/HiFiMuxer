import pylrc
from pymediainfo import MediaInfo
from yt_dlp import YoutubeDL
import requests
import os
import time
import json
import ffmpeg

USERAGENT = "HiFiMuxer 1.0 https://github.com/JimmyJichi/HiFiMuxer"

while True:
    song = input("Enter song filename: ")
    if os.path.isfile(song):
        break
    else:
        print("File not found")

print("Parsing file...")
media_info = MediaInfo.parse(song)
time.sleep(1)

print("Choose an option:")
print("1. Get lyrics from LRCLIB")
print("2. Use local lyrics file")
print("3. Do not embed lyrics")
while True:
    choice = input("Enter choice: ")
    if choice in ["1", "2", "3"]:
        break
    else:
        print("Invalid choice")

embedLyrics = True

if choice == "1":
    trackName = media_info.tracks[0].track_name
    trackName = trackName.replace("[Explicit]", "")
    album = media_info.tracks[0].album
    album = album.replace("[Explicit]", "")
    artist = media_info.tracks[0].performer
    duration = media_info.tracks[0].duration
    duration = round(duration / 1000)
    print(f"Track Name: {trackName}" + "\n" + f"Album: {album}" + "\n" + f"Artist: {artist}" + "\n" + f"Duration: {duration}")

    print("Getting lyrics...")
    r = requests.get(f"https://lrclib.net/api/get?artist_name={artist}&track_name={trackName}&album_name={album}&duration={duration}", headers={"User-Agent": USERAGENT})
    if r.status_code == 404:
        print("Lyrics not found. Exiting...")
        exit()
    response = json.loads(r.text)
    if response['syncedLyrics'] is None:
        print("Synced lyrics not available. Exiting...")
        exit()

    print("Parsing lyrics...")
    lyrics = response['syncedLyrics']
    srt = open("lyrics.srt", "w")
    srt.write(pylrc.parse(lyrics).toSRT())
    srt.close()

elif choice == "2":
    while True:
        lyrics = input("Enter lyrics filename [.lrc .srt]: ")
        if os.path.isfile(lyrics):
            if lyrics.endswith(".lrc") or lyrics.endswith(".srt"):
                break
            else:
                print("Invalid file format")
        else:
            print("File not found")

    srt = open("lyrics.srt", "w")

    if lyrics.endswith(".lrc"):
        print("Parsing LRC file...")
        srt.write(pylrc.parse(open(lyrics).read()).toSRT())
    else:
        srt.write(open(lyrics).read())
    srt.close()

else:
    embedLyrics = False

youtubeLink = input("Enter YouTube link: ")
try:
    with YoutubeDL({'format': 'bestvideo[ext=mp4]', 'outtmpl': 'video.mp4'}) as ydl:
        ydl.download([youtubeLink])
except Exception as e:
    print(e)
    print("Unable to download video. Exiting...")
    exit()
else:
    print("Download successful.")

print("Using ffmpeg to mux video and audio...")
output = song.split(".")[0] + "_muxed.mp4"
try:
    if embedLyrics:
        ffmpeg.output(ffmpeg.input("video.mp4")['v'], ffmpeg.input(song)['a'], ffmpeg.input("lyrics.srt")['s'], output, vcodec="copy", acodec="copy", scodec="mov_text").run()
    else:
        ffmpeg.output(ffmpeg.input("video.mp4")['v'], ffmpeg.input(song)['a'], output, vcodec="copy", acodec="copy").run()
except ffmpeg.Error as e:
    print(e.stderr)
    print("Unable to mux. Exiting...")
    exit()
else:
    print("Mux successful. Deleting temporary files...")
    if embedLyrics:
        os.remove("lyrics.srt")
    os.remove("video.mp4")
    print("Done")