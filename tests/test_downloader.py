import importlib.util
import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch


MODULE_PATH = Path(__file__).resolve().parents[1] / "ytmusic-downloader.py"
SPEC = importlib.util.spec_from_file_location("ytmusic_downloader", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class DownloaderTest(unittest.TestCase):
    def test_default_output_dir_is_below_home_desktop(self):
        with patch.object(MODULE.Path, "home", return_value=Path("/example/home")):
            self.assertEqual(
                MODULE.default_output_dir(),
                Path("/example/home/Desktop/High Quality"),
            )

    def test_parser_defaults_to_single_item_mode(self):
        args = MODULE.build_parser().parse_args(["https://example.test/watch"])
        self.assertFalse(args.playlist)
        self.assertFalse(args.update_yt_dlp)

    def test_parser_accepts_explicit_output_and_playlist(self):
        args = MODULE.build_parser().parse_args(
            ["https://example.test/watch", "--playlist", "--output-dir", "downloads"]
        )
        self.assertTrue(args.playlist)
        self.assertEqual(args.output_dir, Path("downloads"))

    def test_explicit_ffmpeg_location_wins(self):
        self.assertEqual(
            MODULE.resolve_ffmpeg_location("/example/ffmpeg"),
            "/example/ffmpeg",
        )

    def test_download_passes_single_track_wav_settings_to_the_library(self):
        with TemporaryDirectory() as directory, patch("yt_dlp.YoutubeDL", autospec=True) as downloader, redirect_stdout(StringIO()):
            client = downloader.return_value
            client.__enter__.return_value = client
            self.assertTrue(MODULE.download_track(
                "https://example.test/audio", Path(directory), False, "/demo/ffmpeg"
            ))
            settings = downloader.call_args.args[0]
            self.assertTrue(settings["noplaylist"])
            self.assertEqual(settings["ffmpeg_location"], "/demo/ffmpeg")
            self.assertEqual(settings["postprocessors"][0]["preferredcodec"], "wav")
            client.download.assert_called_once_with(["https://example.test/audio"])

    def test_playlist_mode_requires_explicit_opt_in(self):
        with TemporaryDirectory() as directory, patch("yt_dlp.YoutubeDL", autospec=True) as downloader, redirect_stdout(StringIO()):
            self.assertTrue(MODULE.download_track(
                "https://example.test/playlist", Path(directory), True, "/demo/ffmpeg"
            ))
            self.assertFalse(downloader.call_args.args[0]["noplaylist"])

    def test_library_download_error_is_reported_as_failure(self):
        from yt_dlp.utils import DownloadError
        with TemporaryDirectory() as directory, patch("yt_dlp.YoutubeDL", autospec=True) as downloader, redirect_stdout(StringIO()) as console:
            client = downloader.return_value
            client.__enter__.return_value = client
            client.download.side_effect = DownloadError("Synthetic unavailable item")
            self.assertFalse(MODULE.download_track(
                "https://example.test/unavailable", Path(directory), False, "/demo/ffmpeg"
            ))
            self.assertIn("Download failed", console.getvalue())


if __name__ == "__main__":
    unittest.main()
