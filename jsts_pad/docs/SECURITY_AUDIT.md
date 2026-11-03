# Security / safety audit notes

JSTS Pad 0.0.1-exp1 intentionally minimizes execution surface.

- Source files are edited as text and are never executed by JSTS Pad.
- No Node, npm, TypeScript compiler, shell command runner, embedded terminal, debugger, language server or WebEngine is bundled.
- External opening uses argument-safe process launching rather than shell command strings.
- File opening is bounded to 25 MiB and rejects unsupported extensions through the normal UI/CLI routes.
- Large paste/document growth is bounded by the editor.
- Saves use current-file state checks and guarded replacement to reduce accidental overwrite after external changes.
- Symlink/file-state handling is inherited from the hardened Pad-family file I/O layer.
- Custom templates and Library snippets are bounded preference text; they are inserted, not executed.
- The AppImage builder is non-privileged and refuses ordinary root builds unless explicitly overridden for controlled testing.
- PyInstaller excludes unused Qt PDF, PrintSupport and WebEngine modules.

This is an experimental source release and still requires live GUI testing on the supported Fedora environments before promotion.
