# textide/app.py
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Horizontal, Vertical
from textide.panels.file_tree import FileTreePanel
from textide.panels.git_panel import GitPanel
from textide.panels.editor import EditorPanel
from textual.widgets import DirectoryTree
from textide.panels.editor_screen import EditorScreen


class TextIDEApp(App):
    CSS_PATH = "app.css"

    def __init__(self):
        super().__init__()
        self.editor: EditorPanel | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical():
                yield FileTreePanel(id="file-tree")
                yield GitPanel(id="git-panel")
            self.editor = EditorPanel(id="editor")
            yield self.editor
        yield Footer()

    async def on_file_tree_panel_file_picked(self, msg: FileTreePanel.FilePicked) -> None:
        self.notify(f"received picked file! {msg.path}", severity="info")
        editor: EditorPanel = self.query_one(EditorPanel)
        editor.load_file(path=msg.path)
        self.set_focus(editor)  # ✅ move focus into the editor