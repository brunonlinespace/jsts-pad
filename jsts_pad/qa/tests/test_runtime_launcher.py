#!/usr/bin/env python3
from __future__ import annotations
import os, sys, tempfile, types, unittest
from pathlib import Path
from unittest import mock
try:
    import PyQt6.QtCore  # noqa
except ModuleNotFoundError:
    qtcore=types.ModuleType('PyQt6.QtCore')
    class Signal:
        def emit(self,*a,**k): pass
    class QObject:
        def __init__(self,*a,**k): pass
    class QProcess: pass
    class QProcessEnvironment:
        @staticmethod
        def systemEnvironment(): return QProcessEnvironment()
        def remove(self,*a): pass
        def insert(self,*a): pass
    qtcore.QObject=QObject; qtcore.QProcess=QProcess; qtcore.QProcessEnvironment=QProcessEnvironment; qtcore.pyqtSignal=lambda *a,**k: Signal()
    package=types.ModuleType('PyQt6'); package.QtCore=qtcore
    sys.modules.setdefault('PyQt6',package); sys.modules.setdefault('PyQt6.QtCore',qtcore)
from jsts_pad.runtime_launcher import LaunchCommand, RuntimeLauncher
from jsts_pad.runtime_paths import RuntimePaths

class RuntimeLauncherTests(unittest.TestCase):
    def paths(self,root): return RuntimePaths(root,root/'jsts_pad',root/'jsts_pad/assets',root/'config',False,False)
    def test_http_only_url(self):
        with tempfile.TemporaryDirectory() as d:
            launcher=RuntimeLauncher(self.paths(Path(d)))
            with mock.patch.object(launcher,'start_detached') as detached:
                self.assertFalse(launcher.open_url('javascript:alert(1)')); self.assertFalse(launcher.open_url('file:///tmp/x'))
            detached.assert_not_called()
    def test_external_editor_override_is_argument_safe(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); p=root/'x.js'; p.write_text('x')
            launcher=RuntimeLauncher(self.paths(root))
            with mock.patch.dict(os.environ,{'JSTS_PAD_EDITOR':'editor --new-window'},clear=False), mock.patch.object(launcher,'_resolve_executable',return_value='/usr/bin/editor'), mock.patch.object(launcher,'start_detached',return_value=True) as detached:
                self.assertTrue(launcher.open_in_external_editor(p))
            command=detached.call_args.args[0]
            self.assertEqual(command, LaunchCommand('/usr/bin/editor',('--new-window',str(p)),p.parent))
    def test_no_script_execution_api(self):
        forbidden={'run','launch_script','run_script','python_command','shell_command','script_command','terminal_command','node_command','npm_command'}
        self.assertTrue(forbidden.isdisjoint(set(dir(RuntimeLauncher))))
    def test_appimage_sanitizer_includes_jsts_theme(self):
        src=(Path(__file__).resolve().parents[2]/'runtime_launcher.py').read_text()
        self.assertIn('"JSTS_PAD_APPIMAGE_THEME"',src); self.assertIn('APPIMAGE_ORIGINAL_PATH',src)

if __name__ == "__main__": unittest.main()
