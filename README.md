# YouTube Music WAV Downloader

Small downloader for saving YouTube Music or YouTube audio as WAV files.

There are two versions here:

- `ytmusic-downloader.bat` for quick use on Windows
- `ytmusic-downloader.py` if you want a Python version

## What it does

- grabs the best audio stream it can get
- converts it to WAV with `ffmpeg`
- saves into a `High Quality` folder on your Desktop unless you choose another folder

## Requirements

- `ffmpeg` in your PATH
- for the batch version: `yt-dlp.exe` next to the `.bat` file, or `yt-dlp` installed in PATH
- for the Python version:

```bash
pip install -r requirements.txt
```

The Python version will also try to use the bundled `imageio-ffmpeg` binary if `ffmpeg` is not already installed system-wide.

## Python

Interactive:

```bash
python ytmusic-downloader.py
```

Single link:

```bash
python ytmusic-downloader.py "https://music.youtube.com/watch?v=..."
```

Custom folder:

```bash
python ytmusic-downloader.py "https://music.youtube.com/watch?v=..." --output-dir "D:\\Music\\Downloads"
```

Explicit ffmpeg path:

```bash
python ytmusic-downloader.py "https://music.youtube.com/watch?v=..." --ffmpeg-location "C:\\path\\to\\ffmpeg"
```

## Batch

1. Put `yt-dlp.exe` next to `ytmusic-downloader.bat`, or install `yt-dlp`.
2. Run `ytmusic-downloader.bat`.
3. Paste the link.

By default the files go to `C:\Users\<USERNAME>\Desktop\High Quality`.

## Notes

- `yt-dlp.exe` is ignored by git. I keep it locally for convenience.
- File names depend on whatever metadata the source video exposes.
- If YouTube extraction changes upstream, updating `yt-dlp` usually fixes it.
