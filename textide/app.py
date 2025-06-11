# textide/app.py
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Horizontal, Vertical
from textide.panels.file_tree import FileTreePanel
from textide.panels.git_panel import GitPanel
from textide.panels.editors import EditorsPanel


class TextIDEApp(App):
    CSS_PATH = "app.css"

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def __init__(self):
        super().__init__()
        self.editor: EditorsPanel | None = None
        self.notify(f"W.E.L.C.O.M.E to TextIDE", severity="information")

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical():
                yield FileTreePanel(id="file-tree")
                yield GitPanel(id="git-panel")
            self.editor = EditorsPanel(id="editors")
            yield self.editor
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    async def on_file_tree_panel_file_picked(self, msg: FileTreePanel.FilePicked) -> None:
        self.log(f"received picked file! {msg.path}")
        # editor: EditorPanel = self.query_one(EditorPanel)
        # editor.load_file(path=msg.path)
        # self.set_focus(editor)  # ✅ move focus into the editor
        editor = self.query_one("#editors", EditorsPanel)
        with open(msg.path, "r", encoding="utf-8") as f:
            content = f.read()
        editor.load_content(content, path=msg.path)
        self.set_focus(editor)



if __name__ == "__main__":
    app = TextIDEApp()
    app.run()