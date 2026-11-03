#!/usr/bin/env python3
from __future__ import annotations
import os, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from jsts_pad.runtime_paths import RuntimePaths

class RuntimePathsTests(unittest.TestCase):
    def test_linux_paths_no_legacy_import(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'jsts_pad').mkdir(); home=root/'home'
            with patch.object(sys,'platform','linux'), patch.object(Path,'home',return_value=home), patch.dict(os.environ,{},clear=True):
                paths=RuntimePaths.detect(root/'main.py')
            self.assertEqual(paths.config_path, home/'.config/brunonlinespace/jsts-pad/jsts-pad.json')
            self.assertEqual(paths.legacy_config_paths, ())
            self.assertEqual(paths.icon_path, root/'jsts_pad/assets/icons/jsts-pad.png')
    def test_windows_paths(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'jsts_pad').mkdir(); appdata=root/'AppData/Roaming'
            with patch.object(sys,'platform','win32'), patch.dict(os.environ,{'APPDATA':str(appdata)},clear=True):
                paths=RuntimePaths.detect(root/'main.py')
            self.assertEqual(paths.config_path, appdata/'brunonlinespace/jsts-pad/jsts-pad.json')
    def test_source_has_no_appimage_themes(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'jsts_pad').mkdir()
            with patch.dict(os.environ,{},clear=True): paths=RuntimePaths.detect(root/'main.py')
            self.assertFalse(paths.running_as_appimage); self.assertEqual(paths.appimage_theme_paths,{})
    def test_appimage_theme_paths_need_both_files(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'jsts_pad').mkdir(); appdir=root/'AppDir'; styles=appdir/'usr/share/jsts-pad/styles'; styles.mkdir(parents=True)
            (styles/'breeze-dark.qss').write_text('x')
            with patch.dict(os.environ,{'APPDIR':str(appdir)},clear=True):
                self.assertEqual(RuntimePaths.detect(root/'main.py').appimage_theme_paths,{})
                (styles/'breeze-light.qss').write_text('x')
                self.assertEqual(set(RuntimePaths.detect(root/'main.py').appimage_theme_paths),{'dark','light'})

if __name__ == "__main__": unittest.main()
