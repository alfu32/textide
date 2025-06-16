# textide/panels/editors_panel.py
import asyncio
from operator import indexOf
from pathlib import Path
from typing import Dict, List

from textual.app import ComposeResult
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, Select, TextArea,Static, Footer
from textual.containers import Horizontal, Vertical
from textual.await_remove import AwaitRemove

from textide.panels.buttons import SmallButton
from textide.panels.languages import detect_language
from textide.utils import divide_list

MAX_VISIBLE_TABS = 4  # how many tabs before we start overflowing

class EditorsPanel(Widget):
    """A tab-bar + single code editor, with file-meta in memory."""

    BINDINGS = [("^s", "save_current_editor", "Save")]



    def action_save_current_editor(self) -> None:
        """Save the active editor’s contents back to its file."""
        path = self.active
        if not path:
            return  # nothing to save

        # grab the editor widget and its text
        editor: TextArea = self.query_one("#editor", TextArea)
        text = editor.text

        try:
            # write out to disk
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)

            # update our in-memory metadata
            meta = self._files[path]
            meta["content"] = text
            meta["is_saved"] = True

            # refresh the tab labels (to remove the • bullet)
            self._refresh_tabs()

            # optional: notify user
            self.notify(f"Saved {Path(path).name}", severity="information")

        except Exception as exc:
            # notify on error
            self.notify(f"Error saving {Path(path).name}: {exc}", severity="error")

    class FileClosed(Message):
        """Posted when a file tab is closed."""
        def __init__(self, path: str) -> None:
            self.path = path
            super().__init__()

    open_files: reactive[List[str]] = reactive([])
    active: reactive[str | None]    = reactive(None)

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        # path → { content, is_saved, cursor_pos }
        self._files: Dict[str, Dict] = {}

    def compose(self) -> ComposeResult:
        # Tab-bar row
        with Vertical(id="tab-horizontal"):
            yield Horizontal(id="tab-bar")
            # single underlying editor
            yield TextArea.code_editor(
                text="",
                language="python",
                id="editor",
                show_line_numbers=True,
                compact=True# scrollbar=True
            )

    def load_content(self, content: str, path: str) -> None:
        """Open (or focus) a file."""
        if path not in self._files:
            self._files[path] = {
                "content": content,
                "is_saved": True,
                "cursor": 0,
            }
            self.open_files.append(path)
        self._activate(path)

    def _activate(self, path: str) -> None:
        """Switch the editor to this path."""
        meta = self._files[path]
        editor = self.query_one("#editor", TextArea)
        editor.text = meta["content"]
        editor.language = detect_language(path,meta["content"])
        # TODO: restore cursor via editor.cursor_position = meta["cursor"]
        self.active = path
        self._refresh_tabs()

    def _refresh_tabs(self) -> None:
        bar = self.query_one("#tab-bar", Horizontal)
        # bar.clear()
        # schedule it:
        def on_remove_done(task: asyncio.Task):
            at=indexOf(self.open_files,self.active) if self.active else 0
            before,visible,after=divide_list(self.open_files,at,MAX_VISIBLE_TABS)

            if before:
                # use Select with Option tuples for before
                options = [(Path(p).name, p) for p in before]
                sel = Select(options, prompt="⋯", id="before",compact=True)
                bar.mount(sel)
            for p in visible:
                name = Path(p).name
                meta = self._files[p]
                label = f"{name}{'' if meta['is_saved'] else '•'}"
                btn = Button(label=label, name=f"select:{p}", classes="tab-name" if self.active!=p else "tab-name tab-selected",compact=True)
                bar.mount(btn)
                close = Button(label="×", name=f"close:{p}", classes="tab-close" if self.active!=p else "tab-close tab-selected",compact=True)
                bar.mount(close)
            if after:
                # use Select with Option tuples for after
                options = [(Path(p).name, p) for p in after]
                sel = Select(options, prompt="⋯", id="after",compact=True)
                bar.mount(sel)
        task = asyncio.ensure_future(bar.remove_children("*"))
        task.add_done_callback(on_remove_done)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        name = event.button.name
        if name and name.startswith("close:"):
            path = name.split(":", 1)[1]
            self._close(path)
        elif name and name.startswith("select:"):
            path = name.split(":", 1)[1]
            # a tab button—name is the full path
            if Path(path).suffix:
                self._activate(path)

    def on_select_changed(self, event: Select.Changed) -> None:
        # overflow → activate the selected value
        self._activate(event.value)

    def _close(self, path: str) -> None:
        self.open_files.remove(path)
        self._files.pop(path, None)
        self.post_message(self.FileClosed(path))
        if self.active == path:
            if self.open_files:
                self._activate(self.open_files[-1])
            else:
                # empty: blank out editor
                editor = self.query_one("#editor", TextArea)
                editor.text = ""
                self.active = None
        self._refresh_tabs()

    def on_key(self, event) -> None:
        # detect changes to mark unsaved
        if self.active:
            editor = self.query_one("#editor", TextArea)
            meta = self._files[self.active]
            meta["is_saved"] = (editor.text == meta["content"])
            self._refresh_tabs()

    class RefreshLSP(Message):
        """F5 pressed → ask for requery."""
        pass
