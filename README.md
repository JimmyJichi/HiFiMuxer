# HiFiMuxer

This Python script combines music videos on YouTube with local high fidelity audio files. Lyrics are automatically fetched from [LRCLIB](https://lrclib.net/) and embedded as subtitles.

## Dependencies

- ffmpeg
- mediainfo

## Usage

1. Clone the repository

```
git clone https://github.com/JimmyJichi/HiFiMuxer.git
```

2. Install Python packages

```
pip install -r requirements.txt
```

3. Move the audio file to the current directory. Make sure the audio codec is supported by the mp4 container (e.g. flac, m4a).

4. Run the script

```
python HiFiMuxer.py
```

You will be prompted to enter a YouTube link to download the video. Lyrics will be fetched from LRCLIB and embedded as subtitles.
