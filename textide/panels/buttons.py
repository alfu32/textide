from typing import Literal, Text

from textual.widgets import Button
from textual import events

class SmallButton(Button):
    """A Button with no padding or border—just text."""
    DEFAULT_CSS = """
    SmallButton {
        padding: 0;
        border: none;
    }
    /* highlight on hover or focus */
    SmallButton:hover,
    SmallButton:focus {
        background: $accent;
        color: $text;
    }
    """

    def __init__(self,  label: Text | str | None = None,
             variant: Literal["default", "primary", "success", "warning", "error"] = "default",
             *,
             name: str | None = None,
             id: str | None = None,
             classes: str | None = None,
             disabled: bool = False,
             tooltip: str | None = None,
             action: str | None = None,
             compact: bool = False) -> None:
        super().__init__(
            label=label,
            variant=variant,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
            tooltip=tooltip,
            action=action,
            compact=compact,
        )