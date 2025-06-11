from textual.widgets import DirectoryTree
from textual.message import Message
from pathlib import Path

class FileTreePanel(DirectoryTree):

    class FilePicked(Message):  # Unique, avoids name conflict
        def __init__(self, path: str) -> None:
            self.path = path
            super().__init__()

    def __init__(self, path: Path = Path.cwd(), **kwargs):
        super().__init__(path, **kwargs)

    async def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        p=event.path.resolve()
        self.log(f"File {p} picked successfully", severity="information")
        self.post_message(FileTreePanel.FilePicked(p.__str__()))