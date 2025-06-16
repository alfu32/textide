import shutil

from textual import work
from textual.widgets import DirectoryTree
from textual.message import Message
from pathlib import Path

from textual_fspicker import SelectDirectory

from textide.panels.InputModal import InputModal


class FileTreePanel(DirectoryTree, can_focus=True):
    """A minimal git panel: status lines as selectable items + key bindings."""
    BINDINGS = [
        ("r", "refresh", "Refresh"),
        ("n", "new_file",   "New File"),
        ("f", "new_folder", "New Folder"),
        ("x", "rename",  "Rename"),
        ("e", "delete",    "Delete"),
    ]

    @work
    async def action_refresh(self):
        self.reload()

    @work
    async def action_new_file(self):
        if name := await self.app.push_screen_wait(InputModal("New File", "Enter filename")):
            self.create_file(name)

    @work
    async def action_new_folder(self):
        if name := await self.app.push_screen_wait(InputModal("New Folder", "Enter folder name")):
            self.create_folder(name)

    @work
    async def action_rename(self):
        if name := await self.app.push_screen_wait(
                InputModal("Rename", "Enter new name", default=self.get_current_name())):
            self.rename_current(name)

    @work
    async def action_delete(self):
        if confirm := await self.app.push_screen_wait(InputModal("Delete", "Type YES to confirm", default="")):
            if confirm.lower() == "yes":
                self.delete_current()

    def create_file(self, name: str):
        target = (self.selected.parent if self.selected.is_file() else self.selected) / name
        try:
            target.touch(exist_ok=False)
            self.notify(f"Created file: {target.name}")
            self.reload()
        except Exception as e:
            self.notify(f"Error creating file: {e}", severity="error")

    def create_folder(self, name: str):
        target = (self.selected.parent if self.selected.is_file() else self.selected) / name
        try:
            target.mkdir(parents=True, exist_ok=False)
            self.notify(f"Created folder: {target.name}")
            self.reload()
        except Exception as e:
            self.notify(f"Error creating folder: {e}", severity="error")

    def rename_current(self, new_name: str):
        if not hasattr(self, "selected") or self.selected is None:
            self.notify("Nothing selected to rename", severity="error")
            return
        try:
            new_path = self.selected.parent / new_name
            self.selected.rename(new_path)
            self.selected = new_path
            self.notify(f"Renamed to: {new_path.name}")
            self.reload()
        except Exception as e:
            self.notify(f"Error renaming: {e}", severity="error")

    def delete_current(self):
        if not hasattr(self, "selected") or self.selected is None:
            self.notify("Nothing selected to delete", severity="error")
            return
        try:
            if self.selected.is_dir():
                shutil.rmtree(self.selected)
            else:
                self.selected.unlink()
            self.notify(f"Deleted: {self.selected.name}")
            self.selected = None
            self.reload()
        except Exception as e:
            self.notify(f"Error deleting: {e}", severity="error")

    def get_current_name(self) -> str:
        if hasattr(self, "selected") and self.selected:
            return self.selected.name
        return ""

    class FilePicked(Message):  # Unique, avoids name conflict
        def __init__(self, path: str) -> None:
            self.path = path
            super().__init__()

    def __init__(self, path: Path = Path.cwd(), **kwargs):
        super().__init__(path, **kwargs)
        self.selected = None
        self.selected = Path(path)
        self.selected.resolve()
        self.ICON_FILE=' '
        self.ICON_NODE='■ '
        self.ICON_NODE_EXPANDED='■ '
        # self.ICON_FILE='◙ '
        # self.ICON_NODE = '→ ' # '■ ■²ⁿ√·∙°≈÷⌡⌠≤≥±≡∩εφ∞δΩΦΘτµσΣπΓßα▀▐ ▌ ▄ █▀▄█┌┘╪╫╓╒╘╙╥╤╨╧╬═╠╦╩╩¶╚╟╞╞┼─├┬┴└┐╛╜╝╗║╣\╕╕╖╢╡┤↕↕◄►☼♫♪♀♂◙○◘•♠♣♦♥☻☺¶§▬↨↑↓→←∟↔▲▼ !"'
        # self.ICON_NODE_EXPANDED = '↕ '

    async def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        p=event.path.resolve()
        self.selected = p
        self.log(f"File {p} picked successfully", severity="information")
        self.post_message(FileTreePanel.FilePicked(p.__str__()))
