# JSTS Pad 0.1.3 — README filename contract audit

0.1.3 is a publication/source-packaging correction built from 0.1.2. No application behavior changes are included.

- Source root contains `README.md`, `main.py`, `suite-pythoine-component.json`, and `jsts_pad/`.
- AppImage builder and QA require `${PROJECT_ROOT}/README.md`.
- Locked root `README.md` changed only for release-number occurrences (`0.1.2` → `0.1.3`); its substantive text is otherwise identical.
- 0.1.2 editor scrolling behavior remains unchanged.

# JSTS Pad 0.1.2 — Editor EOF scrolling audit

## Scope

0.1.2 is a parity-only editor-behaviour corrective built from **0.1.1**, matching Sheepy Pad's EOF scrolling fix.

## Changes

- `jsts_pad/code_editor.py`: changed global `self.setCenterOnScroll(True)` to `self.setCenterOnScroll(False)`.
- Explicit `self.centerCursor()` behavior used by Go To Line remains unchanged.
- Added a focused static regression covering both requirements.

## Non-changes

- No Sheepy gutter correction was ported in this release.
- No layout, Library, shortcut, theme, file-handling, dependency, execution/lint/checking or workflow behavior changed.
- Locked root `README` content changed only for release-number occurrences (`0.1.1` → `0.1.2`).

# JSTS Pad 0.1.1 — root README / packaging-contract audit

## Scope

0.1.1 is a publication and packaging-contract release built from **0.1.0**. Application behavior is intentionally unchanged.

## Changes

- Added the approved public-facing `README` at source root.
- Root README content is locked for future releases except for version-number updates unless an explicit content change is requested.
- Fedora AppImage builder requires `${PROJECT_ROOT}/README` and records its SHA-256 in build provenance.
- Source-root QA now requires exactly `README`, `main.py`, `suite-pythoine-component.json`, and `jsts_pad/`.
- `SOURCE_MANIFEST.sha256` includes the root README.

## Non-changes

- No editor, Library, shortcut, theme, file-handling, dependency, execution/lint/checking or workflow behavior changes.

# JSTS Pad 0.1.0 — AppImage/portable packaging audit

Date: 2026-09-23

## Scope

0.1.0 is a packaging-focused release on the `0.0.1-exp1-r9` behavioral baseline. Application behavior is intentionally unchanged. The only application-facing text change is the Pad-family slogan **Friendly. Fast. Focused.**

## Packaging contract

- Root portable tree: `main.py`, `suite-pythoine-component.json`, `jsts_pad/`.
- Suite manifest is authoritative for component ID, version, routing, portable entry point, desktop identity and slogan.
- Fedora AppImage builder remains non-privileged and supports native x86_64/aarch64 on validated Fedora 43/44 hosts.
- PyInstaller build requirements live under `packaging/pyinstaller/`.
- `BUILD_ROOT` cleanup is constrained beneath `jsts_pad/build/`.
- Existing AppDir and finished-AppImage GUI/version smoke matrices remain in place.

# JSTS Pad 0.0.1-exp1-r9 — Library default-selection audit

## Scope

This is a narrow maintenance revision of **0.0.1-exp1-r8**. The application version remains `0.0.1-exp1`.

## r9 changes

- Both Library surfaces choose `Favourites` as their initial catalogue when the current JS/TS/JSX/TSX document type has at least one favourite item.
- When the current document type has no favourites, the initial catalogue is `All`.
- The default is recalculated when document type changes.
- If the last favourite is removed while `Favourites` is selected, the catalogue automatically falls back to `All` rather than displaying an empty default view.
- User-selected non-empty catalogue views remain stable during ordinary refreshes.
- No runtime/build dependency changes.

# JSTS Pad 0.0.1-exp1-r8 — Library sidebar close audit

## Scope

This is a narrow maintenance revision of **0.0.1-exp1-r7**. The application version remains `0.0.1-exp1`.

## r8 change

The embedded Library's small `×` no longer calls the placement setter with `Floating Only`. It now sets only the transient sidebar-hidden state and reapplies the current placement. This preserves the user's saved `Left Sidebar` or `Right Sidebar` preference. `Ctrl+L` remains the placement-aware toggle and can show the sidebar again.

No other UI, Library catalogue, shortcut, runtime, build or dependency behavior changed.

# JSTS Pad 0.0.1-exp1-r7 — shortcut correction audit

## Scope

This is a narrow maintenance revision of **0.0.1-exp1-r6**. The application version remains `0.0.1-exp1`.

## r7 changes

- Rebound `Open in External Editor` to `Ctrl+Shift+E`.
- Removed the Properties shortcut entirely.
- No other menu, toolbar, Library, editor, packaging, runtime, or dependency behavior changed.

# JSTS Pad 0.0.1-exp1-r6 — embedded Library simplification audit

## Scope

This is a narrow maintenance revision of **0.0.1-exp1-r5**. The application version remains `0.0.1-exp1`. It simplifies only the embedded sidebar Library presentation while keeping the floating Library fully featured.

## r6 changes

- In embedded Left/Right Sidebar mode, removed the lower custom-snippet management buttons:
  - `Add Custom Snippet…`
  - `Remove Custom`
  - `Edit Custom…`
  - `Manage Snippets…`
- Floating Library mode is unchanged and still exposes all custom snippet management controls.
- No runtime/build dependencies changed.

## Validation

- `python3 -m unittest discover -s jsts_pad/qa/tests -p 'test_*.py'`: pass.
- `python3 jsts_pad/qa/release_check.py`: pass.

# JSTS Pad 0.0.1-exp1-r5 — Library/toolbar/shortcut audit

Date: 2026-08-23

## Scope

Built from the canonical **0.0.1-exp1-r4** source. The application version remains `0.0.1-exp1`.

## r5 changes

- Preserved every original built-in Library entry and added separate additive expansion tuples for common JavaScript, TypeScript, JSX and TSX patterns. Resolved built-in counts are 97 JS, 145 TS, 139 JSX and 213 TSX with unique keys per document type.
- Added only two permanent code-editing toolbar shortcuts: **Comment** and **Duplicate**. They trigger the existing Edit actions while mirroring only enabled state, preserving the shorter toolbar labels across Start-screen and View Only state changes.
- Rebound the Library action to `Ctrl+L`. The action now respects **View → Library** placement: a selected Left/Right Sidebar is toggled transiently without rewriting the saved placement preference; **Floating Only** toggles the modeless floating Library. Direct placement selection resets a transient shortcut-hide state and shows the selected sidebar when a document is active.
- Removed the Delete File keybinding while retaining the command.
- Rebound Properties to `Alt+Enter`, Open in External Editor to `Ctrl+Alt+O`, Rename to `F2`, Duplicate File to `Ctrl+Shift+D`, and Open Containing Folder to `Ctrl+Shift+O`.
- Preserved r4's checker removal, compact embedded Library, split-layout editor column and Start-screen sidebar suppression, plus all r1-r3 startup/editor-state behavior.
- No dependency, execution, linting or validation engine was added.

## Validation

- Dependency-free unit/regression suite: **59/59 PASS**.
- Static release checker and source manifest verification: **PASS**.
- Python parsing and Library key-uniqueness/count regressions: **PASS**.
- Bundled shell syntax and AppStream XML verification: **PASS**.
- PyQt6 is not installed in this construction environment, so live Fedora GUI acceptance remains the final interactive smoke step.

---

# JSTS Pad 0.0.1-exp1-r4 — Library/layout simplification audit

Date: 2026-08-23

## Scope

Built from the canonical **0.0.1-exp1-r3** source. The application version remains `0.0.1-exp1`.

## r4 changes

- Removed the automatic source checker completely: no Structure OK/warning status, no content-language hints, no checker timer/state, no checker field in Properties, and no `source_checks.py` implementation or checker tests.
- Removed the permanent toolbar **Document Type** shortcut. **File → Document Type** remains the explicit control, while opening a supported file still assigns its document type internally from the extension.
- Reworked the embedded Library to match the Timblee/Sheepy family pattern: the sidebar uses a compact catalogue drop-down and a small **×** close button; closing switches the saved placement to **Floating Only**. The floating Library remains tabbed.
- Reworked Split layouts around a dedicated editor column. The Split Find bar now belongs to the editor column, so a left/right Library sidebar spans the full workspace height. Inline layouts are unchanged.
- The embedded Library is always hidden while **Start a Document** is active without changing the saved left/right/Floating Only preference; creating or opening a document restores the selected sidebar placement.
- Preserved r3's disabled Edit menu on Start, r2's visible-but-disabled Find bar on Start, r1's stacked Start/editor workspace, Dark Editor, and File Drag and Drop behavior.
- No runtime or build dependency was added.

## Validation

- Dependency-free unit/regression suite: **56/56 PASS**.
- Static release checker: **PASS**.
- Python AST parse: **PASS**.
- AppStream XML parse and bundled shell syntax are part of final archive verification.
- PyQt6 is not installed in this release environment, so the final Fedora GUI smoke should verify the sidebar/drop-down/close control and both Split orientations visually.

---

# JSTS Pad 0.0.1-exp1-r3 — Start-screen Edit-state audit

Date: 2026-08-22

## Scope

This is a narrow maintenance revision of **0.0.1-exp1-r2**. The application version remains `0.0.1-exp1`; r2's visible-but-disabled Start-screen Find bar, r1's stacked-workspace startup-layout fix, Dark Editor behavior, editor/highlighter implementation, templates, Library, document checks, runtime/packaging policy and assets remain otherwise unchanged.

## r3 changes

- The **Edit** menu stays present on **Start a Document**, but every non-separator action inside it is disabled while `document_active` is false.
- When a document is active, all Edit actions are restored first, then existing **View Only** protection is applied only to mutating commands. Copy, Select All and Go To Line therefore remain available in View Only.
- Edit-state refresh now runs from both `_show_start_panel()` and `_show_document_workspace()`, covering normal Start/create/open transitions and files loaded directly at application launch.
- Added a static regression guard for disabled-on-Start and re-enabled-on-document Edit state.

## Validation

- Dependency-free unit/regression suite: **63/63 PASS**.
- JSTS release checker: **PASS**.
- Python AST parsing through the release checker: **PASS**.
- Source manifest: **57 files verified**.
- No generated Python caches in the source tree: **PASS**.
- `python3 main.py --version`: **JSTS Pad 0.0.1-exp1**.
- Bundled shell syntax and AppStream XML are checked again when the finished source archive is produced.
- PyQt6 is not installed in this construction environment, so live GUI acceptance should verify that every Edit command is greyed on Start and restored with an active document, including an initial file passed on the command line.

---

# JSTS Pad 0.0.1-exp1-r2 — Start-screen Find-state audit

Date: 2026-08-22

## Scope

This is a narrow maintenance revision of **0.0.1-exp1-r1**. The application version remains `0.0.1-exp1`; r1's stacked-workspace startup-layout fix, Dark Editor behavior, editor/highlighter implementation, templates, Library, document checks, runtime/packaging policy and assets remain otherwise unchanged.

## r2 changes

- Corrected the View submenu label from **File Drag Drop** to **File Drag and Drop**.
- Added one document-state helper that disables both Find-bar hosts while the **Start a Document** workspace is active without changing their visibility or position.
- Re-enables both Find-bar hosts whenever the document workspace becomes active, so whichever one the selected Layout displays has the correct enabled state.
- Added static regression guards for disabled-on-Start, enabled-on-document behavior and the exact new menu label.

## Validation

- Dependency-free unit/regression suite: **62/62 PASS**.
- JSTS release checker: **PASS**.
- Python AST parsing through the release checker: **PASS**.
- Source manifest: **57 files verified**.
- No generated Python caches in the source tree: **PASS**.
- `python3 main.py --version`: **JSTS Pad 0.0.1-exp1**.
- Bundled shell syntax and AppStream XML are checked again when the finished source archive is produced.
- PyQt6 is not installed in this construction environment, so live GUI acceptance should specifically verify disabled-on-Start and enabled-on-document Find-bar appearance in all four Layout modes.

---

# JSTS Pad 0.0.1-exp1-r1 — startup layout/editor-palette audit

Date: 2026-08-22

## Scope

This is a focused source revision of **0.0.1-exp1**. The application version remains `0.0.1-exp1`; JavaScript/TypeScript/JSX/TSX editing, templates, Library, document checks, official artwork and packaging policy are otherwise unchanged.

## r1 changes

- Replaced the separate outer Start-panel layout item with a `QStackedWidget` workspace host containing **Start a Document** and the normal editor/Library splitter. `_apply_layout_mode()` now arranges that one host, so all four persisted Inline/Split toolbar and Find-bar choices apply identically in the no-document state.
- Removed the Start panel's forced hiding of both Find bars.
- Added persistent **Dark Editor** (default `true`) using JSTS's existing paired dark/light editor and JavaScript-family syntax palettes, independent of AppImage chrome theme.
- Relabelled the drag/drop submenu and choices to **File Drag Drop → Opens on Active Window / Opens on New Window**.
- Added static regression guards for the shared workspace host, Find-bar visibility, independent editor palette, and exact drag/drop labels.

## Validation

- Dependency-free unit/regression suite: **62/62 PASS**.
- JSTS release checker: **PASS**.
- Python AST parsing through the release checker: **PASS**.
- Source manifest: **57 files verified**.
- No generated Python caches in the source tree: **PASS**.
- `python3 main.py --version`: **JSTS Pad 0.0.1-exp1**.
- Bundled shell syntax and AppStream XML are checked again when the finished source archive is produced.
- PyQt6 is not installed in this construction environment, so the live GUI was not executed here; Fedora GUI acceptance should specifically exercise all four no-document layout modes and Dark Editor/AppImage-theme independence.

---

# JSTS Pad 0.0.1-exp1 — release audit

Date: 2026-08-16

## Release identity

- Product: **JSTS Pad**
- Version: **0.0.1-exp1**
- Python package: `jsts_pad`
- Executable: `jsts-pad`
- Desktop ID: `jsts-pad.desktop`
- AppStream ID: `io.github.brunonlinespace.jsts-pad`
- Linux preferences: `~/.config/brunonlinespace/jsts-pad/jsts-pad.json`
- Portable outer tree: `main.py` + `jsts_pad/`

## Functional scope

This first experimental source supports JavaScript (`.js/.mjs/.cjs`), TypeScript (`.ts/.mts/.cts`), JSX (`.jsx`) and TSX (`.tsx`). JSON is deliberately excluded.

The editor combines the mature Pad-family source-editing mechanics associated with Sheepy/Timblee with the later Timblee document-profile, Start a Document, editable-template and language-aware Library model. JSTS Pad is standalone and has no runtime dependency on either application.

No JavaScript/TypeScript execution, Node/npm, compiler, debugger, language server, embedded terminal, project/workspace manager, ESLint/Prettier or Qt WebEngine was added.

## Official artwork

The user-approved official logo is bundled as the canonical 1024×1024 RGBA master and derived hicolor sizes. It is the parchment/scroll-textured notebook with the thick crimson JSTS monogram, transparent exterior background and no product-name text.

Canonical master SHA-256:

```text
61b6574b4c9da7c92e01e309aa0d0fb795c0010e57f84b56f332743ab06a5e6e
```

Dependency-free PNG validation confirmed 1024×1024, 8-bit RGBA and alpha values spanning fully transparent to fully opaque.

## Automated verification

- Dependency-free unit/static suite: **59/59 PASS**.
- JSTS release checker: **PASS**.
- Python AST/compileall validation: **PASS** (bytecode redirected outside source tree).
- `python3 main.py --version`: **JSTS Pad 0.0.1-exp1**.
- AppStream XML parse: **PASS**.
- Bundled shell scripts `bash -n`: **PASS**.
- Portable outer-root policy: **PASS**.
- Source cache cleanliness: **PASS**.
- AppImage builder privilege policy: **PASS**; no direct sudo/dnf/su/pkexec invocation.
- PyInstaller exclusions include QtPdf/QtPdfWidgets/QtPrintSupport/QtWebEngine*.

## Live-test boundary

PyQt6 is not installed in the artifact-construction environment, so a live Qt GUI launch and AppImage build were not performed here. The included Fedora GUI checklist must be exercised before promoting this experimental line. In particular, test Start a Document/default behavior, each language highlighter, JSX/TSX editing, Library/template dialogs, non-destructive document-type switching, file mismatch warnings, View Only and the AppImage theme smoke matrix.
