import argparse
import os
import shutil
from pathlib import Path


def default_output_dir() -> Path:
    return Path.home() / "Desktop" / "High Quality"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Download YouTube Music or YouTube audio as WAV files."
    )
    parser.add_argument(
        "url",
        nargs="?",
        help="Track URL to download. Omit to use interactive mode.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=default_output_dir(),
        help="Folder where WAV files will be saved.",
    )
    parser.add_argument(
        "--playlist",
        action="store_true",
        help="Allow playlist downloads. By default, only a single track is downloaded.",
    )
    parser.add_argument(
        "--ffmpeg-location",
        help="Optional path to ffmpeg or the folder that contains it.",
    )
    return parser


def resolve_ffmpeg_location(explicit_location: str | None) -> str | None:
    if explicit_location:
        return explicit_location

    ffmpeg_in_path = shutil.which("ffmpeg")
    if ffmpeg_in_path:
        return str(Path(ffmpeg_in_path).parent)

    try:
        from imageio_ffmpeg import get_ffmpeg_exe
    except ImportError:
        return None

    return get_ffmpeg_exe()


def download_track(
    url: str,
    output_dir: Path,
    allow_playlist: bool,
    ffmpeg_location: str | None,
) -> bool:
    try:
        from yt_dlp import YoutubeDL
        from yt_dlp.utils import DownloadError
    except ImportError:
        print("yt-dlp is not installed. Run: pip install -r requirements.txt")
        return False

    output_dir.mkdir(parents=True, exist_ok=True)

    resolved_ffmpeg = resolve_ffmpeg_location(ffmpeg_location or os.getenv("FFMPEG_LOCATION"))

    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": not allow_playlist,
        "outtmpl": str(output_dir / "%(artist)s - %(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }
        ],
    }
    if resolved_ffmpeg:
        ydl_opts["ffmpeg_location"] = resolved_ffmpeg

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except DownloadError as exc:
        print(f"Download failed: {exc}")
        return False

    print(f"Saved audio to: {output_dir}")
    return True


def prompt_for_url() -> str:
    return input("Paste a YouTube Music or YouTube link (or press Enter to quit): ").strip()


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.url:
        return 0 if download_track(args.url, args.output_dir, args.playlist, args.ffmpeg_location) else 1

    print(f"WAV files will be saved in: {args.output_dir}")
    while True:
        url = prompt_for_url()
        if not url:
            print("Goodbye.")
            return 0

        download_track(url, args.output_dir, args.playlist, args.ffmpeg_location)

        again = input("Download another track? [y/N]: ").strip().lower()
        if again not in {"y", "yes"}:
            print("Goodbye.")
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
