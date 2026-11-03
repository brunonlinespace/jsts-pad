#!/usr/bin/env python3
"""Dependency-free static release checks for JSTS Pad."""
from __future__ import annotations
import ast, hashlib, json, re, sys, xml.etree.ElementTree as ET
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PKG=ROOT/'jsts_pad'
ERRORS=[]

def check(condition: bool, message: str) -> None:
    if not condition: ERRORS.append(message)

def main() -> int:
    check({p.name for p in ROOT.iterdir()}=={'README.md','main.py','suite-pythoine-component.json','jsts_pad'}, 'portable outer root must contain only README.md + main.py + suite-pythoine-component.json + jsts_pad/')
    check((ROOT/'README.md').is_file(), 'source-root README.md missing')
    check((PKG/'LICENSE').is_file(), 'LICENSE missing')
    init=(PKG/'__init__.py').read_text(encoding='utf-8')
    check('APP_VERSION = "0.1.3"' in init, 'package version mismatch')
    component_path=ROOT/'suite-pythoine-component.json'
    check(component_path.is_file(), 'suite-pythoine-component.json missing')
    if component_path.is_file():
        try:
            component=json.loads(component_path.read_text(encoding='utf-8'))
        except Exception as exc:
            ERRORS.append(f'Suite component manifest invalid: {exc}')
            component={}
        check(component.get('id')=='jsts-pad' and component.get('version')=='0.1.3', 'Suite component identity/version mismatch')
        check(component.get('extensions')==['.js','.mjs','.cjs','.ts','.mts','.cts','.jsx','.tsx'], 'Suite component routing mismatch')
        check(component.get('portable_command')==['main.py'], 'Suite component portable command mismatch')
        check(component.get('tagline')=='Friendly. Fast. Focused.', 'Suite component tagline mismatch')
    check((PKG/'assets/icons/jsts-pad-master.png').is_file(), 'official master icon missing')
    if (PKG/'assets/icons/jsts-pad-master.png').is_file():
        digest=hashlib.sha256((PKG/'assets/icons/jsts-pad-master.png').read_bytes()).hexdigest()
        check(digest=='61b6574b4c9da7c92e01e309aa0d0fb795c0010e57f84b56f332743ab06a5e6e','official master icon hash changed')
    for p in [ROOT/'main.py', *PKG.rglob('*.py')]:
        if '__pycache__' in p.parts: continue
        try: ast.parse(p.read_text(encoding='utf-8'), filename=str(p))
        except Exception as exc: ERRORS.append(f'Python parse failed: {p.relative_to(ROOT)}: {exc}')
    try: ET.parse(PKG/'packaging/appimage/io.github.brunonlinespace.jsts-pad.metainfo.xml')
    except Exception as exc: ERRORS.append(f'AppStream XML invalid: {exc}')
    desktop=(PKG/'packaging/appimage/jsts-pad.desktop').read_text(encoding='utf-8')
    for required in ('Name=JSTS Pad','Exec=jsts-pad %F','Icon=jsts-pad','application/javascript','text/typescript'):
        check(required in desktop, f'desktop metadata missing {required}')
    editor_source=(PKG/'code_editor.py').read_text(encoding='utf-8')
    check('self.setCenterOnScroll(False)' in editor_source, '0.1.2 EOF scrolling corrective missing')
    check('self.setCenterOnScroll(True)' not in editor_source, 'legacy global center-on-scroll remains enabled')
    check('self.centerCursor()' in editor_source, 'explicit Go To Line centering must remain available')
    profiles=(PKG/'document_profiles.py').read_text(encoding='utf-8')
    for extension in ('.js','.mjs','.cjs','.ts','.mts','.cts','.jsx','.tsx'):
        check(extension in profiles, f'profile extension missing {extension}')
    check('"json"' not in profiles.lower(), 'JSON profile must remain out of exp1')
    app=(PKG/'app.py').read_text(encoding='utf-8')
    check('<b>Friendly. Fast. Focused.</b>' in app, 'Pad-family slogan missing from About')
    for required in ('Start a Document','Default New Document…','Duplicate Line / Selection','Delete Line','Ctrl+Shift+K','QStackedWidget','self.workspace_stack','Dark Editor','"dark_editor": self.dark_editor','File Drag and Drop','Opens on Active Window','Opens on New Window','self.comment_toolbar_button.setText("Comment")','self.duplicate_toolbar_button.setText("Duplicate")','QKeySequence("Ctrl+L")','QKeySequence("Ctrl+Shift+E")','QKeySequence("F2")','QKeySequence("Ctrl+Shift+D")','QKeySequence("Ctrl+Shift+O")','def toggle_library_visibility'):
        check(required in app, f'app contract missing {required}')
    for obsolete_shortcut in ('QKeySequence("Ctrl+Delete")','QKeySequence("Alt+Enter")','QKeySequence("Ctrl+Alt+O")','QKeySequence("Ctrl+Alt+E")','QKeySequence("Ctrl+Alt+R")','QKeySequence("Ctrl+Alt+D")','QKeySequence("Ctrl+Alt+F")','QKeySequence("Ctrl+Alt+L")'):
        check(obsolete_shortcut not in app, f'obsolete shortcut remains: {obsolete_shortcut}')
    start_block=app[app.index('    def _show_start_panel'):app.index('    def _show_document_workspace')]
    check('self.search_container.hide()' not in start_block and 'self.bottom_search.hide()' not in start_block, 'Start panel must not force-hide Find bars')
    check('self._set_find_bars_enabled(False)' in start_block, 'Start panel must leave the visible Find bar disabled')
    document_block=app[app.index('    def _show_document_workspace'):app.index('    def _handle_startup_without_file')]
    check('self._set_find_bars_enabled(True)' in document_block, 'Document workspace must re-enable Find bars')
    edit_state=app[app.index('    def _update_edit_action_state'):app.index('    # ------------------------------------------------------------------\n    # View behavior')]
    check('for action in self.edit_menu.actions()' in edit_state and 'action.setEnabled(has_document)' in edit_state, 'Edit menu actions must follow document-active state')
    check('self._update_edit_action_state()' in start_block, 'Start panel must refresh Edit actions to disabled state')
    check('self._update_edit_action_state()' in document_block, 'Document workspace must refresh Edit actions to active state')
    for forbidden in ('document_type_button','document_check_label','document_check_summary','check_source','content_language_hint','Structure OK'):
        check(forbidden not in app, f'removed r4 UI/checker token remains: {forbidden}')
    check(not (PKG/'source_checks.py').exists(), 'automatic source checker module must be removed')
    check(not (PKG/'qa/tests/test_source_checks.py').exists(), 'automatic source checker tests must be removed with feature')
    check('self.library_sidebar = LibraryPanel(self, sidebar_mode=True)' in app, 'embedded Library must use compact sidebar mode')
    sidebar_block=app[app.index('    def _apply_library_sidebar_position'):app.index('    def set_drop_open_mode')]
    check('or self._library_sidebar_shortcut_hidden' in sidebar_block, 'sidebar Library must support transient Ctrl+L show/hide without changing placement preference')
    catalog=(PKG/'library_catalog.py').read_text(encoding='utf-8')
    for required in ('JS_MORE = (','TS_MORE = (','JSX_MORE = (','TSX_MORE = (','console.log','type guard','useState','typed mouse event'):
        check(required in catalog, f'enriched Library contract missing {required}')
    check('self.catalogue_combo = QComboBox(self)' in app and 'self.close_sidebar_button.setText("×")' in app, 'sidebar Library compact catalogue/close controls missing')
    check('self.close_sidebar_button.clicked.connect(\n                self.window.close_library_sidebar' in app, 'sidebar close button must hide rather than change Library placement')
    close_block=app[app.index('    def close_library_sidebar'):app.index('    def _apply_library_sidebar_position')]
    check('self._library_sidebar_shortcut_hidden = True' in close_block and '_save_preferences()' not in close_block and 'set_library_sidebar_position' not in close_block, 'sidebar close must be transient and preserve saved Left/Right placement')
    check('if not self.sidebar_mode:' in app and 'self.add_custom_button = None' in app and 'self.export_button = None' in app, 'sidebar Library must omit custom snippet management buttons')
    check('def _has_current_language_favourites' in app and 'return "Favourites" if self._has_current_language_favourites() else "All"' in app, 'Library must default to Favourites when the current language has favourites, otherwise All')
    check('self.editor_column = QWidget(self)' in app and 'self.editor_column_layout.addWidget(self.bottom_search)' in app, 'Split Find must live in editor column')
    check('not self.document_active' in sidebar_block and 'or position == "disabled"' in sidebar_block, 'Library sidebar must stay hidden on Start a Document')
    theme_block=app[app.index('    def apply_appimage_theme'):app.index('    def toggle_appimage_dark_mode')]
    check('set_color_scheme' not in theme_block, 'AppImage chrome theme must not override Dark Editor')
    for forbidden in ('Preview in default browser','Run JavaScript','Run TypeScript','Node.js','npm install'):
        check(forbidden.lower() not in app.lower(), f'forbidden execution/preview UI found: {forbidden}')
    spec=(PKG/'packaging/pyinstaller/jsts-pad.spec').read_text(encoding='utf-8')
    for module in ('PyQt6.QtPdf','PyQt6.QtPrintSupport','PyQt6.QtWebEngineCore','PyQt6.QtWebEngineWidgets'):
        check(module in spec, f'PyInstaller exclusion missing {module}')
    builder=(PKG/'packaging/fedora/build-appimage.sh').read_text(encoding='utf-8')
    check('JSTS-Pad-${APP_VERSION}-${ARCH}.AppImage' in builder,'AppImage output identity mismatch')
    check('COMPONENT_MANIFEST="${PROJECT_ROOT}/suite-pythoine-component.json"' in builder, 'Suite component manifest build input missing')
    check('PUBLIC_README="${PROJECT_ROOT}/README.md"' in builder, 'root README build input missing')
    check('Root README SHA-256:' in builder, 'root README provenance missing')
    check('BUILD_REQUIREMENTS="${PROGRAM_ROOT}/packaging/pyinstaller/build-requirements.txt"' in builder, 'canonical PyInstaller build requirements missing')
    check('validate_build_root()' in builder, 'guarded AppImage build root missing')
    check('Suite component manifest SHA-256:' in builder, 'Suite component manifest provenance missing')
    check((PKG/'packaging/pyinstaller/build-requirements.txt').is_file(), 'canonical build requirements missing')
    check(not (PKG/'packaging/fedora/requirements-build.txt').exists(), 'legacy Fedora-local build requirements still present')
    appimage_test=(PKG/'packaging/fedora/test-appimage.sh').read_text(encoding='utf-8')
    check('JSTS-Pad-0.1.3-${ARCH}.AppImage' in appimage_test, 'AppImage test filename version mismatch')
    for script in (PKG/'packaging/fedora').glob('*.sh'):
        for lineno,line in enumerate(script.read_text(encoding='utf-8').splitlines(),1):
            stripped=line.strip()
            if not stripped or stripped.startswith('#'): continue
            if re.match(r'^(?:sudo|dnf|pkexec|su)(?:\s|$)',stripped):
                ERRORS.append(f'privileged/package-manager invocation in {script.name}:{lineno}')
    manifest=PKG/'SOURCE_MANIFEST.sha256'
    check(manifest.is_file(), 'SOURCE_MANIFEST.sha256 missing')
    if manifest.is_file():
        expected={}
        for line in manifest.read_text(encoding='utf-8').splitlines():
            if not line.strip(): continue
            try: digest, relative=line.split('  ',1)
            except ValueError:
                ERRORS.append('invalid SOURCE_MANIFEST.sha256 line'); continue
            expected[relative]=digest
        actual={}
        for path in sorted(ROOT.rglob('*')):
            if not path.is_file() or path == manifest or '__pycache__' in path.parts or path.suffix in {'.pyc','.pyo'}:
                continue
            if 'build' in path.parts or 'dist' in path.parts:
                continue
            relative=path.relative_to(ROOT).as_posix()
            actual[relative]=hashlib.sha256(path.read_bytes()).hexdigest()
        check(expected==actual, 'SOURCE_MANIFEST.sha256 does not match source tree')
    for cache in PKG.rglob('__pycache__'):
        ERRORS.append(f'cache directory present: {cache.relative_to(ROOT)}')
    for compiled in list(PKG.rglob('*.pyc'))+list(PKG.rglob('*.pyo')):
        ERRORS.append(f'compiled Python artifact present: {compiled.relative_to(ROOT)}')
    if ERRORS:
        print('JSTS Pad release check: FAIL', file=sys.stderr)
        for error in ERRORS: print(f' - {error}', file=sys.stderr)
        return 1
    print('JSTS Pad release check: PASS')
    return 0

if __name__=='__main__': raise SystemExit(main())
