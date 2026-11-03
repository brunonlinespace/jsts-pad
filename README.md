<p align="center">
  <a href="https://github.com/brunonlinespace/jsts-pad">
    <img
      src="jsts_pad/assets/icons/jsts-pad-256.png"
      alt="JSTS Pad"
      width="256"
    >
  </a>
</p>

# JSTS Pad

**Friendly. Fast. Focused.**

JSTS Pad is a lightweight standalone source editor for the JavaScript family, built with Python and PyQt6. It focuses on direct editing of ordinary JavaScript, TypeScript, JSX and TSX files, with language-aware syntax colouring, code-oriented editing, reusable templates and a searchable insertion Library.

Current release: **0.1.3**

Repository: <https://github.com/brunonlinespace/jsts-pad>

## What JSTS Pad is

JSTS Pad is designed for people who want a focused desktop editor for JavaScript-family source without turning the editor into a runtime, package manager, debugger or project environment.

Supported filename extensions are:

- JavaScript: `.js`, `.mjs`, `.cjs`
- TypeScript: `.ts`, `.mts`, `.cts`
- JSX: `.jsx`
- TSX: `.tsx`

Documents remain ordinary source files on disk. JSTS Pad does not introduce a private document format or workspace database.

JSTS Pad deliberately stops at editing. It does **not** execute JavaScript or TypeScript, bundle Node or npm, run a compiler, provide a debugger or language server, perform automatic linting or structure validation, embed a terminal, or manage projects/workspaces.

## Highlights

- Dedicated **JavaScript, TypeScript, JSX and TSX** document profiles.
- Syntax highlighting with matching dark and light editor palettes.
- Explicit **Document Type** control, independent of the filename while editing.
- Extension-driven type selection when opening supported source files.
- Non-destructive document-type switching with a warning before saving when the selected type and filename extension differ.
- **Start a Document** workflow with document type and template selection.
- Configurable default new-document type/template, with **Always Ask** as the factory behavior.
- Immutable built-in templates plus editable custom templates.
- `[[cursor]]` support for deliberate caret placement in templates and snippets.
- Large searchable insertion **Library** with built-in catalogues for all four document types.
- Current resolved built-in Library coverage: **97 JavaScript**, **145 TypeScript**, **139 JSX**, and **213 TSX** entries.
- Persistent per-document-type **Favourites**, custom snippets and custom templates.
- Embedded Library as a **Left Sidebar** or **Right Sidebar**, or a separate **Floating Only** Library.
- Compact sidebar catalogue selector and full tabbed floating Library.
- **Comment** and **Duplicate** permanent code-editing shortcuts on the toolbar.
- Find, Replace, Go To Line, Duplicate Line / Selection, Delete Line and Toggle Comment.
- Line numbers, word wrap, current-line highlighting and bracket/tag matching.
- Four persistent toolbar/search layouts.
- **View Only** protection against accidental editing.
- Preservation of source encoding, BOM and predominant line endings.
- Stable file reads, bounded source size, guarded saves, no-clobber creation and external-change checks before overwrite.
- Safe Rename, Duplicate and Delete workflows with filesystem identity checks.
- Configurable file drag-and-drop behavior.
- Independent **Dark Editor** control plus AppImage-only dark/light application chrome.
- Keyboard Shortcuts dialog, bundled documentation, GitHub and issue links.

## Interface

JSTS Pad keeps its command structure intentionally compact:

**File · Edit · View · Library · Help**

### Main toolbar

The main toolbar provides the same five application menus as compact buttons:

- **File**
- **Edit**
- **View**
- **Library**
- **Help**

Two permanent code-editing shortcuts sit beside them:

- **Comment** — Toggle Comment (`Ctrl+/`)
- **Duplicate** — Duplicate Line / Selection (`Ctrl+D`)

**View → Menu Only** switches the File/Edit/View/Library/Help command surface to the native application menu bar while retaining the dedicated code-editing controls.

The toolbar and Find bar can be arranged in four persistent layouts:

- **Inline — Top**
- **Inline — Bottom**
- **Split — Toolbar Up / Search Down**
- **Split — Toolbar Down / Search Top**

The Start screen and active editor share the same workspace slot, so the selected layout is respected before and after a document is opened.

### Library placement

**View → Library** chooses:

- **Left Sidebar**
- **Right Sidebar**
- **Floating Only**

Embedded sidebars use a compact catalogue drop-down and a small **×** close control. The × only hides the current sidebar; it does not change the saved Left/Right placement. `Ctrl+L` restores or hides the selected Library presentation.

The embedded Library is hidden while **Start a Document** is active and returns automatically when a document becomes active.

The floating Library remains the full management surface, including custom snippet creation, editing, removal and management.

### Find bar

The Find bar is part of the selected interface layout rather than a separate dialog.

- Search is literal and case-insensitive by default.
- Matches are highlighted in the editor.
- Previous and Next navigation wraps through retained results.
- Up to **10,000** matches are retained/highlighted to keep extreme searches bounded.
- `Ctrl+F` focuses Find.
- `F3` and `Shift+F3` move through matches.
- `Esc` clears the current search.

On **Start a Document**, the configured Find bar remains visible in its selected position but is disabled until a document is active.

## Document types and templates

JSTS Pad treats the document type as an explicit editing interpretation.

Opening a supported file selects its type from the filename extension. The user can then change interpretation through **File → Document Type** without rewriting the source text.

If the chosen document type no longer matches the existing filename extension, Save warns before continuing. The user can:

- **Save Anyway** and retain the existing filename;
- use **Save As…** and choose a matching filename;
- cancel the save.

New documents use **Start a Document** when no default has been configured. Factory behavior is **Always Ask**.

Built-in templates include:

- Blank JavaScript
- JavaScript Module
- Browser Script
- Blank TypeScript
- TypeScript Module
- Blank JSX
- JSX Component
- Blank TSX
- TSX Component

Factory templates remain immutable. They can be duplicated into editable custom templates, and `[[cursor]]` marks where the caret should land after insertion.

## Editing

JSTS Pad's editor provides code-oriented operations without introducing an IDE runtime.

Editing features include:

- Undo / Redo
- Cut / Copy / Paste / Delete
- Toggle Comment
- Duplicate Line / Selection
- Delete Line
- Select All
- Go To Line
- Replace / Replace All
- Line numbers
- Word wrap
- Insert / Overwrite mode
- Current-line highlighting
- Bracket matching for JavaScript/TypeScript-style delimiters
- JSX/TSX named-tag matching

The editor uses document-type-aware syntax colouring for JavaScript, TypeScript, JSX and TSX.

Paste and document growth are bounded to protect the GUI from extremely large operations. Source files larger than **25 MiB** are not opened or saved.

## Library and snippets

The Library is JSTS Pad's main reusable-code surface.

It is language-aware: changing the active document type changes the available catalogue rather than mixing unrelated JavaScript, TypeScript, JSX and TSX entries together.

The built-in catalogues cover common patterns such as:

- declarations and functions;
- control flow;
- arrays and objects;
- classes and modules;
- async / Promise patterns;
- errors and JSON;
- browser DOM and events;
- TypeScript types, interfaces, generics, utility types and narrowing;
- JSX elements, props, conditional rendering, lists, forms and events;
- React hooks and common JSX patterns;
- typed TSX props, events, state, refs, contexts and component patterns.

The Library does not execute or validate inserted code. It is an insertion/reference aid only.

Each document type has its own Favourites. When at least one favourite exists for the active type, the Library opens on **Favourites**; otherwise it opens on **All**. Removing the final favourite while Favourites is selected falls back to All.

Custom snippets support bounded names, descriptions and content. The full custom-snippet management controls remain available in the floating Library and through the Library menu.

## Search and replace

Find is integrated into the main window and keeps the current query synchronized between Inline and Split layouts.

**Replace…** opens a separate modeless panel with:

- Replace
- Replace All
- Match case

Replace operations respect **View Only** and the editor's document-size safety limit.

## Source-file handling

JSTS Pad prefers UTF-8 and recognises BOM-marked:

- UTF-8
- UTF-16 LE / BE
- UTF-32 LE / BE

If a file is not UTF-8 and has no recognised BOM, JSTS Pad can ask the user to open it using:

- Windows-1252
- ISO-8859-1
- UTF-16 LE
- UTF-16 BE
- the system encoding

The detected encoding and BOM are preserved when saving. JSTS Pad also preserves the predominant original line-ending style:

- LF
- CRLF
- CR

If edited text cannot be represented in the file's existing encoding, saving is cancelled rather than silently replacing characters.

Binary-looking source is rejected rather than loaded as editable text.

## File safety and external changes

JSTS Pad treats file safety as part of normal source editing.

Reads capture stable filesystem identity and a SHA-256 digest of the exact source bytes. Saves use synchronized temporary files and re-check the expected path/file identity before replacement.

When the file on disk has changed since JSTS Pad opened or last saved it, Save offers an explicit choice instead of silently overwriting the external change:

- **Reload**
- **Save As…**
- **Overwrite**
- **Cancel**

New-file creation uses exclusive/no-clobber installation so a file that appears at the destination during the operation is not overwritten accidentally.

Symbolic-link saves verify that the link and target still identify the expected objects before replacement.

Rename and Delete re-check filesystem identity around confirmation/destructive steps. Duplicate writes the current editor contents through the same bounded, encoding-aware file path rather than treating the editor as disposable state.

## Drag and drop

JSTS Pad accepts supported local JavaScript-family source files dropped into the application.

**View → File Drag and Drop** chooses between:

- **Opens on Active Window**
- **Opens on New Window**

In active-window mode, the normal unsaved-changes workflow is respected before replacing the current document. Additional accepted files can open in separate JSTS Pad windows.

Unsupported extensions and invalid filesystem items are rejected rather than reinterpreted as generic text.

## View Only

**View Only** is a non-persistent protection state for the active document.

It disables mutating editor actions while preserving navigation and read-only operations such as Copy, Select All, Find and Go To Line. Disabling View Only requires confirmation so accidental edits are less likely.

On the no-document Start screen, the full Edit menu remains visible but disabled.

## Appearance

**Dark Editor** is enabled by default and controls only the source canvas plus its matching syntax, search, current-line and bracket/tag colours.

Turn Dark Editor off for the paired light editor canvas and syntax palette.

The editor palette is independent from application chrome.

The Linux AppImage additionally provides Breeze-inspired dark/light application styling through **View → Dark Mode**. One-launch AppImage theme overrides are also available:

```bash
./JSTS-Pad-0.1.3-x86_64.AppImage --appimage-theme=dark
./JSTS-Pad-0.1.3-x86_64.AppImage --appimage-theme=light
./JSTS-Pad-0.1.3-x86_64.AppImage --appimage-theme=system
```

Source/portable mode otherwise uses the normal host Qt appearance while retaining the independent Dark Editor choice.

## Useful keyboard shortcuts

| Shortcut | Action |
| --- | --- |
| `Ctrl+N` | New |
| `Ctrl+Shift+N` | New Window |
| `Ctrl+O` | Open… |
| `Ctrl+S` | Save |
| `Ctrl+Shift+S` | Save As… |
| `Ctrl+Shift+E` | Open in External Editor |
| `F2` | Rename… |
| `Ctrl+Shift+D` | Duplicate File |
| `Ctrl+Shift+O` | Open Containing Folder |
| `Ctrl+Q` | Exit |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |
| `Ctrl+X` | Cut |
| `Ctrl+C` | Copy |
| `Ctrl+V` | Paste |
| `Delete` | Delete |
| `Ctrl+/` | Toggle Comment |
| `Ctrl+D` | Duplicate Line / Selection |
| `Ctrl+Shift+K` | Delete Line |
| `Ctrl+A` | Select All |
| `Ctrl+F` | Find |
| `F3` / `Shift+F3` | Next / Previous Find result |
| `Esc` | Clear Find |
| `Ctrl+H` | Replace… |
| `Ctrl+G` | Go To Line… |
| `Ctrl+L` | Toggle selected Library presentation |
| `F1` | Documentation |

**Properties** and **Delete File** intentionally have no keyboard shortcut.

The complete shortcut inventory is available from **Help → Keyboard Shortcuts**.

## Running from source

JSTS Pad requires Python 3 and PyQt6 within the supported PyQt6 6.x series.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r jsts_pad/requirements.txt
python main.py
```

Other useful launch forms:

```bash
python main.py --version
python main.py source.js
python main.py component.tsx
python main.py one.js two.ts three.jsx
```

When multiple supported files are supplied, the first opens in the initial window and additional files open in separate JSTS Pad windows.

## Building the AppImage

The Fedora AppImage builder is included in the source tree:

```bash
./jsts_pad/packaging/fedora/build-appimage.sh
```

Expected outputs include:

```text
jsts_pad/dist/JSTS-Pad-0.1.3-x86_64.AppImage
jsts_pad/dist/JSTS-Pad-0.1.3-x86_64.AppImage.sha256
jsts_pad/dist/JSTS-Pad-0.1.3-x86_64.build-info.txt
jsts_pad/dist/JSTS-Pad-0.1.3-x86_64.build-python-lock.txt
```

The builder supports native `x86_64` and `aarch64` Fedora hosts and is validated for Fedora 43/44. Run it as the normal desktop user: it is deliberately non-privileged and reports missing host prerequisites instead of installing packages or invoking privilege elevation itself.

The build validates the Suite Pythoine component manifest, source manifest, packaged metadata and runtime identity, then performs GUI and version smoke tests for default, dark, light and system AppImage themes.

A completed AppImage can be rechecked with:

```bash
./jsts_pad/packaging/fedora/test-appimage.sh
```

## Validation

Run the bundled JSTS Pad QA gate from the portable source root:

```bash
bash jsts_pad/qa/run-qa.sh
```

The retained QA covers document profiles, templates, Library data, file I/O, runtime paths and launcher safety, packaging identity, official artwork, no-execution boundaries, shortcut/menu contracts, portable-tree policy and source-manifest integrity.

The AppImage builder adds final packaged-runtime GUI and version smoke tests.

## Configuration

JSTS Pad stores per-user preferences outside source documents.

Linux:

```text
~/.config/brunonlinespace/jsts-pad/jsts-pad.json
```

Windows:

```text
%APPDATA%/brunonlinespace/jsts-pad/jsts-pad.json
```

Preferences include interface layout, Library placement, drag-and-drop behavior, editor appearance/font choices, custom snippets, custom templates, favourites and new-document defaults.

JSTS Pad does not import another Pad application's preferences implicitly.

## Scope

JSTS Pad is a **standalone JavaScript-family source editor**.

Its goal is to make ordinary JavaScript, TypeScript, JSX and TSX source comfortable to create and edit while remaining deliberately smaller than an IDE.

The Library and templates help with writing; they do not claim to replace the user's compiler, linter, formatter, runtime, framework tooling or development environment.

JSTS Pad therefore deliberately excludes source execution, Node/npm management, embedded terminals, debugging, language-server features, automatic lint/structure checking, browser preview and project/workspace management.

## License

JSTS Pad is licensed under the **GNU General Public License v3.0 or later**.

See `jsts_pad/LICENSE` for the complete license text.

## Links

- JSTS Pad: <https://github.com/brunonlinespace/jsts-pad>
- Issues: <https://github.com/brunonlinespace/jsts-pad/issues>
- GitHub profile: <https://github.com/brunonlinespace/>

Copyright © 2026 Bruno Machado.
