## 0.1.3 README filename contract acceptance

- Source root must contain `README.md` and must not contain extensionless `README`.
- AppImage builder must require `${PROJECT_ROOT}/README.md`.
- Locked public README must differ from 0.1.2 only by version-number substitutions.
- 0.1.2 EOF scrolling regression remains green.

## 0.1.2 editor scrolling acceptance

- Open a short document with many empty viewport rows, move to the final line and scroll. Confirm the final lines remain naturally near the bottom and the former excessive blank scroll region below EOF is gone.
- Use Go To Line and confirm the destination line is still explicitly centered.
- Confirm no unrelated gutter/layout behavior changed.

## 0.1.1 publication/package-contract acceptance

- Confirm source root contains exactly `README`, `main.py`, `suite-pythoine-component.json`, and `jsts_pad/`.
- Confirm root `README` is the approved public README with only the release version advanced to 0.1.1.
- Confirm the Fedora AppImage builder requires root `README` and records its SHA-256 in build provenance.
- Confirm application behavior remains identical to 0.1.0.

## 0.1.0 packaging acceptance

- Confirm Suite Pythoine identifies JSTS Pad as editor `jsts-pad`, version `0.1.0`, with `.js`, `.mjs`, `.cjs`, `.ts`, `.mts`, `.cts`, `.jsx` and `.tsx` routing.
- Build through `jsts_pad/packaging/fedora/build-appimage.sh` and confirm AppDir plus final-AppImage default/dark/light/system GUI and version smoke tests pass.
- Confirm About displays **Friendly. Fast. Focused.**
- Confirm editor, Library, document, theme, shortcut and workflow behavior matches `0.0.1-exp1-r9`.

## 0.0.1-exp1-r9 focused GUI regression

- With favourites for the active document type, open Library and confirm Favourites is selected by default.
- With no favourites for the active document type, open Library and confirm All is selected by default.
- Confirm the behavior in both sidebar and floating Library modes and after changing document type.
- Remove the final favourite while Favourites is selected and confirm Library falls back to All.

## 0.0.1-exp1-r8 focused GUI regression

- Select View → Library → Left Sidebar, click the sidebar `×`, and confirm the sidebar closes without changing the checked placement to Floating Only.
- Press `Ctrl+L` and confirm the same Left Sidebar returns. Repeat for Right Sidebar.
- Confirm Floating Only behavior remains unchanged.

## 0.0.1-exp1-r7 focused GUI regression

- Confirm **Open in External Editor** uses `Ctrl+Shift+E`.
- Confirm **Properties** has no keyboard shortcut and is absent from the Keyboard Shortcuts listing.

## 0.0.1-exp1-r6 focused GUI regression

- Confirm embedded Left/Right Library sidebar mode omits the lower custom snippet management buttons.
- Confirm Floating Library still shows Add/Edit/Remove/Manage custom snippet controls.

# JSTS Pad QA

## Automated

From the portable source root:

```bash
bash jsts_pad/qa/run-qa.sh
```

The dependency-free suite covers document profiles, templates, Library data, file I/O, runtime paths/launcher safety, packaging identity, official artwork, no-execution boundaries, portable-tree policy and release metadata.

## Fedora GUI acceptance checklist

1. Start JSTS Pad with no file and fresh preferences. Confirm the **real main window** shows **Start a Document** and no splash/dialog can be dismissed into an untyped editor.
2. Confirm factory behavior is **Always Ask**.
3. Create JavaScript, TypeScript, JSX and TSX documents; confirm title, template, syntax colour and Library follow the selected type.
4. Check **Use this type and template as my default**, restart, and confirm file-less launch directly creates that selection.
5. Use **File → Default New Document… → Always Ask**, restart, and confirm Start a Document returns.
6. Confirm `Ctrl+N` uses the configured default or opens the New chooser when set to Always Ask; **File → New Type…** always asks.
7. Open `.js`, `.mjs`, `.cjs`, `.ts`, `.mts`, `.cts`, `.jsx`, `.tsx`; confirm extension-driven type selection.
8. Switch type with **File → Document Type**. Confirm source text is unchanged and only interpretation changes; confirm there is no permanent Document Type toolbar shortcut.
9. Switch a saved `.js` to TypeScript and press Save. Confirm the mismatch warning offers Save Anyway / Save As… / Cancel.
10. Verify JavaScript/TypeScript brace/bracket/parenthesis matching and JSX/TSX named-tag matching.
11. Verify `Ctrl+/`, `Ctrl+D`, `Ctrl+Shift+K`, Find/Replace and Go To Line.
12. Exercise the Library for each type; add/edit/remove a custom snippet; favourites survive restart.
13. Duplicate & Edit a factory template, include `[[cursor]]`, create from it, and verify caret placement. Factory template remains unchanged.
14. Confirm JSTS Pad does not display automatic structure/type/lint results in the status bar or Properties and does not silently inspect content to guess another type.
15. Confirm there is no Run/Launch JavaScript action, Node/npm control, embedded terminal, debugger, project manager or browser preview.
16. Confirm toolbar order begins **File / Edit / View / Library / Help** with no permanent Document Type button.
17. Confirm View Only blocks editing and its first blocked edit explains how to disable protection.
18. Exercise external-change protection, rename/duplicate/delete, drag/drop and 25 MiB file/paste safety paths.
19. On AppImage, verify System/Dark/Light chrome modes and the official transparent JSTS artwork.
## 0.0.1-exp1-r1 focused GUI regression

21. With **Always Ask** enabled, select each of the four **View → Layout** modes, restart with no file, and confirm the initial **Start a Document** screen preserves the exact toolbar/Find-bar ordering. Inline modes keep Find inline; split modes show the dedicated Find bar on the chosen top/bottom side.
22. On the no-document Start screen, switch between all four layouts without opening a file and confirm the Find bar never disappears or drops below the requested side.
23. Create/open a document after each Start-screen layout and confirm the same ordering is retained when the workspace switches from Start to editor/Library.
24. Confirm **View → Dark Editor** is checked by default with fresh preferences. Untick it and verify the editor canvas, gutter, syntax colours, search highlights, current-line and bracket colours switch to the paired light palette; restart and confirm persistence.
25. In an AppImage, toggle **Dark Mode** independently from **Dark Editor** in all four combinations and confirm chrome changes do not override the editor choice.
26. Confirm **View → File Drag and Drop** contains exactly **Opens on Active Window** and **Opens on New Window**, and both retain their existing drag/drop behavior and persistence.


## 0.0.1-exp1-r2 focused GUI regression

27. Launch with **Always Ask** and no document. In each of the four Layout modes, confirm the configured Find bar is still visible in its correct inline/top/bottom position but all Find controls are disabled/greyed.
28. Create or open a document and confirm the visible Find bar immediately becomes enabled without changing layout. Return to the no-document Start state through a file-removal path and confirm it becomes disabled again.
29. Confirm the View submenu is labelled exactly **File Drag and Drop**, with **Opens on Active Window** and **Opens on New Window** unchanged.
30. On **Start a Document**, open **Edit** and confirm every command is visible but disabled/greyed. Create or open a document and confirm the commands become available again; enable **View Only** and confirm only mutating Edit commands are disabled while Copy, Select All and Go To Line remain usable.


## 0.0.1-exp1-r4 focused GUI regression

31. With **View → Library → Left Sidebar**, open a document and confirm the embedded Library uses a catalogue drop-down rather than tabs and has a small **×** close button. Click × and confirm the View choice becomes **Floating Only**. Repeat on the right.
32. Open **Library → Library...** and confirm the floating Library still uses tabs.
33. In **Split — Toolbar Up / Search Down**, verify the toolbar spans the whole window, the left/right Library sidebar spans the full workspace height, and Find appears only below the editor column.
34. In **Split — Toolbar Down / Search Top**, verify Find appears only above the editor column, the left/right Library sidebar spans the full workspace height, and the toolbar spans the whole window at the bottom.
35. Return to **Start a Document** with a saved Left or Right Library preference. Confirm the Library is hidden, the Find bar remains visible-but-disabled in the selected layout, and opening/creating a document restores the saved sidebar automatically.
36. Confirm the status bar has no **Structure OK**, structure warning, type-content hint, or other automatic checker field; Properties likewise has no document-check row.

## 0.0.1-exp1-r5 focused GUI regression

37. Confirm the toolbar contains exactly the new code shortcuts **Comment** and **Duplicate** after the menu controls, with no Document Type shortcut restored. On **Start a Document**, both are disabled because their backing Edit actions are disabled; they enable with an editable document and follow View Only state.
38. For JavaScript, TypeScript, JSX and TSX, open the Library and confirm the previous built-ins still exist. Spot-check new entries such as `console.log`, `Promise.all()`, `Object.entries()`, `Partial`, `satisfies`, `type guard`, `useState`, controlled input, typed mouse event and typed `useState`.
39. Select **View → Library → Left Sidebar**. Press `Ctrl+L` repeatedly and confirm the left sidebar hides/shows without changing the checked Left Sidebar preference. Repeat with Right Sidebar. Confirm Start a Document still suppresses the embedded sidebar.
40. Select **Floating Only**. Press `Ctrl+L` and confirm the floating Library opens; press it again and confirm the floating Library closes.
41. Confirm **Delete File** has no keyboard shortcut. Verify **Properties** `Alt+Enter`, **Open in External Editor** `Ctrl+Alt+O`, **Rename** `F2`, **Duplicate File** `Ctrl+Shift+D`, and **Open Containing Folder** `Ctrl+Shift+O`; confirm the Keyboard Shortcuts dialog shows the same mappings.

