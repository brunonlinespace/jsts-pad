#!/usr/bin/env python3
from __future__ import annotations
import unittest
from pathlib import Path
from jsts_pad.document_profiles import (
    DOCUMENT_TYPE_ORDER, SUPPORTED_SOURCE_SUFFIXES, document_type_for_path,
    document_type_for_suffix, extension_matches_type, profile_for_key,
)

class DocumentProfileTests(unittest.TestCase):
    def test_order(self):
        self.assertEqual(DOCUMENT_TYPE_ORDER, ("javascript", "typescript", "jsx", "tsx"))
    def test_supported_suffixes(self):
        self.assertEqual(SUPPORTED_SOURCE_SUFFIXES, frozenset({".js", ".mjs", ".cjs", ".ts", ".mts", ".cts", ".jsx", ".tsx"}))
    def test_suffix_detection(self):
        expected={".js":"javascript",".mjs":"javascript",".cjs":"javascript",".ts":"typescript",".mts":"typescript",".cts":"typescript",".jsx":"jsx",".tsx":"tsx"}
        for suffix,key in expected.items():
            with self.subTest(suffix=suffix): self.assertEqual(document_type_for_suffix(suffix.upper()), key)
    def test_path_detection(self):
        self.assertEqual(document_type_for_path(Path("Component.tsx")), "tsx")
        self.assertIsNone(document_type_for_path("settings.json"))
    def test_extension_matching(self):
        self.assertTrue(extension_matches_type("module.mjs", "javascript"))
        self.assertTrue(extension_matches_type("component.cts", "typescript"))
        self.assertFalse(extension_matches_type("component.jsx", "tsx"))
    def test_profiles_have_distinct_default_extensions(self):
        self.assertEqual([profile_for_key(k).default_extension for k in DOCUMENT_TYPE_ORDER], [".js", ".ts", ".jsx", ".tsx"])

if __name__ == "__main__": unittest.main()
