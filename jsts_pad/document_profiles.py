# JSTS Pad
# Copyright (C) 2026 Bruno Machado
# SPDX-License-Identifier: GPL-3.0-or-later
"""Lightweight document-language profiles for JSTS Pad."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class DocumentProfile:
    key: str
    label: str
    short_label: str
    extensions: tuple[str, ...]
    default_extension: str
    editor_language: str
    description: str


DOCUMENT_PROFILES: dict[str, DocumentProfile] = {
    "javascript": DocumentProfile(
        "javascript",
        "JavaScript",
        "JS",
        (".js", ".mjs", ".cjs"),
        ".js",
        "javascript",
        "JavaScript source file",
    ),
    "typescript": DocumentProfile(
        "typescript",
        "TypeScript",
        "TS",
        (".ts", ".mts", ".cts"),
        ".ts",
        "typescript",
        "TypeScript source file",
    ),
    "jsx": DocumentProfile(
        "jsx",
        "JSX",
        "JSX",
        (".jsx",),
        ".jsx",
        "jsx",
        "JavaScript with JSX syntax",
    ),
    "tsx": DocumentProfile(
        "tsx",
        "TSX",
        "TSX",
        (".tsx",),
        ".tsx",
        "tsx",
        "TypeScript with JSX syntax",
    ),
}

DOCUMENT_TYPE_ORDER = ("javascript", "typescript", "jsx", "tsx")
SUPPORTED_SOURCE_SUFFIXES = frozenset(
    suffix
    for key in DOCUMENT_TYPE_ORDER
    for suffix in DOCUMENT_PROFILES[key].extensions
)

SOURCE_FILE_FILTER = (
    "JSTS Source Files (*.js *.mjs *.cjs *.ts *.mts *.cts *.jsx *.tsx);;"
    "JavaScript Files (*.js *.mjs *.cjs);;"
    "TypeScript Files (*.ts *.mts *.cts);;"
    "JSX Files (*.jsx);;TSX Files (*.tsx);;All Files (*)"
)


def profile_for_key(key: str) -> DocumentProfile:
    return DOCUMENT_PROFILES.get(key, DOCUMENT_PROFILES["javascript"])


def document_type_for_suffix(suffix: str) -> str | None:
    folded = (suffix or "").casefold()
    for key in DOCUMENT_TYPE_ORDER:
        if folded in DOCUMENT_PROFILES[key].extensions:
            return key
    return None


def document_type_for_path(path: str | Path) -> str | None:
    return document_type_for_suffix(Path(path).suffix)


def extension_matches_type(path: str | Path, document_type: str) -> bool:
    return Path(path).suffix.casefold() in profile_for_key(document_type).extensions
