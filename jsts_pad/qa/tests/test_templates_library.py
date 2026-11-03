#!/usr/bin/env python3
from __future__ import annotations
import unittest
from jsts_pad.document_profiles import DOCUMENT_TYPE_ORDER
from jsts_pad.templates import (
    BUILTIN_TEMPLATES, CURSOR_MARKER, MAX_CUSTOM_TEMPLATES,
    default_template_id, normalise_custom_templates, serialise_custom_templates,
)
from jsts_pad.library_catalog import (
    COMMON_JS, JSX_EXTRA, TSX_EXTRA, TS_EXTRA,
    MAX_CUSTOM_SNIPPETS, LibrarySpec, builtins_for_language,
    normalise_custom_snippets, serialise_custom_snippets,
)

class TemplateLibraryTests(unittest.TestCase):
    def test_each_language_has_blank_factory_default(self):
        by_id={s.template_id:s for s in BUILTIN_TEMPLATES}
        for language in DOCUMENT_TYPE_ORDER:
            spec=by_id[default_template_id(language)]
            self.assertEqual(spec.language, language)
            self.assertTrue(spec.builtin)
            self.assertEqual(spec.content, "")
    def test_richer_factory_templates_exist(self):
        ids={s.template_id for s in BUILTIN_TEMPLATES}
        for wanted in {"javascript:module","javascript:browser","typescript:module","jsx:component","tsx:component"}:
            self.assertIn(wanted, ids)
    def test_factory_cursor_marker_is_at_most_once(self):
        self.assertTrue(all(s.content.count(CURSOR_MARKER) <= 1 for s in BUILTIN_TEMPLATES))
    def test_custom_template_normalisation(self):
        raw=[{"id":"user:1","language":"tsx","name":" My TSX ","content":"<div>[[cursor]]</div>"}, {"id":"bad","language":"tsx","name":"x","content":"x"}]
        result=normalise_custom_templates(raw)
        self.assertEqual(len(result),1); self.assertEqual(result[0].name,"My TSX")
        self.assertEqual(serialise_custom_templates(result)[0]["language"],"tsx")
    def test_custom_template_limit(self):
        raw=[{"id":f"user:{i}","language":"javascript","name":str(i),"content":""} for i in range(MAX_CUSTOM_TEMPLATES+20)]
        self.assertEqual(len(normalise_custom_templates(raw)), MAX_CUSTOM_TEMPLATES)
    def test_library_exists_for_all_languages(self):
        for language in DOCUMENT_TYPE_ORDER:
            with self.subTest(language=language): self.assertGreater(len(builtins_for_language(language)), 8)
    def test_r5_library_is_rich_and_keeps_original_builtins(self):
        minimums={"javascript":90,"typescript":140,"jsx":130,"tsx":200}
        for language, minimum in minimums.items():
            specs=builtins_for_language(language)
            self.assertGreaterEqual(len(specs), minimum)
            self.assertEqual(len({s.key for s in specs}), len(specs))
        js_keys={s.key for s in builtins_for_language("javascript")}
        self.assertTrue({s.key for s in COMMON_JS}.issubset(js_keys))
        ts_labels={s.label for s in builtins_for_language("typescript")}
        self.assertTrue({s.label for s in TS_EXTRA}.issubset(ts_labels))
        jsx_labels={s.label for s in builtins_for_language("jsx")}
        self.assertTrue({s.label for s in JSX_EXTRA}.issubset(jsx_labels))
        tsx_labels={s.label for s in builtins_for_language("tsx")}
        self.assertTrue({s.label for s in TSX_EXTRA}.issubset(tsx_labels))
        for expected in ("console.log", "Promise.all()", "Object.entries()", "localStorage set"):
            self.assertIn(expected, {s.label for s in builtins_for_language("javascript")})
        for expected in ("type guard", "Partial", "satisfies", "type-only import"):
            self.assertIn(expected, ts_labels)
        for expected in ("useState", "controlled input", "arrow component"):
            self.assertIn(expected, jsx_labels)
        for expected in ("typed useState", "typed mouse event", "forwardRef component"):
            self.assertIn(expected, tsx_labels)
    def test_typescript_has_type_material(self):
        labels={s.label for s in builtins_for_language("typescript")}
        self.assertIn("interface", labels); self.assertIn("type alias", labels)
    def test_jsx_has_markup_material(self):
        labels={s.label for s in builtins_for_language("jsx")}
        self.assertIn("element", labels); self.assertIn("fragment", labels)
    def test_tsx_combines_types_and_markup(self):
        labels={s.label for s in builtins_for_language("tsx")}
        self.assertIn("typed Props interface", labels); self.assertIn("element", labels); self.assertIn("type alias", labels)
    def test_custom_snippet_roundtrip(self):
        raw=[{"id":"user:s","language":"typescript","name":"Typed value","category":"Types","content":"const x: string = [[cursor]];","description":"demo"}]
        result=normalise_custom_snippets(raw)
        self.assertEqual(len(result),1); self.assertFalse(result[0].builtin)
        serial=serialise_custom_snippets(result)[0]
        self.assertEqual(serial["content"], "const x: string = [[cursor]];")
    def test_custom_snippet_limit(self):
        raw=[{"id":f"user:{i}","language":"javascript","name":str(i),"category":"Custom","content":"x","description":""} for i in range(MAX_CUSTOM_SNIPPETS+5)]
        self.assertEqual(len(normalise_custom_snippets(raw)), MAX_CUSTOM_SNIPPETS)
    def test_json_is_not_a_language(self):
        self.assertEqual(builtins_for_language("json"), ())

if __name__ == "__main__": unittest.main()
