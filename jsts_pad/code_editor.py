# JSTS Pad
# Copyright (C) 2026 Bruno Machado
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
"""JSTS Pad source editor.

The editor keeps Sheepy Pad's hardened source-editing mechanics and Timblee
Pad's later language-profile/document-safety improvements, specialized for
JavaScript, TypeScript, JSX and TSX. It deliberately does not execute code.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from PyQt6.QtCore import QMimeData, QRect, QSize, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import (
    QColor,
    QFont,
    QFontDatabase,
    QInputMethodEvent,
    QKeyEvent,
    QKeySequence,
    QPainter,
    QTextCharFormat,
    QTextCursor,
    QSyntaxHighlighter,
    QTextDocument,
)
from PyQt6.QtWidgets import QPlainTextEdit, QTextEdit, QWidget


@dataclass(frozen=True, slots=True)
class HighlightRule:
    pattern: re.Pattern[str]
    text_format: QTextCharFormat


EDITOR_COLOR_SCHEMES: dict[str, dict[str, str]] = {
    "dark": {
        "background": "#1e1e1e",
        "foreground": "#d4d4d4",
        "border": "#3f3f46",
        "selection_background": "#264f78",
        "selection_foreground": "#ffffff",
        "gutter_background": "#181818",
        "gutter_current": "#c6c6c6",
        "gutter_foreground": "#858585",
        "current_line": "#2a2d2e",
        "bracket_background": "#3b514d",
        "bracket_foreground": "#ffffff",
        "search_current_background": "#d7ba7d",
        "search_current_foreground": "#1e1e1e",
        "search_background": "#5a4a00",
        "search_foreground": "#ffffff",
        "keyword": "#c586c0",
        "type": "#4ec9b0",
        "function": "#dcdcaa",
        "builtin": "#4fc1ff",
        "string": "#ce9178",
        "number": "#b5cea8",
        "comment": "#6a9955",
        "regex": "#d16969",
        "jsx_tag": "#569cd6",
        "jsx_attribute": "#9cdcfe",
    },
    "light": {
        "background": "#ffffff",
        "foreground": "#202124",
        "border": "#aeb4ba",
        "selection_background": "#b8d7f0",
        "selection_foreground": "#101214",
        "gutter_background": "#f0f2f4",
        "gutter_current": "#202124",
        "gutter_foreground": "#687078",
        "current_line": "#eef5fb",
        "bracket_background": "#c8e6c9",
        "bracket_foreground": "#16351b",
        "search_current_background": "#f4c95d",
        "search_current_foreground": "#202124",
        "search_background": "#fff1a8",
        "search_foreground": "#202124",
        "keyword": "#7b2f91",
        "type": "#267f99",
        "function": "#795e26",
        "builtin": "#005a9c",
        "string": "#a31515",
        "number": "#805000",
        "comment": "#2e7d32",
        "regex": "#a31515",
        "jsx_tag": "#005a9c",
        "jsx_attribute": "#7b2f91",
    },
}


def _normalise_color_scheme(name: str) -> str:
    return "light" if name == "light" else "dark"


class SourceHighlighter(QSyntaxHighlighter):
    @staticmethod
    def _format(color: str, *, bold: bool = False, italic: bool = False) -> QTextCharFormat:
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        fmt.setFontWeight(QFont.Weight.Bold if bold else QFont.Weight.Normal)
        fmt.setFontItalic(italic)
        return fmt


class ECMAScriptHighlighter(SourceHighlighter):
    """Dependency-free JavaScript/TypeScript/JSX/TSX syntax highlighter."""

    NORMAL = 0
    BLOCK_COMMENT = 1
    TEMPLATE = 2

    JS_KEYWORDS = frozenset(
        "as async await break case catch class const continue debugger default delete do else export extends finally for from function get if import in instanceof let new of return set static super switch this throw try typeof var void while with yield true false null undefined".split()
    )
    TS_KEYWORDS = frozenset(
        "abstract any assert asserts bigint boolean constructor declare enum global implements infer interface intrinsic is keyof module namespace never object override private protected public readonly require satisfies string symbol type unknown using number void".split()
    )
    BUILTINS = frozenset(
        "Array BigInt Boolean Date Error JSON Map Math Number Object Promise RegExp Set String Symbol WeakMap WeakSet console document window globalThis fetch URL URLSearchParams".split()
    )

    def __init__(self, document: QTextDocument, language: str = "javascript", color_scheme: str = "dark") -> None:
        super().__init__(document)
        self.language = language if language in {"javascript", "typescript", "jsx", "tsx"} else "javascript"
        colors = EDITOR_COLOR_SCHEMES[_normalise_color_scheme(color_scheme)]
        self.keyword_format = self._format(colors["keyword"], bold=True)
        self.type_format = self._format(colors["type"])
        self.function_format = self._format(colors["function"])
        self.builtin_format = self._format(colors["builtin"])
        self.string_format = self._format(colors["string"])
        self.number_format = self._format(colors["number"])
        self.comment_format = self._format(colors["comment"], italic=True)
        self.regex_format = self._format(colors["regex"])
        self.jsx_tag_format = self._format(colors["jsx_tag"], bold=True)
        self.jsx_attribute_format = self._format(colors["jsx_attribute"])

    def _highlight_code(self, text: str, offset: int = 0) -> None:
        keywords = set(self.JS_KEYWORDS)
        if self.language in {"typescript", "tsx"}:
            keywords.update(self.TS_KEYWORDS)
        for match in re.finditer(r"\b[A-Za-z_$][\w$]*\b", text):
            word = match.group()
            if word in keywords:
                self.setFormat(offset + match.start(), len(word), self.keyword_format)
            elif word in self.BUILTINS:
                self.setFormat(offset + match.start(), len(word), self.builtin_format)
        for match in re.finditer(r"\b(?:0[xX][0-9A-Fa-f]+|0[bB][01]+|0[oO][0-7]+|\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)n?\b", text):
            self.setFormat(offset + match.start(), len(match.group()), self.number_format)
        for match in re.finditer(r"\b([A-Za-z_$][\w$]*)\s*(?=\()", text):
            self.setFormat(offset + match.start(1), len(match.group(1)), self.function_format)
        if self.language in {"typescript", "tsx"}:
            for match in re.finditer(r"(?<=:\s)([A-Za-z_$][\w$]*(?:<[^>\n]+>)?(?:\[\])?)", text):
                self.setFormat(offset + match.start(1), len(match.group(1)), self.type_format)
            for match in re.finditer(r"\b(?:interface|type|enum|class)\s+([A-Za-z_$][\w$]*)", text):
                self.setFormat(offset + match.start(1), len(match.group(1)), self.type_format)
        if self.language in {"jsx", "tsx"}:
            for match in re.finditer(r"</?\s*([A-Za-z_$][\w$.-]*(?:\.[A-Za-z_$][\w$-]*)*)", text):
                self.setFormat(offset + match.start(1), len(match.group(1)), self.jsx_tag_format)
            for match in re.finditer(r"\s([A-Za-z_$][\w$:-]*)(?=\s*=|\s|/?>)", text):
                self.setFormat(offset + match.start(1), len(match.group(1)), self.jsx_attribute_format)
        # Conservative regex-literal colouring; division remains untouched when
        # the token is not in an expression-start context.
        for match in re.finditer(r"(?:(?<=^)|(?<=[(=,:;!&|?{}\[]))\s*(/)(?![/*])(?:\\.|[^/\n\\])+/[dgimsuvy]*", text):
            slash = match.start(1)
            self.setFormat(offset + slash, match.end() - slash, self.regex_format)

    def _highlight_strings(self, text: str, offset: int = 0) -> None:
        for match in re.finditer(r"'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"", text):
            self.setFormat(offset + match.start(), len(match.group()), self.string_format)
        for match in re.finditer(r"//.*$", text):
            self.setFormat(offset + match.start(), len(match.group()), self.comment_format)

    def highlightBlock(self, text: str) -> None:  # noqa: N802 - Qt API name
        previous = self.previousBlockState()
        self.setCurrentBlockState(self.NORMAL)
        cursor = 0

        if previous == self.BLOCK_COMMENT:
            end = text.find("*/")
            if end < 0:
                self.setFormat(0, len(text), self.comment_format)
                self.setCurrentBlockState(self.BLOCK_COMMENT)
                return
            self.setFormat(0, end + 2, self.comment_format)
            cursor = end + 2
        elif previous == self.TEMPLATE:
            end = self._find_unescaped(text, "`", 0)
            if end < 0:
                self.setFormat(0, len(text), self.string_format)
                self.setCurrentBlockState(self.TEMPLATE)
                return
            self.setFormat(0, end + 1, self.string_format)
            cursor = end + 1

        while cursor < len(text):
            block = text.find("/*", cursor)
            template = self._find_unescaped(text, "`", cursor)
            candidates = [(p, k) for p, k in ((block, "comment"), (template, "template")) if p >= 0]
            next_special = min(candidates) if candidates else None
            segment_end = next_special[0] if next_special else len(text)
            segment = text[cursor:segment_end]
            self._highlight_code(segment, cursor)
            self._highlight_strings(segment, cursor)
            if next_special is None:
                break
            pos, kind = next_special
            if kind == "comment":
                end = text.find("*/", pos + 2)
                if end < 0:
                    self.setFormat(pos, len(text) - pos, self.comment_format)
                    self.setCurrentBlockState(self.BLOCK_COMMENT)
                    return
                self.setFormat(pos, end + 2 - pos, self.comment_format)
                cursor = end + 2
            else:
                end = self._find_unescaped(text, "`", pos + 1)
                if end < 0:
                    self.setFormat(pos, len(text) - pos, self.string_format)
                    self.setCurrentBlockState(self.TEMPLATE)
                    return
                self.setFormat(pos, end + 1 - pos, self.string_format)
                cursor = end + 1

    @staticmethod
    def _find_unescaped(text: str, character: str, start: int) -> int:
        index = text.find(character, start)
        while index >= 0:
            backslashes = 0
            probe = index - 1
            while probe >= 0 and text[probe] == "\\":
                backslashes += 1
                probe -= 1
            if backslashes % 2 == 0:
                return index
            index = text.find(character, index + 1)
        return -1


class LineNumberArea(QWidget):
    """Narrow child widget that paints visible line numbers."""

    def __init__(self, editor: "CodeEditor") -> None:
        super().__init__(editor)
        self._editor = editor

    def sizeHint(self) -> QSize:  # noqa: N802 - Qt API name
        return QSize(self._editor.line_number_area_width(), 0)

    def paintEvent(self, event) -> None:  # noqa: N802 - Qt API name
        self._editor.paint_line_number_area(event)


class CodeEditor(QPlainTextEdit):
    """Reusable source-code editor for JavaScript, TypeScript, JSX and TSX files."""

    go_to_line_requested = pyqtSignal()
    paste_rejected = pyqtSignal(str)
    view_only_edit_attempt = pyqtSignal()
    overwrite_mode_changed = pyqtSignal(bool)
    files_dropped = pyqtSignal(list)

    BRACKET_PAIRS = {
        "(": ")",
        "[": "]",
        "{": "}",
        ")": "(",
        "]": "[",
        "}": "{",
    }

    OPENING_BRACKETS = "([{"
    CLOSING_BRACKETS = ")] }".replace(" ", "")
    MAX_PASTE_CHARACTERS = 5_000_000
    MAX_DOCUMENT_CHARACTERS = 25_000_000
    MAX_BRACKET_SCAN_CHARACTERS = 250_000

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._line_number_area = LineNumberArea(self)
        self._language = "javascript"
        self._color_scheme = "dark"
        self._highlighter: QSyntaxHighlighter = ECMAScriptHighlighter(
            self.document(), self._language, self._color_scheme
        )
        self._tab_width_spaces = 4
        self._line_numbers_visible = True
        self._search_selections: list[QTextEdit.ExtraSelection] = []
        self._refreshing_extra_selections = False
        self._pending_full_paste: str | None = None
        self._full_paste_generation = 0

        fixed_font = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
        fixed_font.setPointSize(10)
        self.setFont(fixed_font)

        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setTabStopDistance(
            self.fontMetrics().horizontalAdvance(" ") * self._tab_width_spaces
        )
        self.setUndoRedoEnabled(True)
        self.setCenterOnScroll(False)

        self._decoration_timer = QTimer(self)
        self._decoration_timer.setSingleShot(True)
        self._decoration_timer.setInterval(0)
        self._decoration_timer.timeout.connect(self._refresh_extra_selections)

        self.blockCountChanged.connect(self._update_line_number_area_width)
        self.updateRequest.connect(self._update_line_number_area)
        self.cursorPositionChanged.connect(self._schedule_decoration_refresh)
        self.textChanged.connect(self._schedule_decoration_refresh)

        self._update_line_number_area_width()
        self._schedule_decoration_refresh()

        self._apply_color_scheme()

    def set_source_language(self, language: str) -> None:
        """Switch syntax colouring and language-aware indentation."""
        selected = language if language in {"javascript", "typescript", "jsx", "tsx"} else "javascript"
        if selected == self._language:
            return
        self._language = selected
        self._replace_highlighter()
        self._schedule_decoration_refresh()

    @property
    def source_language(self) -> str:
        return self._language

    def set_color_scheme(self, color_scheme: str) -> None:
        """Apply a complete dark or light editor and syntax palette."""
        selected = _normalise_color_scheme(color_scheme)
        if selected == self._color_scheme:
            self._apply_color_scheme()
            return
        self._color_scheme = selected
        self._replace_highlighter()
        self._apply_color_scheme()

    @property
    def color_scheme(self) -> str:
        """Return the active editor colour scheme."""
        return self._color_scheme

    def search_highlight_colors(self) -> tuple[str, str, str, str]:
        """Return current-match and ordinary-match colours for the scheme."""
        colors = EDITOR_COLOR_SCHEMES[self._color_scheme]
        return (
            colors["search_current_background"],
            colors["search_current_foreground"],
            colors["search_background"],
            colors["search_foreground"],
        )

    def _replace_highlighter(self) -> None:
        old_highlighter = self._highlighter
        old_highlighter.setDocument(None)
        self._highlighter = ECMAScriptHighlighter(
            self.document(), self._language, self._color_scheme
        )
        old_highlighter.deleteLater()
        self._schedule_decoration_refresh()

    def _apply_color_scheme(self) -> None:
        colors = EDITOR_COLOR_SCHEMES[self._color_scheme]
        self.setStyleSheet(
            f"""
            QPlainTextEdit {{
                background: {colors['background']};
                color: {colors['foreground']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
                selection-background-color: {colors['selection_background']};
                selection-color: {colors['selection_foreground']};
                padding: 4px 4px 4px 0;
            }}
            """
        )
        self._line_number_area.update()
        self.viewport().update()
        self._schedule_decoration_refresh()

    def set_view_only(self, enabled: bool) -> None:
        """Enable or disable the hardened read-only editor mode."""
        enabled = bool(enabled)
        if enabled:
            self._pending_full_paste = None
            self._full_paste_generation += 1
        self.setReadOnly(enabled)
        self._schedule_decoration_refresh()

    def set_tab_width_spaces(self, spaces: int) -> None:
        """Set logical Tab width and update the displayed tab stop."""
        self._tab_width_spaces = max(1, spaces)
        self.setTabStopDistance(
            self.fontMetrics().horizontalAdvance(" ") * self._tab_width_spaces
        )

    def line_number_area_width(self) -> int:
        """Calculate the gutter width for the current line count."""
        if not self._line_numbers_visible:
            return 0
        digits = max(1, len(str(max(1, self.blockCount()))))
        return 14 + self.fontMetrics().horizontalAdvance("9") * digits

    def set_line_numbers_visible(self, visible: bool) -> None:
        """Show or hide the line-number gutter."""
        self._line_numbers_visible = bool(visible)
        self._line_number_area.setVisible(self._line_numbers_visible)
        self._update_line_number_area_width()
        self._line_number_area.update()

    def set_word_wrap_enabled(self, enabled: bool) -> None:
        """Enable or disable editor word wrapping."""
        mode = (
            QPlainTextEdit.LineWrapMode.WidgetWidth
            if enabled
            else QPlainTextEdit.LineWrapMode.NoWrap
        )
        self.setLineWrapMode(mode)

    def set_editor_font(self, font: QFont) -> None:
        """Apply a display font while retaining the configured logical Tab width."""
        self.setFont(font)
        self.setTabStopDistance(
            self.fontMetrics().horizontalAdvance(" ") * self._tab_width_spaces
        )
        self._update_line_number_area_width()

    def set_search_selections(
        self, selections: list[QTextEdit.ExtraSelection]
    ) -> None:
        """Install search highlights without replacing editor decorations."""
        self._search_selections = list(selections)
        self._schedule_decoration_refresh()

    def clear_search_selections(self) -> None:
        """Clear search highlights and retain current-line/bracket decorations."""
        self._search_selections = []
        self._schedule_decoration_refresh()

    def paint_line_number_area(self, event) -> None:
        """Paint only line numbers intersecting the exposed area."""
        if not self._line_numbers_visible:
            return
        painter = QPainter(self._line_number_area)
        painter.fillRect(
            event.rect(),
            QColor(EDITOR_COLOR_SCHEMES[self._color_scheme]["gutter_background"]),
        )

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())
        current_block_number = self.textCursor().blockNumber()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                colors = EDITOR_COLOR_SCHEMES[self._color_scheme]
                painter.setPen(
                    QColor(colors["gutter_current"])
                    if block_number == current_block_number
                    else QColor(colors["gutter_foreground"])
                )
                painter.drawText(
                    0,
                    top,
                    self._line_number_area.width() - 7,
                    self.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight,
                    str(block_number + 1),
                )

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def resizeEvent(self, event) -> None:  # noqa: N802 - Qt API name
        super().resizeEvent(event)
        contents = self.contentsRect()
        self._line_number_area.setGeometry(
            QRect(
                contents.left(),
                contents.top(),
                self.line_number_area_width(),
                contents.height(),
            )
        )

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802 - Qt API name
        modifiers = event.modifiers()
        key = event.key()

        if modifiers == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_G:
            self.go_to_line_requested.emit()
            return

        if key == Qt.Key.Key_Insert and modifiers in (
            Qt.KeyboardModifier.NoModifier,
            Qt.KeyboardModifier.KeypadModifier,
        ):
            enabled = not self.overwriteMode()
            self.setOverwriteMode(enabled)
            self.overwrite_mode_changed.emit(enabled)
            event.accept()
            return

        # Preserve navigation, selection and copying in View Only mode, but
        # explain the mode when the user presses a key that would modify text.
        if self.isReadOnly():
            if self._is_mutating_key_event(event):
                self.view_only_edit_attempt.emit()
                event.accept()
                return
            super().keyPressEvent(event)
            return

        if modifiers == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_Slash:
            self.toggle_comment()
            return

        if modifiers == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_D:
            self.duplicate_current_line_or_selection()
            return

        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self._insert_newline_with_indent()
            return

        if key == Qt.Key.Key_Tab and not (modifiers & Qt.KeyboardModifier.ControlModifier):
            if modifiers & Qt.KeyboardModifier.ShiftModifier:
                self._unindent_selection_or_line()
            else:
                self._indent_selection_or_insert_spaces()
            return

        if key == Qt.Key.Key_Backtab:
            self._unindent_selection_or_line()
            return

        super().keyPressEvent(event)

    @staticmethod
    def _is_mutating_key_event(event: QKeyEvent) -> bool:
        """Return whether a key event would normally change the document."""
        key = event.key()
        if key in (
            Qt.Key.Key_Backspace,
            Qt.Key.Key_Delete,
            Qt.Key.Key_Return,
            Qt.Key.Key_Enter,
            Qt.Key.Key_Tab,
            Qt.Key.Key_Backtab,
        ):
            return True

        for standard_key in (
            QKeySequence.StandardKey.Cut,
            QKeySequence.StandardKey.Paste,
            QKeySequence.StandardKey.Undo,
            QKeySequence.StandardKey.Redo,
        ):
            if event.matches(standard_key):
                return True

        modifiers = event.modifiers()
        if modifiers == Qt.KeyboardModifier.ControlModifier and key in (
            Qt.Key.Key_D,
            Qt.Key.Key_Slash,
        ):
            return True

        # Printable text includes normal typing and AltGr-composed characters.
        text = event.text()
        return bool(text and any(character.isprintable() for character in text))

    def inputMethodEvent(self, event: QInputMethodEvent) -> None:  # noqa: N802
        """Report blocked input-method text while retaining read-only safety."""
        if self.isReadOnly() and (event.commitString() or event.preeditString()):
            self.view_only_edit_attempt.emit()
            event.accept()
            return
        super().inputMethodEvent(event)

    def insertFromMimeData(self, source: QMimeData) -> None:  # noqa: N802
        """
        Insert clipboard/drop content as guarded plain text.

        Rich HTML, images, binary payloads and extremely large clipboard
        contents are not useful in a source-code editor and have triggered
        instability in some bundled Qt clipboard integrations.
        """
        if self.isReadOnly():
            self.view_only_edit_attempt.emit()
            return
        if source is None or not source.hasText():
            self.paste_rejected.emit(
                "Clipboard content is not plain text and was not pasted."
            )
            return

        try:
            text = source.text()
        except Exception as error:
            self.paste_rejected.emit(
                f"Clipboard text could not be read: {error}"
            )
            return

        if len(text) > self.MAX_PASTE_CHARACTERS:
            self.paste_rejected.emit(
                "Clipboard text is too large to paste safely."
            )
            return

        # NUL characters are invalid in normal source files and can cause
        # surprising behavior in downstream APIs.
        text = text.replace("\x00", "")
        if not text:
            return

        cursor = self.textCursor()
        document_length = max(0, self.document().characterCount() - 1)
        selected_length = abs(cursor.selectionEnd() - cursor.selectionStart())
        resulting_length = document_length - selected_length + len(text)
        if resulting_length > self.MAX_DOCUMENT_CHARACTERS:
            self.paste_rejected.emit(
                "The paste would exceed JSTS Pad's document safety limit."
            )
            return
        selection_start = min(cursor.selectionStart(), cursor.selectionEnd())
        selection_end = max(cursor.selectionStart(), cursor.selectionEnd())
        replaces_entire_document = (
            cursor.hasSelection()
            and selection_start == 0
            and selection_end >= document_length
        )

        if replaces_entire_document:
            # Replacing a full selected document during the same native Qt
            # event that created the selection can crash bundled Qt builds.
            # Complete the selection event first, then perform one guarded edit.
            self._pending_full_paste = text
            self._full_paste_generation += 1
            generation = self._full_paste_generation
            self._decoration_timer.stop()
            self.setExtraSelections([])
            QTimer.singleShot(
                0,
                lambda: self._apply_pending_full_paste(generation),
            )
            return

        plain = QMimeData()
        plain.setText(text)
        super().insertFromMimeData(plain)
        self._schedule_decoration_refresh()

    def dragEnterEvent(self, event) -> None:  # noqa: N802 - Qt API name
        mime = event.mimeData()
        if mime.hasUrls() and any(url.isLocalFile() for url in mime.urls()):
            event.acceptProposedAction()
            return
        super().dragEnterEvent(event)

    def dragMoveEvent(self, event) -> None:  # noqa: N802 - Qt API name
        mime = event.mimeData()
        if mime.hasUrls() and any(url.isLocalFile() for url in mime.urls()):
            event.acceptProposedAction()
            return
        super().dragMoveEvent(event)

    def dropEvent(self, event) -> None:  # noqa: N802 - Qt API name
        mime = event.mimeData()
        if mime.hasUrls():
            paths = [
                url.toLocalFile()
                for url in mime.urls()
                if url.isLocalFile()
            ]
            if paths:
                self.files_dropped.emit(paths)
                event.acceptProposedAction()
                return
        super().dropEvent(event)

    def _apply_pending_full_paste(self, generation: int) -> None:
        """Replace the whole document after Qt's selection event has settled."""
        if generation != self._full_paste_generation or self.isReadOnly():
            return

        text = self._pending_full_paste
        self._pending_full_paste = None
        if text is None:
            return

        self.replace_document_text(text)
        self.setFocus()

    def replace_document_text(self, text: str) -> bool:
        """Replace the complete document through the hardened editor path."""
        if self.isReadOnly():
            self.view_only_edit_attempt.emit()
            return False
        if len(text) > self.MAX_DOCUMENT_CHARACTERS:
            self.paste_rejected.emit(
                "The replacement would exceed JSTS Pad's document safety limit."
            )
            return False

        self._decoration_timer.stop()
        self.setExtraSelections([])

        # Temporarily detach the highlighter while the document structure is
        # replaced. It is reattached immediately and rehighlights afterwards.
        highlighter = self._highlighter
        highlighter.setDocument(None)
        cursor = QTextCursor(self.document())
        cursor.beginEditBlock()
        try:
            cursor.select(QTextCursor.SelectionType.Document)
            cursor.insertText(text)
            self.setTextCursor(cursor)
        finally:
            cursor.endEditBlock()
            highlighter.setDocument(self.document())

        self.document().setModified(True)
        self._schedule_decoration_refresh()
        return True

    def paste_safely(self) -> None:
        """Route programmatic Paste through the guarded MIME handler."""
        if self.isReadOnly():
            self.view_only_edit_attempt.emit()
            return
        from PyQt6.QtWidgets import QApplication

        clipboard = QApplication.clipboard()
        if clipboard is not None:
            self.insertFromMimeData(clipboard.mimeData())

    def delete_selection_or_character(self) -> None:
        """Delete the selection or the character after the cursor."""
        if self.isReadOnly():
            self.view_only_edit_attempt.emit()
            return

        cursor = self.textCursor()
        if cursor.hasSelection():
            cursor.removeSelectedText()
        else:
            cursor.deleteChar()
        self.setTextCursor(cursor)
        self.setFocus()

    def select_all_text(self) -> None:
        """Select the complete document using the guarded decoration path."""
        cursor = self.textCursor()
        cursor.select(QTextCursor.SelectionType.Document)
        self.setTextCursor(cursor)
        self.setFocus()
        self._decoration_timer.stop()
        self.setExtraSelections([])

    def toggle_comment(self) -> None:
        """Toggle JavaScript-style // comments on the selected/current lines."""
        if self.isReadOnly():
            self.view_only_edit_attempt.emit()
            return
        cursor = self.textCursor()
        start, end = self._selected_block_range(cursor)
        document = self.document()
        blocks = []
        block = document.findBlock(start)
        while block.isValid() and block.position() <= end:
            blocks.append(block)
            block = block.next()
        nonblank = [b for b in blocks if b.text().strip()]
        uncomment = bool(nonblank) and all(
            b.text().lstrip().startswith("//") for b in nonblank
        )
        cursor.beginEditBlock()
        delta = 0
        for block in blocks:
            text = block.text()
            if not text.strip():
                continue
            pos = block.position() + delta
            leading = len(text) - len(text.lstrip())
            edit = QTextCursor(document)
            edit.setPosition(pos + leading)
            if uncomment:
                edit.setPosition(pos + leading + 2, QTextCursor.MoveMode.KeepAnchor)
                if edit.selectedText() == "//":
                    edit.removeSelectedText()
                    delta -= 2
                    # Remove one conventional following space when present.
                    after = QTextCursor(document)
                    after.setPosition(pos + leading)
                    after.movePosition(QTextCursor.MoveOperation.NextCharacter, QTextCursor.MoveMode.KeepAnchor)
                    if after.selectedText() == " ":
                        after.removeSelectedText()
                        delta -= 1
            else:
                edit.insertText("// ")
                delta += 3
        cursor.endEditBlock()
        self.setFocus()

    def duplicate_current_line_or_selection(self) -> None:
        """Duplicate the selected text or the current complete line."""
        if self.isReadOnly():
            self.view_only_edit_attempt.emit()
            return
        cursor = self.textCursor()
        cursor.beginEditBlock()

        if cursor.hasSelection():
            selected = cursor.selectedText().replace("\u2029", "\n")
            addition = len(selected)
            insertion = selected
            cursor.setPosition(cursor.selectionEnd())
        else:
            cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
            cursor.movePosition(
                QTextCursor.MoveOperation.EndOfBlock,
                QTextCursor.MoveMode.KeepAnchor,
            )
            line = cursor.selectedText()
            addition = len(line) + 1
            insertion = "\n" + line
            cursor.clearSelection()
            cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock)

        document_length = max(0, self.document().characterCount() - 1)
        if document_length + addition > self.MAX_DOCUMENT_CHARACTERS:
            cursor.endEditBlock()
            self.paste_rejected.emit(
                "Duplication would exceed JSTS Pad's document safety limit."
            )
            return
        cursor.insertText(insertion)

        cursor.endEditBlock()
        self.setTextCursor(cursor)

    def delete_current_line(self) -> None:
        """Delete the complete current line without affecting other content."""
        if self.isReadOnly():
            self.view_only_edit_attempt.emit()
            return

        cursor = self.textCursor()
        block = cursor.block()
        start = block.position()
        end = start + max(0, block.length() - 1)
        next_block = block.next()

        cursor.beginEditBlock()
        if next_block.isValid():
            # Remove this line and its following paragraph separator.
            cursor.setPosition(start)
            cursor.setPosition(next_block.position(), QTextCursor.MoveMode.KeepAnchor)
            cursor.removeSelectedText()
        elif start > 0:
            # Last line: include the preceding separator so no empty tail line
            # is left behind.
            cursor.setPosition(start - 1)
            cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
            cursor.removeSelectedText()
        else:
            # Single-line document: clear the line while retaining the one
            # document block Qt requires.
            cursor.setPosition(start)
            cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
            cursor.removeSelectedText()
        cursor.endEditBlock()
        self.setTextCursor(cursor)
        self.setFocus()

    def go_to_line(self, line_number: int) -> bool:
        """Move the cursor to a one-based line number."""
        if line_number < 1 or line_number > self.blockCount():
            return False

        block = self.document().findBlockByNumber(line_number - 1)
        if not block.isValid():
            return False

        cursor = QTextCursor(block)
        self.setTextCursor(cursor)
        self.centerCursor()
        self.setFocus()
        return True

    def load_text(self, text: str) -> None:
        """Load text efficiently and mark the Qt document clean."""
        self._decoration_timer.stop()
        self.setExtraSelections([])
        highlighter = self._highlighter
        highlighter.setDocument(None)
        try:
            self.setPlainText(text)
        finally:
            highlighter.setDocument(self.document())
        self.document().setModified(False)
        self._schedule_decoration_refresh()

    def mark_clean(self) -> None:
        """Mark the current document state as saved."""
        self.document().setModified(False)

    @property
    def is_modified(self) -> bool:
        """Return Qt's efficient native dirty-state flag."""
        return self.document().isModified()

    def _update_line_number_area_width(self, _new_count: int = 0) -> None:
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def _update_line_number_area(self, rect: QRect, dy: int) -> None:
        if dy:
            self._line_number_area.scroll(0, dy)
        else:
            self._line_number_area.update(0, rect.y(), self._line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self._update_line_number_area_width()

    def _schedule_decoration_refresh(self, *_args) -> None:
        """Repaint decorations only after Qt has completed the current edit."""
        if not self._decoration_timer.isActive():
            self._decoration_timer.start()

    def _refresh_extra_selections(self) -> None:
        """
        Refresh visual-only decorations without allowing a bad cursor snapshot
        to escape through Qt's event loop.

        Cursor and document lengths can briefly disagree immediately after a
        large replacement. Decorations are optional, so any transient failure
        clears them rather than terminating the application.
        """
        if self._refreshing_extra_selections:
            return

        self._refreshing_extra_selections = True
        try:
            selections: list[QTextEdit.ExtraSelection] = list(
                self._search_selections
            )
            cursor = self.textCursor()

            if not cursor.hasSelection():
                if not self.isReadOnly():
                    current_line = QTextEdit.ExtraSelection()
                    current_line.format.setBackground(
                        QColor(
                            EDITOR_COLOR_SCHEMES[self._color_scheme][
                                "current_line"
                            ]
                        )
                    )
                    current_line.format.setProperty(
                        QTextCharFormat.Property.FullWidthSelection,
                        True,
                    )
                    current_line.cursor = QTextCursor(cursor)
                    current_line.cursor.clearSelection()
                    selections.append(current_line)

                selections.extend(self._matching_bracket_selections())
                selections.extend(self._matching_tag_selections())

            self.setExtraSelections(selections)
        except (IndexError, RuntimeError, ValueError):
            # A stale cursor position is harmless; retry on the next cursor or
            # text event after Qt has fully synchronized the document.
            self.setExtraSelections([])
        finally:
            self._line_number_area.update()
            self._refreshing_extra_selections = False

    def _matching_bracket_selections(self) -> list[QTextEdit.ExtraSelection]:
        document = self.document()
        text_length = max(0, document.characterCount() - 1)
        if text_length == 0:
            return []

        cursor = self.textCursor()
        position = max(0, min(cursor.position(), text_length))
        candidate_positions: list[int] = []
        if position > 0:
            candidate_positions.append(position - 1)
        if position < text_length:
            candidate_positions.append(position)

        bracket_position: int | None = None
        bracket = ""
        for index in candidate_positions:
            character = document.characterAt(index)
            if character in self.BRACKET_PAIRS:
                bracket_position = index
                bracket = character
                break
        if bracket_position is None:
            return []

        match_position = self._find_matching_bracket(
            document,
            bracket_position,
            bracket,
            text_length,
        )
        if match_position is None:
            return []

        selections: list[QTextEdit.ExtraSelection] = []
        for index in (bracket_position, match_position):
            selection = QTextEdit.ExtraSelection()
            colors = EDITOR_COLOR_SCHEMES[self._color_scheme]
            selection.format.setBackground(QColor(colors["bracket_background"]))
            selection.format.setForeground(QColor(colors["bracket_foreground"]))
            selection.cursor = QTextCursor(document)
            selection.cursor.setPosition(index)
            selection.cursor.movePosition(
                QTextCursor.MoveOperation.NextCharacter,
                QTextCursor.MoveMode.KeepAnchor,
            )
            selections.append(selection)
        return selections

    def _matching_tag_selections(self) -> list[QTextEdit.ExtraSelection]:
        """Highlight a nearby JSX/TSX opening/closing element pair."""
        if self._language not in {"jsx", "tsx"}:
            return []
        document = self.document()
        text_length = max(0, document.characterCount() - 1)
        if not text_length:
            return []
        cursor_pos = max(0, min(self.textCursor().position(), text_length))
        radius = min(self.MAX_BRACKET_SCAN_CHARACTERS, 150_000)
        start = max(0, cursor_pos - radius)
        end = min(text_length, cursor_pos + radius)
        probe = QTextCursor(document)
        probe.setPosition(start)
        probe.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
        text = probe.selectedText().replace("\u2029", "\n")
        local_pos = cursor_pos - start
        # Deliberately conservative: named JSX elements only. Fragments remain
        # editable/highlighted by syntax colouring but are not pair-scanned.
        tag_re = re.compile(r"<\s*(/?)\s*([A-Za-z_$][\w$.-]*(?:\.[A-Za-z_$][\w$-]*)*)\b[^<>]*?(/?)>")
        tags = list(tag_re.finditer(text))
        current_index = None
        for index, match in enumerate(tags):
            if match.start() <= local_pos <= match.end():
                current_index = index
                break
        if current_index is None:
            return []
        current = tags[current_index]
        name = current.group(2)
        if current.group(3):
            return []
        is_closing = bool(current.group(1))
        partner = None
        depth = 1
        if not is_closing:
            for match in tags[current_index + 1:]:
                if match.group(2) != name or match.group(3):
                    continue
                if match.group(1):
                    depth -= 1
                    if depth == 0:
                        partner = match
                        break
                else:
                    depth += 1
        else:
            for match in reversed(tags[:current_index]):
                if match.group(2) != name or match.group(3):
                    continue
                if match.group(1):
                    depth += 1
                else:
                    depth -= 1
                    if depth == 0:
                        partner = match
                        break
        if partner is None:
            return []
        colors = EDITOR_COLOR_SCHEMES[self._color_scheme]
        selections: list[QTextEdit.ExtraSelection] = []
        for match in (current, partner):
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(QColor(colors["bracket_background"]))
            selection.format.setForeground(QColor(colors["bracket_foreground"]))
            selection.cursor = QTextCursor(document)
            selection.cursor.setPosition(start + match.start())
            selection.cursor.setPosition(start + match.end(), QTextCursor.MoveMode.KeepAnchor)
            selections.append(selection)
        return selections

    def _find_matching_bracket(
        self,
        document: QTextDocument,
        position: int,
        bracket: str,
        text_length: int,
    ) -> int | None:
        if not (0 <= position < text_length):
            return None
        partner = self.BRACKET_PAIRS.get(bracket)
        if partner is None:
            return None

        if bracket in self.OPENING_BRACKETS:
            depth = 1
            stop = min(
                text_length,
                position + 1 + self.MAX_BRACKET_SCAN_CHARACTERS,
            )
            for index in range(position + 1, stop):
                character = document.characterAt(index)
                if character == bracket:
                    depth += 1
                elif character == partner:
                    depth -= 1
                    if depth == 0:
                        return index
        else:
            depth = 1
            stop = max(-1, position - self.MAX_BRACKET_SCAN_CHARACTERS - 1)
            for index in range(position - 1, stop, -1):
                character = document.characterAt(index)
                if character == bracket:
                    depth += 1
                elif character == partner:
                    depth -= 1
                    if depth == 0:
                        return index
        return None

    def _insert_newline_with_indent(self) -> None:
        if self.isReadOnly():
            self.view_only_edit_attempt.emit()
            return
        cursor = self.textCursor()
        current_line = cursor.block().text()
        leading = current_line[: len(current_line) - len(current_line.lstrip())]
        before_cursor = current_line[: cursor.positionInBlock()].rstrip()
        after_cursor = current_line[cursor.positionInBlock():].lstrip()
        indent = leading
        if before_cursor.endswith(("{", "[", "(")):
            indent += " " * self._tab_width_spaces
        # If Enter is pressed between paired delimiters, create the conventional
        # blank indented line while keeping the closer at the original level.
        paired = (("{", "}"), ("[", "]"), ("(", ")"))
        closer = next((close for open_, close in paired if before_cursor.endswith(open_) and after_cursor.startswith(close)), None)
        if closer is not None:
            cursor.insertText("\n" + indent + "\n" + leading)
            cursor.movePosition(QTextCursor.MoveOperation.Up)
            cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock)
        else:
            cursor.insertText("\n" + indent)
        self.setTextCursor(cursor)

    def _indent_selection_or_insert_spaces(self) -> None:
        if self.isReadOnly():
            self.view_only_edit_attempt.emit()
            return
        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.insertText(" " * self._tab_width_spaces)
            return

        start, end = self._selected_block_range(cursor)
        cursor.beginEditBlock()
        cursor.setPosition(start)

        while cursor.position() <= end:
            cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
            cursor.insertText(" " * self._tab_width_spaces)
            end += self._tab_width_spaces

            if not cursor.movePosition(QTextCursor.MoveOperation.NextBlock):
                break

        cursor.endEditBlock()

    def _unindent_selection_or_line(self) -> None:
        if self.isReadOnly():
            self.view_only_edit_attempt.emit()
            return
        cursor = self.textCursor()
        start, end = self._selected_block_range(cursor)
        cursor.beginEditBlock()
        cursor.setPosition(start)

        while cursor.position() <= end:
            cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
            block_text = cursor.block().text()

            remove_count = 0
            if block_text.startswith("\t"):
                remove_count = 1
            else:
                remove_count = min(
                    self._tab_width_spaces,
                    len(block_text) - len(block_text.lstrip(" ")),
                )

            for _ in range(remove_count):
                cursor.deleteChar()
            end -= remove_count

            if not cursor.movePosition(QTextCursor.MoveOperation.NextBlock):
                break

        cursor.endEditBlock()

    def _selected_block_range(self, cursor: QTextCursor) -> tuple[int, int]:
        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        start_cursor = QTextCursor(self.document())
        start_cursor.setPosition(start)
        start_cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)

        end_cursor = QTextCursor(self.document())
        end_cursor.setPosition(end)
        if end > start and end_cursor.positionInBlock() == 0:
            end_cursor.movePosition(QTextCursor.MoveOperation.PreviousBlock)
        end_cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock)

        return start_cursor.position(), end_cursor.position()
