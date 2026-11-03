#!/usr/bin/env python3
from __future__ import annotations
import os, tempfile, unittest
from pathlib import Path
from jsts_pad.file_io import (
    FileTooLargeError, UnsupportedFileError, absolute_user_path,
    current_file_state, path_identity_matches, read_regular_file,
)

class FileIOTests(unittest.TestCase):
    def test_absolute_path_does_not_resolve_final_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); target=root/'target.js'; target.write_text('x')
            link=root/'link.js'
            try: link.symlink_to(target)
            except (OSError, NotImplementedError): self.skipTest('symlink unavailable')
            self.assertEqual(absolute_user_path(link), link.absolute())
    def test_read_regular_file_and_digest(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.ts'; p.write_bytes(b'const x: number = 1;')
            data,snap=read_regular_file(p,1024)
            self.assertEqual(data,b'const x: number = 1;'); self.assertEqual(len(snap.digest),64)
    def test_size_limit(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.js'; p.write_bytes(b'12345')
            with self.assertRaises(FileTooLargeError): read_regular_file(p,4)
    def test_directory_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(UnsupportedFileError): read_regular_file(Path(d),1024)
    def test_file_identity(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.jsx'; p.write_text('const x = <div />;')
            state=current_file_state(p)
            self.assertTrue(path_identity_matches(p,state))
            old=p.with_name('old.jsx'); p.rename(old); p.write_text('replacement')
            self.assertFalse(path_identity_matches(p,state))

if __name__ == "__main__": unittest.main()
