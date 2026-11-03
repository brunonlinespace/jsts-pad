# JSTS Pad

JSTS Pad is a lightweight, source-only PyQt6 editor for the JavaScript family:

- JavaScript: `.js`, `.mjs`, `.cjs`
- TypeScript: `.ts`, `.mts`, `.cts`
- JSX: `.jsx`
- TSX: `.tsx`

Version: **0.1.3**

JSTS Pad deliberately stops at editing. It does **not** execute source, bundle Node or npm, provide a debugger, language server, package manager, embedded terminal, project/workspace system, or Qt WebEngine.

## Editing model

The editor combines proven Pad-family source-editing mechanics with the newer language-profile workflow developed for Timblee Pad:

- line numbers, current-line highlighting and bracket matching;
- Find/Replace, Go To Line, Duplicate Line / Selection, Delete Line and Toggle Comment;
- View Only protection and guarded large-file/paste handling;
- JavaScript/TypeScript/JSX/TSX syntax highlighting;
- explicit document type, independent of the filename while editing;
- non-destructive type switching;
- extension/type mismatch warning before Save;
- a searchable, language-aware insertion Library with a broad built-in JS/TS/JSX/TSX catalogue;
- editable custom snippets and favourites;
- immutable factory templates plus Duplicate & Edit custom templates;
- `[[cursor]]` template/snippet marker;

## Starting a document

There is no splash screen. With no file and no configured default, the real JSTS Pad window opens to **Start a Document**, where the user chooses a document type and template or opens an existing file.

The factory preference is **Always Ask**. A user can set a default type/template from the startup chooser or **File → Default New Document…**. `Ctrl+N` then uses the configured default; **File → New Type…** always opens the chooser.

The Start state shares the same workspace slot as the editor, so **View → Layout** is honoured before a document is opened as well as afterward. The selected Find bar remains visible but disabled until a document is active. **View → Dark Editor** is enabled by default and independently controls only the editor canvas plus its matching syntax/search/bracket palette. On the Start screen, all **Edit** menu commands also remain visible but disabled until a document is active.

The embedded Library is hidden on the Start screen. With a document active, **View → Library** can place it left or right; embedded sidebars use a compact catalogue drop-down and × close control, while the floating Library remains tabbed. `Ctrl+L` toggles whichever Library presentation the user selected without changing a Left/Right placement preference. In Split layouts the Find bar is confined to the editor column so the selected Library sidebar spans the full workspace height. Document type remains available from **File → Document Type** rather than as a permanent toolbar shortcut. The permanent toolbar keeps only the code-editing shortcuts **Comment** and **Duplicate**. JSTS Pad performs no automatic syntax/structure/lint check; validation is deliberately the user/toolchain responsibility.

## Current file/Library shortcuts

- `Ctrl+Shift+E` — Open in External Editor
- `F2` — Rename file
- Delete File — no keybinding
- `Ctrl+Shift+D` — Duplicate File
- `Ctrl+Shift+O` — Open Containing Folder
- `Ctrl+L` — toggle the selected Library presentation

## Source tree

The portable source archive intentionally has only three items at its outer root:

```text
main.py
suite-pythoine-component.json
jsts_pad/
```

Run from source with:

```bash
python3 main.py
```

Version probe:

```bash
python3 main.py --version
```

## Preferences

Linux:

```text
~/.config/brunonlinespace/jsts-pad/jsts-pad.json
```

Windows:

```text
%APPDATA%/brunonlinespace/jsts-pad/jsts-pad.json
```

JSTS Pad does not import another Pad's preferences.

## License

GNU General Public License v3 or later. See `LICENSE`.
