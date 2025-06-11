# textide/panels/editor.py
from textual.widget import Widget
from textual.reactive import reactive
from textual import events
from rich.text import Text
from pygments import lex
from pygments.lexers.python import PythonLexer
from pygments.token import Token

def split_text_lines(text: Text) -> list[Text]:
    lines = []
    current = Text()
    for span in text.split("\n"):
        current = Text()
        current.append(span)
        lines.append(current)
    return lines

class EditorPanel(Widget):
    can_focus = True

    content = reactive("")
    cursor_x = reactive(0)
    cursor_y = reactive(0)
    scroll_y = reactive(0)
    current_path = None

    def load_content(self, content: str, path=None):
        self.content = content
        self.current_path = path
        self.cursor_x = 0
        self.cursor_y = 0
        self.scroll_y = 0
        self.refresh()

    def save_content(self):
        if not self.current_path:
            return
        with open(self.current_path, "w", encoding="utf-8") as f:
            f.write(self.content)

    def key_down(self):
        if self.cursor_y + 1 < len(self._lines()):
            self.cursor_y += 1
            self.cursor_x = min(self.cursor_x, len(self._lines()[self.cursor_y]))

    def key_up(self):
        if self.cursor_y > 0:
            self.cursor_y -= 1
            self.cursor_x = min(self.cursor_x, len(self._lines()[self.cursor_y]))

    def key_left(self):
        if self.cursor_x > 0:
            self.cursor_x -= 1
        elif self.cursor_y > 0:
            self.cursor_y -= 1
            self.cursor_x = len(self._lines()[self.cursor_y])

    def key_right(self):
        line = self._lines()[self.cursor_y]
        if self.cursor_x < len(line):
            self.cursor_x += 1
        elif self.cursor_y + 1 < len(self._lines()):
            self.cursor_y += 1
            self.cursor_x = 0

    def _lines(self):
        return self.content.splitlines() or [""]

    def insert_char(self, c: str):
        lines = self._lines()
        line = lines[self.cursor_y]
        new_line = line[:self.cursor_x] + c + line[self.cursor_x:]
        lines[self.cursor_y] = new_line
        self.cursor_x += 1
        self.content = "\n".join(lines)

    def backspace(self):
        lines = self._lines()
        if self.cursor_x > 0:
            line = lines[self.cursor_y]
            new_line = line[:self.cursor_x - 1] + line[self.cursor_x:]
            lines[self.cursor_y] = new_line
            self.cursor_x -= 1
        elif self.cursor_y > 0:
            prev_line = lines[self.cursor_y - 1]
            current_line = lines.pop(self.cursor_y)
            self.cursor_y -= 1
            self.cursor_x = len(prev_line)
            lines[self.cursor_y] = prev_line + current_line
        self.content = "\n".join(lines)

    def on_key(self, event: events.Key) -> None:
        key = event.key

        if key == "up":
            self.key_up()
        elif key == "down":
            self.key_down()
        elif key == "left":
            self.key_left()
        elif key == "right":
            self.key_right()
        elif key == "backspace":
            self.backspace()
        elif key == "enter":
            lines = self._lines()
            line = lines[self.cursor_y]
            before, after = line[:self.cursor_x], line[self.cursor_x:]
            lines[self.cursor_y] = before
            lines.insert(self.cursor_y + 1, after)
            self.cursor_y += 1
            self.cursor_x = 0
            self.content = "\n".join(lines)
        elif len(key) == 1:
            self.insert_char(key)

        # Auto-scroll logic
        height = self.size.height
        if self.cursor_y < self.scroll_y:
            self.scroll_y = self.cursor_y
        elif self.cursor_y >= self.scroll_y + height:
            self.scroll_y = self.cursor_y - height + 1

        self.refresh()

    def render(self) -> Text:
        lines = self._lines()
        total_lines = len(lines)

        # Adjust scroll position if cursor moves off-screen
        if self.cursor_y < self.scroll_y:
            self.scroll_y = self.cursor_y
        elif self.cursor_y >= self.scroll_y + self.size.height:
            self.scroll_y = self.cursor_y - self.size.height + 1

        # Lex entire content once
        all_tokens = list(lex(self.content, PythonLexer()))

        # Build Text with syntax + line numbers
        rendered = Text()
        current_line = 0
        current_line_tokens = []
        line_buffer = []

        def flush_line():
            nonlocal rendered, current_line_tokens, current_line
            line_text = Text(f"{current_line + 1:>4} │ ", style="dim")  # Line number prefix
            for ttype2, val2 in current_line_tokens:
                line_text.append(val2, self._token_style(ttype2))
            rendered.append(line_text)
            rendered.append("\n")
            current_line_tokens = []

        for ttype, val in all_tokens:
            val_lines = val.split("\n")
            for i, piece in enumerate(val_lines):
                if i > 0:
                    flush_line()
                    current_line += 1
                current_line_tokens.append((ttype, piece))
        flush_line()

        # Slice visible lines
        # self._lines()[self.scroll_y:self.scroll_y + self.size.height]
        visible_text = rendered.crop_lines(self.scroll_y, self.scroll_y + self.size.height)

        # Caret
        cy = self.cursor_y
        cx = self.cursor_x
        if self.scroll_y <= cy < self.scroll_y + self.size.height:
            line_offset = cy - self.scroll_y
            prefix_len = 6  # " 999 │ "
            caret_pos = 0
            line = lines[cy] if cy < len(lines) else ""
            caret_pos = prefix_len + min(cx, len(line))
            absolute = sum(len(l.plain) + 1 for l in visible_text.lines[:line_offset]) + caret_pos
            visible_text.stylize("reverse", absolute, absolute + 1)

        return visible_text

    def _token_style(self, token):
        while token is not None and token not in TOKEN_MAP and token.parent is not None and token.parent != token:
            token = token.parent
        return TOKEN_MAP.get(token, "white")

# Basic token-to-style map
TOKEN_MAP = {
    Token.Keyword: "bold magenta",
    Token.Name: "white",
    Token.Comment: "dim",
    Token.Literal.String: "yellow",
    Token.Operator: "cyan",
    Token.Punctuation: "white",
    Token.Number: "blue",
    Token.Name.Function: "bold green",
    Token.Name.Class: "bold blue",
    Token.Text: "white",
}
