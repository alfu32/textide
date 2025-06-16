from pathlib import Path

from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Input, Log
from textual.containers import Vertical
from textual import work
import asyncio


class Shell(Widget):
    CSS = """
    Input {
        border: tall $accent;
        height: 3;
    }
    TextLog {
        background: $panel;
    }
    """
    path:Path | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        yield Vertical(
            Log(id="log", highlight=True, auto_scroll=True),
            Input(placeholder="Enter command...", id="input"),
        )

    @work(thread=False)
    async def run_command(self, command: str) -> None:
        log = self.query_one("#log", Log)
        log.write(f"$ {command}")

        try:
            proc = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True,
            )
            stdout, stderr = await proc.communicate()

            if stdout:
                log.write(stdout.decode())
            if stderr:
                log.write(f"[stderr] {stderr.decode()}") # , style="red"
        except Exception as e:
            log.write(f"[error] {e}") # , style="bold red"

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        command = event.value.strip()
        event.input.value = ""
        if command:
            self.run_command(command)


if __name__ == "__main__":
    PseudoShell().run()
