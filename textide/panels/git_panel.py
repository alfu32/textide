# textide/panels/git_panel.py
import asyncio
import subprocess
from pathlib import Path
from typing import List, Set

from textual.app import ComposeResult
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, ListView, ListItem,TextArea,Button
from textual.containers import Vertical
from asyncio import Future, ensure_future,Task
from git import Repo,Commit
def to_uint64(n: int) -> int:
    # mask to lowest 64 bits
    return n & ((1 << 64) - 1)
def line_id(line:str)->str:
    return f"{to_uint64(hash(line)):016x}"
class GitPanel(Widget, can_focus=True):
    """A minimal git panel: status lines as selectable items + key bindings."""

    BINDINGS = [
        ("r", "refresh", "Refresh"),
        ("a", "stage",   "Stage"),
        ("u", "unstage", "Unstage"),
        ("c", "commit",  "Commit"),
        ("p", "push",    "Push"),
        ("m", "copy_commit_message",    "Copy Message"),
    ]

    class Refreshed(Message): pass
    class Staged(Message):    pass
    class Unstaged(Message):  pass
    class Committed(Message): pass
    class Pushed(Message):    pass

    branch:       reactive[str]     = reactive("")
    path:Path = Path('.')
    repo = Repo('.')
    selected_commit:Commit = None

    # which lines are toggled on
    selected: reactive[Set[str]]     = reactive(set())

    def __init__(self, path: Path = Path.cwd(), **kwargs):
        super().__init__(**kwargs)
        self.path=path

    def compose(self) -> ComposeResult:
        with Vertical(id="git-panel-container"):
            yield Label(f"Branch: {self.branch}", id="git-panel-branch")
            yield Vertical(id="git-panel-changes")
            yield Label(f"Commit Message", id="git-panel-commit-message-title")
            yield TextArea(text="",id="git-panel-commit-message")
            yield Vertical(id="git-panel-commits")

    def on_mount(self) -> None:
        self.action_refresh()

    def action_refresh(self) -> None:
        """Reload `git status` and current branch."""
        self.repo = Repo(self.path)
        # branch
        # drop selections no longer present
        self._rebuild_lists()
        self.post_message(self.Refreshed())

    def _rebuild_lists(self) -> None:
        tx = self.query_one("#git-panel-commit-message", TextArea)
        lab = self.query_one("#git-panel-branch", Label)
        lv = self.query_one("#git-panel-changes", Vertical)
        com = self.query_one("#git-panel-commits", Vertical)
        lab.update(f"Branch: {self.repo.active_branch.name}")
        def on_remove_done_diffs(task: asyncio.Task):
            for ix,line in enumerate(self.repo.git.status('--porcelain').splitlines()):
                # self.notify(line)
                if line:
                    selected="✓ " if line in self.selected else "  "
                    classes="git-panel-file git-panel-file-selected" if line in self.selected else "git-panel-file"
                    item = Button(f"{selected}{line}", name=f"diff:{ix}", tooltip=f"diff:{line_id(line)}",classes=classes, compact=True)
                    lv.mount(item)
        def on_remove_done_commits(task: asyncio.Task):
            for ix,commit in enumerate(self.repo.iter_commits(self.repo.active_branch.name, max_count=10)):
                # self.notify(commit.hexsha)
                if commit:
                    selected="•" if self.selected_commit and commit.hexsha ==self.selected_commit.hexsha else "○"
                    btext=f"{selected}{commit.hexsha[0:7]}: {commit.message.splitlines()[0]}"
                    item = Button(btext, name=f"commit:{ix}", tooltip=f"commit:{commit.hexsha}",classes="git-panel-commit",compact=True)
                    com.mount(item)
        if len(lv.children):
            task = asyncio.ensure_future(lv.remove_children('*'))
            task.add_done_callback(on_remove_done_diffs)
        else:
            on_remove_done_diffs(None)
        if len(com.children):
            task = asyncio.ensure_future(com.remove_children('*'))
            task.add_done_callback(on_remove_done_commits)
        else:
            on_remove_done_commits(None)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Toggle selection on click/enter."""
        line = event.item.id
        if line in self.selected:
            self.selected.remove(line)
        else:
            self.selected.add(line)
        self._rebuild_lists()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        name = event.button.name
        if name and name.startswith("diff:"):
            ix = int(event.button.name.replace("diff:", ""))
            key = self.repo.git.status('--porcelain').splitlines()[ix]
            if key in self.selected:
                self.selected.remove(key)
                self.notify(f"{key} is de-selected")
            else:
                self.selected.add(key)
                self.notify(f"{key} is selected")
            self._rebuild_lists()
        elif name and name.startswith("commit:"):
            ix = int(event.button.name.replace("commit:", ""))
            com:Commit = None
            for i,c in enumerate(self.repo.iter_commits(self.repo.active_branch.name, max_count=10)):
                if i== ix:
                    com:Commit = c
                    break
            # a tab button—name is the full path
            self.selected_commit = com
            tx = self.query_one("#git-panel-commit-message", TextArea)
            tx.text = com.message
            self.notify(f"{com.hexsha} is selected")
            self._rebuild_lists()
        event.stop()

    def action_stage(self) -> None:
        """git add <selected paths>."""
        paths = [l[3:] for l in self.selected]
        if paths:
            subprocess.run(["git", "add", *paths])
            self.post_message(self.Staged())
            self.action_refresh()
    def action_copy_commit_message(self) -> None:
        """git add <selected paths>."""
        paths = [l[3:] for l in self.selected]
        if paths:
            subprocess.run(["git", "add", *paths])
            self.post_message(self.Staged())
            self.action_refresh()

    def action_unstage(self) -> None:
        """git reset HEAD <selected paths>."""
        paths = [l[3:] for l in self.selected]
        if paths:
            subprocess.run(["git", "reset", "HEAD", *paths])
            self.post_message(self.Unstaged())
            self.action_refresh()

    def action_commit(self) -> None:
        """git commit (opens editor)."""
        ct:TextArea = self.query_one("#git-panel-commit-message", TextArea)
        subprocess.run(["git", "commit", "-m", ct.text])
        self.post_message(self.Committed())
        self.action_refresh()

    def action_push(self) -> None:
        """git push."""
        subprocess.run(["git", "push"])
        self.post_message(self.Pushed())
        self.action_refresh()
