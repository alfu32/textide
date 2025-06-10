# textide/panels/editor_screen.py
from textual.screen import Screen
from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.document import Document
from pygments.lexers import PythonLexer
from prompt_toolkit.styles import Style
from threading import Thread
from pathlib import Path

class EditorScreen(Screen):
    def __init__(self, path: Path):
        super().__init__()
        self.path = path
        self.thread = None

    def compose(self):
        yield  # No Textual UI here — just prompt_toolkit

    def on_mount(self):
        self.thread = Thread(target=self.launch_editor, daemon=True)
        self.thread.start()

    def launch_editor(self):
        # Read the file
        try:
            text = self.path.read_text(encoding="utf-8")
        except Exception as e:
            text = f"# Failed to load: {e}\n"

        # Create buffer
        buffer = Buffer(
            document=Document(text),
            multiline=True
        )

        editor = TextArea(
            buffer=buffer,
            lexer=PygmentsLexer(PythonLexer),
            scrollbar=True,
            line_numbers=True,
        )

        kb = KeyBindings()

        @kb.add("c-s")
        def _(event):
            # Save the buffer content
            try:
                self.path.write_text(buffer.text, encoding="utf-8")
            except Exception as e:
                buffer.insert_text(f"\n# Save failed: {e}\n")

        @kb.add("c-q")
        def _(event):
            event.app.exit()
            self.app.pop_screen()

        style = Style.from_dict({
            "editor": "bg:#1e1e1e #ffffff",
            "cursor-line": "bg:#333333",
        })

        app = Application(
            layout=Layout(editor),
            key_bindings=kb,
            style=style,
            full_screen=True,
            mouse_support=True
        )

        app.run()
