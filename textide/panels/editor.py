# textide/panels/editor.py
from textual.widget import Widget
from textual.reactive import reactive
from prompt_toolkit.document import Document
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout import Window
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.application import get_app_or_none
from prompt_toolkit.data_structures import Point
from pygments import lex
from pygments.lexers.python import PythonLexer
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.token import Token
from rich.text import Text

# Mapping Pygments token types to Rich styles
PYGMENTS_STYLE_MAP = {
    Token.Keyword: "bold magenta",
    Token.Name: "white",
    Token.Literal.String: "yellow",
    Token.Comment: "dim",
    Token.Operator: "cyan",
    Token.Punctuation: "white",
    Token.Number: "bright_blue",
    Token.Name.Function: "bold green",
    Token.Name.Class: "bold blue",
    Token.Text: "white",
}

def get_rich_style(token_type):
    """Simplify token types to their base class (e.g., Token.Comment.Single -> Token.Comment)"""
    while token_type not in PYGMENTS_STYLE_MAP and token_type.parent != token_type:
        token_type = token_type.parent
    return PYGMENTS_STYLE_MAP.get(token_type, "white")

class EditorPanel(Widget):
    can_focus = True  # ✅ this allows keyboard focus
    filename = reactive("")
    content = reactive("# Start typing Python code...\n", layout=True)
    
    def load_file(self, path:str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                self.filename = str(path)
                self.buffer.document = Document(content, cursor_position=0)
        except Exception as e:
            self.buffer.document = Document(f"Error loading file:\n{e}", cursor_position=0)
            self.filename = "<error>"
        self.refresh()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.buffer = Buffer(
            document=Document(self.content),
            multiline=True
        )
        self.lexer = PygmentsLexer(PythonLexer)

    def render(self) -> Text:
        self.content = self.buffer.text
        output = Text()
        if self.has_focus:
            output.stylize("reverse", 0, 1)  # Show something if focused

        try:
            tokens = lex(self.content, PythonLexer())
            for tok_type, tok_val in tokens:
                style = get_rich_style(tok_type)
                output.append(tok_val, style)
        except Exception as e:
            output.append(str(e), "bold red")

        return output

    def on_key(self, event) -> None:
        key = event.key

        if len(key) == 1:
            self.buffer.insert_text(key)
        elif key == "backspace":
            self.buffer.delete_before_cursor()
        elif key == "enter":
            self.buffer.insert_text("\n")
        elif key == "left":
            self.buffer.cursor_left()
        elif key == "right":
            self.buffer.cursor_right()
        elif key == "up":
            self.buffer.cursor_up()
        elif key == "down":
            self.buffer.cursor_down()
        elif key == "tab":
            self.buffer.insert_text("    ")
        elif key == "ctrl+s":
            self.save_file()
