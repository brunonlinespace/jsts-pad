# JSTS Pad 0.1.3 — README filename contract correction

JSTS Pad 0.1.3 corrects the public source-root README filename and its packaging contract. Application behavior is unchanged from 0.1.2.

- Public source-root file is now exactly `README.md`.
- Fedora AppImage builder, source manifest and release QA require `README.md`.
- The locked public README content changes only for release-number occurrences (`0.1.2` → `0.1.3`).
- The 0.1.2 EOF scrolling correction remains unchanged.

# JSTS Pad 0.1.2 — Editor EOF Scrolling Corrective

JSTS Pad 0.1.2 is a narrowly scoped editor-behaviour corrective based on 0.1.1, ported exactly from Sheepy Pad's corresponding EOF scrolling fix.

- Disables `QPlainTextEdit` global center-on-scroll behavior so the end of a document stays naturally near the bottom of the editor instead of allowing a large scrollable blank region below EOF.
- Keeps explicit `centerCursor()` behavior for Go To Line unchanged.
- Makes no layout, gutter, Library, shortcut, theme, file-handling, dependency or workflow changes.
- Application/package version advances to **0.1.2**.

# JSTS Pad 0.1.1

Publication and source-packaging contract release on the **0.1.0** application baseline.

- Adds the approved public-facing `README` at source root, with no filename extension.
- Locks the root `README` content for future releases: only its version number may change unless an explicit README content change is requested.
- Updates the Fedora AppImage builder to require the root `README` and record its SHA-256 in build provenance.
- Updates source-root QA and `SOURCE_MANIFEST.sha256` to require/include `README`.
- No editor, Library, shortcut, theme, file-handling, dependency or workflow behavior changes.

# JSTS Pad 0.1.0

Packaging-focused release on the `0.0.1-exp1-r9` behavioral baseline. Editor, Library, document, theme, shortcut and workflow behavior are intentionally unchanged.

- Promotes the application identity to **0.1.0**.
- Corrects the Pad-family slogan to **Friendly. Fast. Focused.**
- Adds the root `suite-pythoine-component.json` as the authoritative Suite Pythoine identity/version/routing contract.
- Standardizes PyInstaller build requirements at `jsts_pad/packaging/pyinstaller/build-requirements.txt`.
- Makes the Fedora AppImage builder validate and record the Suite component manifest and guards destructive `BUILD_ROOT` cleanup beneath `jsts_pad/build/`.
- Preserves the existing hardened non-privileged Fedora 43/44, native x86_64/aarch64, AppDir/final-AppImage smoke-test, metadata-validation, appimagetool-pinning, checksum, build-info and Python-lock behavior.

# JSTS Pad 0.0.1-exp1-r9

Focused Library default-selection revision. The application version remains **0.0.1-exp1**.

- Library now defaults to **Favourites** when the active document type has at least one favourite Library item.
- If that document type has no favourites, Library defaults to **All** instead of opening an empty Favourites catalogue.
- The rule applies to both embedded sidebar and floating Library surfaces and is re-evaluated when the active document type changes.
- If the final favourite is removed while Favourites is selected, the Library falls back to All.
- No other r8 behavior or dependencies changed.

# JSTS Pad 0.0.1-exp1-r8

Focused Library-sidebar close-behavior correction. The application version remains **0.0.1-exp1**.

- The small **×** in embedded Left/Right Library sidebar mode now only closes/hides that sidebar.
- Closing the sidebar no longer changes View → Library to **Floating Only** and does not alter the saved Left/Right placement preference.
- `Ctrl+L` can show the same preferred sidebar again.
- All r7 shortcuts, r6 sidebar simplification, Library contents, layouts, editor behavior and dependencies remain unchanged.

# JSTS Pad 0.0.1-exp1-r7

Focused shortcut correction. The application version remains **0.0.1-exp1**.

- **Open in External Editor** is now `Ctrl+Shift+E`.
- **Properties** no longer has a keyboard shortcut.
- All r6 Library simplifications and prior behavior remain unchanged.

# JSTS Pad 0.0.1-exp1-r6

Focused embedded-Library simplification revision. The application version remains **0.0.1-exp1**.

- Embedded Left/Right Library sidebar mode now omits the lower custom-snippet management buttons: **Add Custom Snippet…**, **Remove Custom**, **Edit Custom…**, and **Manage Snippets…**.
- Floating Library mode is unchanged and still exposes the full custom snippet management controls.
- No runtime/build dependency changes.

# JSTS Pad 0.0.1-exp1-r5

Focused Library/toolbar/shortcut revision. The application version remains **0.0.1-exp1**.

- Expands the built-in Library additively for all four document types while retaining every previous built-in snippet: **97 JavaScript**, **145 TypeScript**, **139 JSX** and **213 TSX** resolved entries.
- Adds permanent toolbar shortcuts **Comment** (`Ctrl+/`) and **Duplicate** (`Ctrl+D`), backed by the existing Edit actions so Start-screen/View Only enabled state stays synchronized.
- Changes the Library shortcut from `Ctrl+Alt+L` to **`Ctrl+L`** and makes it placement-aware: Left/Right Sidebar toggles that embedded sidebar without changing the saved placement; Floating Only toggles the floating Library window.
- Removes the **Delete File** keybinding. The menu command remains available.
- Changes **Properties** to `Alt+Enter`, **Open in External Editor** to `Ctrl+Alt+O`, **Rename** to `F2`, **Duplicate File** to `Ctrl+Shift+D`, and **Open Containing Folder** to `Ctrl+Shift+O`.
- No runtime/build dependency or execution/lint/checking surface is added.

---

# JSTS Pad 0.0.1-exp1-r4

Focused Library/layout simplification revision. The application version remains **0.0.1-exp1**.

- Removes the automatic structure/content checker entirely and removes its status-bar/Properties surface.
- Removes the permanent toolbar **Document Type** shortcut; **File → Document Type** remains.
- Embedded Library sidebars now use a compact catalogue drop-down plus a small **×** close button that selects **Floating Only**; the floating Library remains tabbed.
- In Split layouts, Find now sits inside the editor column so left/right Library sidebars span the full workspace height.
- The Library sidebar stays hidden on **Start a Document** while preserving the saved placement preference and automatically returns when a document becomes active.
- No extra dependency or validator/linter/parser reliance was added.

---

# JSTS Pad 0.0.1-exp1-r3

Focused no-document Edit-state maintenance revision. The application version remains **0.0.1-exp1**.

## r3 changes

- Keeps the **Edit** menu visible on **Start a Document**, but greys/disables every Edit command until a document is active.
- Re-enables the Edit commands automatically when a document is created or opened, including files supplied at application launch.
- Preserves **View Only** semantics: with an active document, mutating Edit commands remain disabled in View Only while copy/navigation/select commands remain available.
- Preserves r2's visible-but-disabled Start-screen Find bar and r1's shared stacked-workspace layout behavior.

## r2 changes

- Corrects the View submenu name to **File Drag and Drop → Opens on Active Window / Opens on New Window**.
- Keeps the configured Find bar visible on **Start a Document**, but disables it while no document is active.
- Re-enables the Find bar automatically when a document is created or opened.
- Preserves r1's shared stacked-workspace layout behavior in all four Inline/Split modes.

## r1 changes

- Ports Timblee Pad's shared stacked-workspace startup fix: **Start a Document** and the editor/Library splitter now occupy one `QStackedWidget` slot. Persisted Inline/Split toolbar and Find-bar placement therefore behaves the same before and after a document is opened.
- The Start screen no longer force-hides either Find bar.
- Adds persistent **View → Dark Editor**, checked by default. Unticking it uses the existing light editor canvas and matching light JavaScript-family syntax/search/bracket palette. This setting is independent of AppImage **Dark Mode** chrome.
- Relabels the drag/drop submenu to **File Drag Drop → Opens on Active Window / Opens on New Window**.

---

# JSTS Pad 0.0.1-exp1

Initial experimental source release of **JSTS Pad**, a lightweight standalone editor for JavaScript, TypeScript, JSX and TSX.

## Scope

Supported source types:

- JavaScript: `.js`, `.mjs`, `.cjs`
- TypeScript: `.ts`, `.mts`, `.cts`
- JSX: `.jsx`
- TSX: `.tsx`

JSON is intentionally not part of this release.

## Editor

- Sheepy/Timblee-derived safe source editor foundation.
- JavaScript-family syntax highlighting without external parser/runtime dependencies.
- Bracket/brace/parenthesis matching.
- JSX/TSX tag-pair highlighting.
- Source-aware indentation.
- `Ctrl+/` Toggle Comment using `//`.
- Duplicate Line / Selection (`Ctrl+D`).
- Delete Line (`Ctrl+Shift+K`).
- Find/Replace, Go To Line, View Only, line numbers, word wrap and guarded drag/drop/save behavior.

## Document-type workflow

- No splash screen.
- File-less launch uses a **Start a Document** state inside the real main window when the preference is **Always Ask**.
- New documents choose JavaScript / TypeScript / JSX / TSX plus a template.
- A chosen type/template can become the default for future `Ctrl+N` and file-less launches.
- **File → New Type…** always opens the chooser.
- **File → Default New Document…** changes or resets the default to **Always Ask**.
- Current type is visible and switchable from the toolbar immediately after **Help**.
- Switching type changes interpretation/highlighting/Library/checking only; source text is never rewritten.
- Saved filename/type mismatch is warned before Save.

## Templates and Library

Factory templates are immutable and custom templates are editable. The Library follows the current language and contains focused reference/insertion snippets for declarations, functions, control flow, arrays/objects, classes, modules, async/errors, TypeScript types, JSX/TSX structures and custom entries. Both templates and snippets support `[[cursor]]`.

## Deliberate exclusions

JSTS Pad does not include or invoke:

- Node or npm;
- JavaScript/TypeScript execution;
- TypeScript compiler;
- ESLint/Prettier;
- debugger;
- language server/IntelliSense;
- embedded terminal;
- project/workspace/package management;
- Qt WebEngine;
- JSON editing profile.

This boundary is intentional: JSTS Pad is an editor, not an IDE.
