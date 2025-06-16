from textual import work
from textual.widgets import DirectoryTree
from textual.message import Message
from pathlib import Path

from textual_fspicker import SelectDirectory

class FileTreePanel(DirectoryTree, can_focus=True):
    """A minimal git panel: status lines as selectable items + key bindings."""
    BINDINGS = [
        ("r", "refresh", "Refresh"),
        ("n", "new_file",   "New File"),
        ("f", "new_folder", "New Folder"),
        ("x", "rename",  "Rename"),
        ("d", "delete",    "Delete"),
        ("o", "open_workspace", "Open Workspace"),
    ]

    class FilePicked(Message):  # Unique, avoids name conflict
        def __init__(self, path: str) -> None:
            self.path = path
            super().__init__()

    def __init__(self, path: Path = Path.cwd(), **kwargs):
        super().__init__(path, **kwargs)
        self.ICON_FILE=' '
        self.ICON_NODE='■ '
        self.ICON_NODE_EXPANDED='■ '
        # self.ICON_FILE='◙ '
        # self.ICON_NODE = '→ ' # '■ ■²ⁿ√·∙°≈÷⌡⌠≤≥±≡∩εφ∞δΩΦΘτµσΣπΓßα▀▐ ▌ ▄ █▀▄█┌┘╪╫╓╒╘╙╥╤╨╧╬═╠╦╩╩¶╚╟╞╞┼─├┬┴└┐╛╜╝╗║╣\╕╕╖╢╡┤↕↕◄►☼♫♪♀♂◙○◘•♠♣♦♥☻☺¶§▬↨↑↓→←∟↔▲▼ !"'
        # self.ICON_NODE_EXPANDED = '↕ '

    async def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        p=event.path.resolve()
        self.log(f"File {p} picked successfully", severity="information")
        self.post_message(FileTreePanel.FilePicked(p.__str__()))

    @work
    async def action_open_workspace(self):
        if opened := await self.app.push_screen_wait(SelectDirectory(location=self.path)):
            self.path = (str(opened))
            await self.reload()