#!/usr/bin/env python3
from __future__ import annotations
import ast, re, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; PKG=ROOT/'jsts_pad'

class SourceContractTests(unittest.TestCase):
    def test_all_python_parses(self):
        for p in [ROOT/'main.py', *PKG.rglob('*.py')]:
            if '__pycache__' in p.parts: continue
            with self.subTest(path=p.name): ast.parse(p.read_text(encoding='utf-8'), filename=str(p))
    def test_editor_profiles_and_actions_present(self):
        src=(PKG/'code_editor.py').read_text()
        for token in ('javascript','typescript','jsx','tsx','delete_current_line','duplicate_current_line_or_selection','toggle_comment','_matching_bracket_selections'):
            self.assertIn(token,src)
    def test_app_has_start_document_and_default_workflow(self):
        src=(PKG/'app.py').read_text()
        for token in ('Start a Document','Default New Document…','New Type…','Use this type and template as my default','Document Type'):
            self.assertIn(token,src)
    def test_start_panel_uses_shared_workspace_stack(self):
        src=(PKG/'app.py').read_text()
        self.assertIn('QStackedWidget', src)
        self.assertIn('self.workspace_stack = QStackedWidget(self)', src)
        self.assertIn('self.workspace_stack.addWidget(self.start_panel)', src)
        self.assertIn('self.workspace_stack.addWidget(self.workspace_splitter)', src)
        layout=src[src.index('    def _apply_layout_mode'):src.index('    def set_library_sidebar_position')]
        self.assertIn('self.workspace_stack', layout)
        self.assertNotIn('self.main_layout.addWidget(self.workspace_splitter', layout)
        start=src[src.index('    def _show_start_panel'):src.index('    def _show_document_workspace')]
        self.assertIn('self.workspace_stack.setCurrentWidget(self.start_panel)', start)
        self.assertNotIn('self.search_container.hide()', start)
        self.assertNotIn('self.bottom_search.hide()', start)
        self.assertIn('self._set_find_bars_enabled(False)', start)
        document=src[src.index('    def _show_document_workspace'):src.index('    def _handle_startup_without_file')]
        self.assertIn('self._set_find_bars_enabled(True)', document)
        helper=src[src.index('    def _set_find_bars_enabled'):src.index('    def _show_start_panel')]
        self.assertIn('find_bar.setEnabled(bool(enabled))', helper)
    def test_edit_menu_is_disabled_without_document(self):
        src=(PKG/'app.py').read_text()
        state=src[src.index('    def _update_edit_action_state'):src.index('    # ------------------------------------------------------------------\n    # View behavior')]
        self.assertIn('has_document = self.document_active', state)
        self.assertIn('for action in self.edit_menu.actions()', state)
        self.assertIn('action.setEnabled(has_document)', state)
        self.assertIn('if not has_document:', state)
        self.assertIn('editing_enabled = not self.view_only', state)
        start=src[src.index('    def _show_start_panel'):src.index('    def _show_document_workspace')]
        document=src[src.index('    def _show_document_workspace'):src.index('    def _handle_startup_without_file')]
        self.assertIn('self._update_edit_action_state()', start)
        self.assertIn('self._update_edit_action_state()', document)

    def test_dark_editor_is_persistent_and_independent(self):
        src=(PKG/'app.py').read_text()
        for token in ('self.dark_editor = True', 'boolean_value("dark_editor", True)', '"dark_editor": self.dark_editor', '"Dark Editor"', 'def toggle_dark_editor'):
            self.assertIn(token, src)
        apply_theme=src[src.index('    def apply_appimage_theme'):src.index('    def toggle_appimage_dark_mode')]
        self.assertNotIn('set_color_scheme', apply_theme)
        apply_prefs=src[src.index('    def _apply_preferences'):src.index('    def toggle_view_only')]
        self.assertIn('self.editor.set_color_scheme("dark" if self.dark_editor else "light")', apply_prefs)
    def test_drag_drop_menu_labels(self):
        src=(PKG/'app.py').read_text()
        for token in ('"File Drag and Drop"', '"Opens on Active Window"', '"Opens on New Window"'):
            self.assertIn(token, src)
        self.assertNotIn('"Behaviour"', src)
        self.assertNotIn('"File Drag Drop"', src)
        self.assertNotIn('"Drag and drop opens on active window"', src)
        self.assertNotIn('"Drag and drop opens on new window"', src)
    def test_toolbar_order_contract(self):
        src=(PKG/'app.py').read_text()
        block=src[src.index('for label, menu in ('):src.index('self.primary_controls =',src.index('for label, menu in ('))]
        positions=[block.index(f'("{x}"') for x in ('File','Edit','View','Library','Help')]
        self.assertEqual(positions,sorted(positions))
        self.assertNotIn('document_type_button',src)
        self.assertIn('self.document_type_file_menu = self.file_menu.addMenu("Document Type")',src)
    def test_r5_toolbar_code_shortcuts(self):
        src=(PKG/'app.py').read_text()
        self.assertIn('self.comment_toolbar_button.setText("Comment")',src)
        self.assertIn('self.comment_toolbar_button.clicked.connect(self.comment_action.trigger)',src)
        self.assertIn('self.duplicate_toolbar_button.setText("Duplicate")',src)
        self.assertIn('self.duplicate_toolbar_button.clicked.connect(self.duplicate_action.trigger)',src)
        self.assertIn('self.comment_toolbar_button.setEnabled(self.comment_action.isEnabled())',src)
        self.assertIn('self.duplicate_toolbar_button.setEnabled(self.duplicate_action.isEnabled())',src)

    def test_r5_file_and_library_shortcuts(self):
        src=(PKG/'app.py').read_text()
        for token in (
            'QKeySequence("Ctrl+Shift+E")',
            'QKeySequence("F2")',
            'QKeySequence("Ctrl+Shift+D")',
            'QKeySequence("Ctrl+Shift+O")',
            'QKeySequence("Ctrl+L")',
        ):
            self.assertIn(token,src)
        self.assertNotIn('QKeySequence("Ctrl+Delete")',src)
        self.assertNotIn('QKeySequence("Alt+Enter")',src)
        self.assertNotIn('QKeySequence("Ctrl+Alt+O")',src)
        for obsolete in ('QKeySequence("Ctrl+Alt+E")','QKeySequence("Ctrl+Alt+R")','QKeySequence("Ctrl+Alt+D")','QKeySequence("Ctrl+Alt+F")','QKeySequence("Ctrl+Alt+L")'):
            self.assertNotIn(obsolete,src)
        toggle=src[src.index('    def toggle_library_visibility'):src.index('    def show_library')]
        self.assertIn('self.library_sidebar_position in ("left", "right")',toggle)
        self.assertIn('self._library_sidebar_shortcut_hidden',toggle)
        self.assertIn('self.library_dialog.isVisible()',toggle)
        sidebar=src[src.index('    def _apply_library_sidebar_position'):src.index('    def set_drop_open_mode')]
        self.assertIn('or self._library_sidebar_shortcut_hidden',sidebar)
    def test_checker_is_fully_removed(self):
        src=(PKG/'app.py').read_text()
        for token in ('source_checks','check_source','content_language_hint','document_check_label','document_check_summary','Structure OK'):
            self.assertNotIn(token,src)
        self.assertFalse((PKG/'source_checks.py').exists())
        self.assertFalse((PKG/'qa/tests/test_source_checks.py').exists())
        properties=src[src.index('    def show_properties'):src.index('    def _documentation_path')]
        self.assertNotIn('Document check:',properties)

    def test_sidebar_library_is_compact_and_closable(self):
        src=(PKG/'app.py').read_text()
        self.assertIn('self.library_sidebar = LibraryPanel(self, sidebar_mode=True)',src)
        self.assertIn('self.catalogue_combo = QComboBox(self)',src)
        self.assertIn('self.close_sidebar_button.setText("×")',src)
        self.assertIn('self.window.close_library_sidebar',src)
        close=src[src.index('    def close_library_sidebar'):src.index('    def _apply_library_sidebar_position')]
        self.assertIn('self._library_sidebar_shortcut_hidden = True',close)
        self.assertIn('self._apply_library_sidebar_position()',close)
        self.assertNotIn('set_library_sidebar_position',close)
        self.assertNotIn('_save_preferences()',close)
        sidebar_init=src[src.index('class LibraryPanel'):src.index('class LibraryDialog')]
        self.assertIn('if not self.sidebar_mode:',sidebar_init)
        self.assertIn('self.add_custom_button = None',sidebar_init)
        self.assertIn('self.export_button = None',sidebar_init)
        dialog=src[src.index('class LibraryDialog'):src.index('class JSTSPadWindow')]
        self.assertIn('self.panel = LibraryPanel(window, self)',dialog)
        self.assertNotIn('sidebar_mode=True',dialog)

    def test_library_defaults_to_favourites_when_available(self):
        src=(PKG/'app.py').read_text()
        panel=src[src.index('class LibraryPanel'):src.index('class LibraryDialog')]
        self.assertIn('def _has_current_language_favourites',panel)
        self.assertIn('return "Favourites" if self._has_current_language_favourites() else "All"',panel)
        self.assertIn('language_changed = language != self._catalogue_language',panel)
        self.assertIn('if not self._category_signature or language_changed',panel)
        self.assertIn('self._set_current_category("All")',panel)

    def test_split_find_is_inside_editor_column_and_sidebar_hidden_on_start(self):
        src=(PKG/'app.py').read_text()
        self.assertIn('self.editor_column = QWidget(self)',src)
        self.assertIn('self.workspace_splitter.addWidget(self.editor_column)',src)
        layout=src[src.index('    def _apply_layout_mode'):src.index('    def set_library_sidebar_position')]
        self.assertIn('self.editor_column_layout.addWidget(self.bottom_search)',layout)
        self.assertIn('if split and self.document_active:',layout)
        sidebar=src[src.index('    def _apply_library_sidebar_position'):src.index('    def set_drop_open_mode')]
        self.assertIn('not self.document_active',sidebar)
        self.assertIn('or position == "disabled"',sidebar)
        self.assertIn('editor_column = self.editor_column',sidebar)
        start=src[src.index('    def _show_start_panel'):src.index('    def _show_document_workspace')]
        document=src[src.index('    def _show_document_workspace'):src.index('    def _handle_startup_without_file')]
        self.assertIn('self._apply_library_sidebar_position()',start)
        self.assertIn('self._apply_library_sidebar_position()',document)

    def test_no_preview_or_source_execution_actions(self):
        src=(PKG/'app.py').read_text()
        self.assertNotIn('Preview in default browser',src)
        for pattern in (r'"Run JavaScript"',r'"Run TypeScript"',r'"Launch"\s*,\s*self\.',r'node_command',r'npm_command'):
            self.assertIsNone(re.search(pattern,src,re.I))
    def test_edit_menu_reviewed_labels(self):
        src=(PKG/'app.py').read_text()
        self.assertIn('"Toggle Comment"',src); self.assertIn('"Duplicate Line / Selection"',src); self.assertIn('"Delete Line"',src); self.assertIn('QKeySequence("Ctrl+Shift+K")',src)
    def test_json_profile_absent(self):
        profiles=(PKG/'document_profiles.py').read_text().lower(); self.assertNotIn('"json"',profiles)
    def test_jsts_identity_not_old_product_identity(self):
        checked=[PKG/'app.py',PKG/'document_profiles.py',PKG/'packaging/appimage/jsts-pad.desktop',PKG/'packaging/appimage/io.github.brunonlinespace.jsts-pad.metainfo.xml']
        for p in checked:
            text=p.read_text().lower(); self.assertNotIn('timblee pad',text); self.assertNotIn('sheepy pad',text)

if __name__ == "__main__": unittest.main()
