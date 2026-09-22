import importlib.util
import sys
import unittest
from pathlib import Path
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


if __name__ == "__main__":
    unittest.main()
