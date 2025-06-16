from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Button
from textual.containers import Horizontal,Vertical,Container

class VerticalTabs(Widget):
    def __init__(self, tabs: list[tuple[str, Widget]], **kwargs):
        super().__init__( **kwargs)
        self._tabs = tabs
        self._active = 0

    def compose(self) -> ComposeResult:
        # tab-button column
        with Horizontal(id="vertical-tab-parent"):
            with Vertical(id="vertical-tab-buttons"):
                for idx, (symbol, _) in enumerate(self._tabs):
                    yield Button(
                        symbol,
                        id=f"tab-{idx}", 
                        classes="vertical-tab-button" if idx!= self._active else "vertical-tab-button vertical-tab-button-active",
                        compact=True
                    )
            # the actual panes
            with Container(id="vertical-tabs-content"):
                for _, pane in self._tabs:
                    pane.display = False
                    yield pane

    def on_mount(self) -> None:
        # show the first pane by default
        self._tabs[0][1].display = True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        idx = int(event.button.id.split("-")[1])
        if idx == self._active:
            return
        # hide old, show new
        self._tabs[self._active][1].display = False
        self._tabs[idx][1].display = True
        self._active = idx