## 0.1.3 — 2026-11-03

- Corrected the locked public source-root filename from `README` to `README.md`.
- AppImage/source packaging and QA now require `README.md` at source root.
- No application behavior changes from 0.1.2.

## 0.1.2 — 2026-11-03

- Ported Sheepy Pad's EOF scrolling correction by changing the editor from global `setCenterOnScroll(True)` to `setCenterOnScroll(False)`.
- Go To Line retains its explicit `centerCursor()` behavior.
- No unrelated editor, gutter, layout, Library, shortcut, theme, file-handling, dependency or workflow changes.

## 0.1.1 — 2026-11-03

- Added the approved public-facing source-root `README` and locked its future content except for version-number updates unless explicitly instructed otherwise.
- Updated the AppImage builder and source QA contract to require the new root README and record its SHA-256 in build provenance.
- No application behavior changes from 0.1.0.

## 0.1.0 — 2026-09-23

- Promote JSTS Pad to **0.1.0** on the `0.0.1-exp1-r9` behavioral baseline.
- Adopt the canonical Suite Pythoine portable/AppImage packaging contract and authoritative component manifest.
- Standardize PyInstaller build requirements and harden build-root cleanup.
- Correct the Pad-family slogan to **Friendly. Fast. Focused.**
- No editor, Library, document, theme, shortcut or workflow behavior changes.

## 0.0.1-exp1-r9 — 2026-08-23

- Library defaults to Favourites when the active document type has favourites; otherwise it defaults to All.
- Applies to embedded and floating Library surfaces and follows document-type changes.
- Empty Favourites view falls back to All after the last favourite is removed.
- Application version remains **0.0.1-exp1**.

## 0.0.1-exp1-r8 — 2026-08-23

- Corrected the embedded Library sidebar **×** so it transiently hides the sidebar instead of switching the saved placement to Floating Only.
- Left/Right placement is preserved; `Ctrl+L` reopens the preferred sidebar.
- Application version remains **0.0.1-exp1**.

## 0.0.1-exp1-r7 — 2026-08-23

- Changed **Open in External Editor** to `Ctrl+Shift+E`.
- Removed the **Properties** keyboard shortcut.
- Application version remains **0.0.1-exp1**.

## 0.0.1-exp1-r6 — 2026-08-23

- Simplified embedded Left/Right Library sidebar mode by removing the lower custom-snippet management buttons there only.
- Floating Library remains fully featured, including custom snippet creation/edit/removal/management controls.
- Application version remains **0.0.1-exp1**.

# Changelog

## 0.0.1-exp1-r5 — 2026-08-23

- Expanded the built-in JS/TS/JSX/TSX Library without removing any existing built-in snippet.
- Added **Comment** and **Duplicate** permanent toolbar buttons using the existing Toggle Comment and Duplicate Line / Selection actions.
- Changed Library to `Ctrl+L` and made the shortcut toggle the user-selected embedded or floating Library presentation.
- Removed the Delete File shortcut and reassigned Properties (`Alt+Enter`), External Editor (`Ctrl+Alt+O`), Rename (`F2`), Duplicate File (`Ctrl+Shift+D`) and Open Containing Folder (`Ctrl+Shift+O`).
- Application version remains **0.0.1-exp1**.

## 0.0.1-exp1-r4 — 2026-08-23

- Removed automatic source checking/status and checker implementation.
- Removed the toolbar Document Type shortcut while retaining File → Document Type.
- Added compact drop-down + × close treatment to embedded Library sidebars; floating Library stays tabbed.
- Moved Split Find into a dedicated editor column so sidebars span the full workspace height.
- Suppressed embedded Library visibility on Start a Document while preserving the saved placement preference.
- Application version remains **0.0.1-exp1**.

## 0.0.1-exp1-r3 — 2026-08-22

- On the no-document **Start a Document** screen, every visible command in the **Edit** menu is now disabled/greyed while the menu itself remains discoverable.
- Edit commands are re-enabled automatically whenever a document is created or opened. **View Only** continues to disable only document-changing Edit commands while leaving copy/navigation/select commands available.
- Centralised Edit-state refresh in the Start/document workspace transitions so files opened at application launch receive the correct active-document state.
- Application version remains **0.0.1-exp1**.

## 0.0.1-exp1-r2 — 2026-08-22

- Corrected **View → File Drag Drop** to **File Drag and Drop**; choices remain **Opens on Active Window** and **Opens on New Window**.
- The Find bar now remains visible but disabled on the no-document **Start a Document** screen, in the exact position selected by the persisted Layout.
- The Find bar is automatically re-enabled when a document becomes active.
- Application version remains **0.0.1-exp1**.

## 0.0.1-exp1-r1 — 2026-08-22

- Fixed the no-document **Start a Document** layout by placing it and the normal editor/Library splitter in one `QStackedWidget` workspace slot, matching the Timblee Pad startup-layout correction.
- All four persisted Layout choices now apply identically on the initial screen and after opening/creating a document; the Start screen no longer force-hides the Find bars.
- Added persistent **View → Dark Editor**, enabled by default, switching the editor canvas and JavaScript/TypeScript/JSX/TSX syntax palette together between dark and light independently of AppImage chrome theme.
- Relabelled **View → Behaviour** to **File Drag Drop**, with **Opens on Active Window** and **Opens on New Window**.
- Application version remains **0.0.1-exp1**.

## 0.0.1-exp1 — 2026-08-16

- Initial experimental JSTS Pad source release.
- Added JavaScript, TypeScript, JSX and TSX document profiles.
- Added dependency-free JavaScript-family highlighter and conservative structure/type checks.
- Retained hardened Pad-family source editing: safe paste/file bounds, line numbers, search/replace, bracket matching, View Only, line operations and guarded saves.
- Added in-window **Start a Document** state with configurable default type/template and **Always Ask** factory default.
- Added editable custom templates, immutable factory templates and `[[cursor]]` placement.
- Added language-aware searchable Library with favourites and bounded custom snippets.
- Added toolbar document-type selector and non-destructive type switching.
- Added filename/type mismatch warning.
- Adopted the approved parchment notebook with thick crimson JSTS monogram as the official application artwork.
- Added portable source/AppImage packaging and dependency-free QA.
- Deliberately omitted source execution, Node/npm, JSON, debugger/LSP, WebEngine and IDE/project machinery.
