# textide/panels/editors_panel.py

from pathlib import Path
from typing import Dict, List

from textual.app import ComposeResult
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, Select, TextArea
from textual.containers import Horizontal, Vertical

MAX_VISIBLE_TABS = 6  # how many tabs before we start overflowing

class EditorsPanel(Widget):
    """A tab-bar + single code editor, with file-meta in memory."""

    class FileClosed(Message):
        """Posted when a file tab is closed."""
        def __init__(self, path: str) -> None:
            self.path = path
            super().__init__()

    open_files: reactive[List[str]] = reactive([])
    active: reactive[str | None]    = reactive(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # path → { content, is_saved, cursor_pos }
        self._files: Dict[str, Dict] = {}

    def compose(self) -> ComposeResult:
        # Tab-bar row
        with Vertical():
            yield Horizontal(id="tab-bar")
            # single underlying editor
            yield TextArea.code_editor(
                "", language="python", id="editor", show_line_numbers=True, # scrollbar=True
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
        editor.language = self._detect_language(path)
        # TODO: restore cursor via editor.cursor_position = meta["cursor"]
        self.active = path
        self._refresh_tabs()

    def _detect_language(self, path: str) -> str:
        ext = Path(path).suffix.lower().lstrip(".")
        return {
            "py": "python",
            "js": "javascript",
            "ts": "typescript",
            "html": "html",
            "css": "css",
        }.get(ext, "text")

    def _refresh_tabs(self) -> None:
        bar = self.query_one("#tab-bar", Horizontal)
        # bar.clear()

        visible = self.open_files[:MAX_VISIBLE_TABS]
        overflow = self.open_files[MAX_VISIBLE_TABS:]

        for p in visible:
            name = Path(p).name
            meta = self._files[p]
            label = f"{name}{'' if meta['is_saved'] else '•'}"
            btn = Button(label, name=p, variant=("primary" if p == self.active else "default"))
            bar.mount(btn)
            close = Button("×", name=f"close:{p}", variant="error")
            bar.mount(close)

        if overflow:
            # use Select with Option tuples for overflow
            options = [(Path(p).name, p) for p in overflow]
            sel = Select(options, prompt="⋯", id="overflow")
            bar.mount(sel)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        name = event.button.name
        if name and name.startswith("close:"):
            path = name.split(":", 1)[1]
            self._close(path)
        elif name and Path(name).suffix:
            # a tab button—name is the full path
            self._activate(name)

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
