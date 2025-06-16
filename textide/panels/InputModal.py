from textual.screen import ModalScreen
from textual.widgets import Input, Label, Button
from textual.containers import Vertical, Horizontal
from textual.message import Message

class InputModal(ModalScreen):
    class Submitted(Message):
        def __init__(self, sender, value: str):
            self.value = value
            super().__init__(sender)

    def __init__(self, title: str, placeholder: str = "", default: str = ""):
        super().__init__(id="input-modal")
        self.title = title
        self.placeholder = placeholder
        self.default = default

    def compose(self):
        yield Vertical(
            Label(self.title),
            Input(placeholder=self.placeholder, value=self.default, id="input"),
            Horizontal(
                Button("OK", variant="success", id="ok",compact=True),
                Button("Cancel", variant="error", id="cancel",compact=True),
                id="buttons"
            ),
            id="modal"
        )

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "ok":
            val = self.query_one("#input", Input).value.strip()
            self.dismiss(val if val else None)
        else:
            self.dismiss(None)
