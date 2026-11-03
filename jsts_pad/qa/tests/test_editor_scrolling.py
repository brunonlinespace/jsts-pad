#!/usr/bin/env python3
"""Static regressions for JSTS Pad 0.1.2 EOF scrolling correction."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EDITOR_SOURCE = ROOT / "code_editor.py"


class EditorScrollingRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = EDITOR_SOURCE.read_text(encoding="utf-8")

    def test_global_center_on_scroll_is_disabled(self) -> None:
        self.assertIn("self.setCenterOnScroll(False)", self.source)
        self.assertNotIn("self.setCenterOnScroll(True)", self.source)

    def test_go_to_line_keeps_explicit_centering(self) -> None:
        self.assertIn("def go_to_line(self, line_number: int) -> bool:", self.source)
        self.assertIn("self.centerCursor()", self.source)


if __name__ == "__main__":
    unittest.main()
