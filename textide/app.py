# textide/app.py
import sys
from pathlib import Path

from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Horizontal, Vertical
from textual_fspicker import SelectDirectory

from textide.panels.ShellsPanel import Shell
from textide.panels.file_tree import FileTreePanel
from textide.panels.git_panel import GitPanel
from textide.panels.editors import EditorsPanel
from textide.panels.vertical_tabs import VerticalTabs


class TextIDEApp(App):
    CSS_PATH = "app.tcss"

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("o", "open_workspace", "Open Workspace"),
    ]

    def __init__(self,base:Path):
        super().__init__()
        self.editor: EditorsPanel | None = None
        self.file_tree_panel: FileTreePanel | None = None
        self.git_panel: GitPanel | None = None
        self.terminal_panel: Shell | None = None
        self.base=base
        self.notify(f"W.E.L.C.O.M.E to TextIDE", severity="information")

    def compose(self) -> ComposeResult:
        if self.editor is None:
            self.editor = EditorsPanel(id="editors")
        if self.git_panel is None:
            self.git_panel = GitPanel(self.base,id="git-panel")
        if self.file_tree_panel is None:
            self.file_tree_panel =FileTreePanel(path=self.base,id="file-tree")
        if self.terminal_panel is None:
            self.terminal_panel = Shell(id="terminal-shell")
        tabs = [
            ("☰", self.file_tree_panel),
            ("⎇", self.git_panel ),
        ]
        yield Header()
        with Horizontal():
            yield VerticalTabs(tabs,id="left-panel")
            with Vertical(id="right-panel"):
                yield self.editor
                yield self.terminal_panel
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    @work
    async def action_open_workspace(self):
        if opened := await self.push_screen_wait(SelectDirectory(location=self.base)):
            self.base = (str(opened))
            self.git_panel.path=Path(self.base)
            self.git_panel.action_refresh()
            self.file_tree_panel.path=self.base

            await self.file_tree_panel.reload()

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
    app = TextIDEApp(base=Path(sys.argv[1] if len(sys.argv) >1 else "."))
    app.run()