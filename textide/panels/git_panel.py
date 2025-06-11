# textide/panels/git_panel.py

import subprocess
from pathlib import Path
from typing import List, Dict

from textual.app import ComposeResult
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Tree, TextArea, Button
from textual.containers import Vertical


def _parse_porcelain(lines: List[str]) -> Dict:
    """
    Turn porcelain lines into a nested folder→...→leaf dict.
    Leaf entries have a dict value with keys:
      - "__path__": the full repo‐relative path
      - "staged": bool
    """
    tree: Dict[str, any] = {}
    for line in lines:
        status = line[:2]
        raw = line[3:].strip()
        # handle renames "R100 old -> new"
        if " -> " in raw:
            raw = raw.split(" -> ", 1)[1]
        parts = raw.split("/")
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        # final part = filename
        node[parts[-1]] = {
            "__path__": raw,
            "staged": (status[0] != " "),
        }
    return tree
def parse(lines) -> (list,list):
    staged, unstaged = [], []
    for line in lines:
        code, path = line[:2], line[3:].strip()
        # code[0] = INDEX status, code[1] = WORKTREE status
        if code[0] != " ":
            staged.append(path)
        elif code[1] != " " or code.startswith("??"):
            unstaged.append(path)
    return staged,unstaged
class GitPanel(Widget):
    """A Git commit UI with a Tree of changed files and a commit form."""

    BINDINGS = [("c", "commit", "Commit")]

    class Commit(Message):
        """Fired after a successful commit."""
        def __init__(self, message: str, staged: List[str]) -> None:
            self.message = message
            self.staged = staged
            super().__init__()

    # reactive lists so UI updates when you reassign them
    staged_files: reactive[List[str]]   = reactive([])
    unstaged_files: reactive[List[str]] = reactive([])

    def compose(self) -> ComposeResult:
        # 1) the tree of changes
        yield Tree("Git Changes", id="git-tree")
        # 2) the commit message area
        yield TextArea(
            text="",
            id="git-commit-msg",
        )

    def on_mount(self) -> None:
        self.refresh_status()


    async def refresh_status(self) -> None:
        proc = subprocess.run(
            ["git", "status", "--porcelain"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True
        )
        lines = proc.stdout.splitlines()
        # parse lines into staged_files & unstaged_files as before…
        staged_files, unstaged_files = parse(lines)  # your parsing helper
        self.notify("\n".join(staged_files))
        self.notify("\n".join(unstaged_files))
        self.staged_files=staged_files
        self.unstaged_files=unstaged_files

        # now actually rebuild the Tree
        await self._rebuild_tree()

    async def _add_tree_nodes(self, parent, subtree: Dict):
        """
        Recursively mount nodes under `parent` (a TreeNode).
        """
        for name, entry in subtree.items():
            if isinstance(entry, dict) and "__path__" in entry:
                # leaf
                label = f"[x] {name}" if entry["staged"] else f"[ ] {name}"
                node = await parent.add(label, expand=False)
                node.data = {"path": entry["__path__"], "staged": entry["staged"]}
            else:
                # folder
                branch = await parent.add(name, expand=True)
                await self._add_tree_nodes(branch, entry)

    async def _rebuild_tree(self) -> None:
        """Populate the Tree from our parsed file‐tree."""
        # 1) get porcelain lines
        proc = subprocess.run(
            ["git", "status", "--porcelain"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True
        )
        lines = proc.stdout.splitlines()
        # 2) parse into nested dict
        file_tree = _parse_porcelain(lines)
        # 3) clear & build Tree widget
        tree = self.query_one("#git-tree", Tree)
        tree.root.label = "Git Changes"
        tree.root.clear()
        await self._add_tree_nodes(tree.root, file_tree)
        tree.show_root = False
        await tree.root.expand()

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """Toggle stage/unstage when the user clicks a file node."""
        node = event.node
        data = node.data or {}
        path = data.get("path")
        staged = data.get("staged")
        if not path or staged is None:
            return

        if staged:
            subprocess.run(["git", "reset", "HEAD", path])
        else:
            subprocess.run(["git", "add", path])

        self.refresh_status()

    def action_commit(self) -> None:
        """Stage per tree, then commit -m message."""
        msg = self.query_one("#git-commit-msg", TextArea).text.strip()
        if not msg:
            return

        subprocess.run(["git", "commit", "-m", msg])
        # clear the message box
        self.query_one("#git-commit-msg", TextArea).text = ""
        # refresh the tree
        self.refresh_status()
        # notify or emit message
        self.post_message(self.Commit(msg, self.staged_files))
