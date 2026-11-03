# Source lineage / porting notes

JSTS Pad is a standalone application, not a runtime-dependent skin of another Pad.

The first experimental source intentionally combines two proven lines of Pad-family work:

- **Sheepy-derived strengths:** hardened source-code editor behavior, line/search/bracket mechanics, View Only, safe paste/file limits, code-oriented indentation/comment/line operations and guarded file actions.
- **Timblee-derived strengths:** explicit document-language profiles, file-less Start a Document workflow, configurable default type/template, editable templates, language-aware Library/favourites/custom snippets and non-destructive type switching.

JSTS-specific code then specializes those generic ideas for JavaScript, TypeScript, JSX and TSX.

No shared runtime `pad_common` dependency is introduced; JSTS Pad remains self-contained.
