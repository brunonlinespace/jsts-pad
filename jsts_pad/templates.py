# JSTS Pad
# Copyright (C) 2026 Bruno Machado
# SPDX-License-Identifier: GPL-3.0-or-later
"""Built-in and user-editable JSTS document templates."""

from __future__ import annotations

from dataclasses import dataclass

CURSOR_MARKER = "[[cursor]]"
MAX_CUSTOM_TEMPLATES = 64
MAX_TEMPLATE_NAME = 96
MAX_TEMPLATE_CHARACTERS = 100_000
LANGUAGES = frozenset({"javascript", "typescript", "jsx", "tsx"})


@dataclass(frozen=True, slots=True)
class TemplateSpec:
    template_id: str
    language: str
    name: str
    content: str
    builtin: bool = True


BUILTIN_TEMPLATES: tuple[TemplateSpec, ...] = (
    TemplateSpec("javascript:blank", "javascript", "Blank JavaScript", ""),
    TemplateSpec(
        "javascript:module",
        "javascript",
        "JavaScript Module",
        """export function main() {\n    [[cursor]]\n}\n""",
    ),
    TemplateSpec(
        "javascript:browser",
        "javascript",
        "Browser Script",
        """document.addEventListener("DOMContentLoaded", () => {\n    [[cursor]]\n});\n""",
    ),
    TemplateSpec("typescript:blank", "typescript", "Blank TypeScript", ""),
    TemplateSpec(
        "typescript:module",
        "typescript",
        "TypeScript Module",
        """export function main(): void {\n    [[cursor]]\n}\n""",
    ),
    TemplateSpec("jsx:blank", "jsx", "Blank JSX", ""),
    TemplateSpec(
        "jsx:component",
        "jsx",
        "JSX Component",
        """export default function Component() {\n    return (\n        <div>[[cursor]]</div>\n    );\n}\n""",
    ),
    TemplateSpec("tsx:blank", "tsx", "Blank TSX", ""),
    TemplateSpec(
        "tsx:component",
        "tsx",
        "TSX Component",
        """interface Props {\n    title: string;\n}\n\nexport default function Component({ title }: Props) {\n    return (\n        <div>{title}[[cursor]]</div>\n    );\n}\n""",
    ),
)

BUILTIN_TEMPLATE_BY_ID = {spec.template_id: spec for spec in BUILTIN_TEMPLATES}


def default_template_id(language: str) -> str:
    # JSTS deliberately defaults each chosen language to a blank source file;
    # richer factory templates remain one selection away in the New dialog.
    return f"{language}:blank" if language in LANGUAGES else "javascript:blank"


def normalise_custom_templates(raw: object) -> list[TemplateSpec]:
    """Validate config JSON and return bounded custom templates."""
    if not isinstance(raw, list):
        return []
    result: list[TemplateSpec] = []
    seen: set[str] = set()
    for item in raw[:MAX_CUSTOM_TEMPLATES]:
        if not isinstance(item, dict):
            continue
        template_id = item.get("id")
        language = item.get("language")
        name = item.get("name")
        content = item.get("content")
        if (
            not isinstance(template_id, str)
            or not template_id.startswith("user:")
            or len(template_id) > 160
            or template_id in seen
            or language not in LANGUAGES
            or not isinstance(name, str)
            or not name.strip()
            or len(name) > MAX_TEMPLATE_NAME
            or not isinstance(content, str)
            or len(content) > MAX_TEMPLATE_CHARACTERS
        ):
            continue
        seen.add(template_id)
        result.append(
            TemplateSpec(template_id, str(language), name.strip(), content, builtin=False)
        )
    return result


def serialise_custom_templates(templates: list[TemplateSpec]) -> list[dict[str, str]]:
    return [
        {
            "id": spec.template_id,
            "language": spec.language,
            "name": spec.name,
            "content": spec.content,
        }
        for spec in templates
        if not spec.builtin
    ]
