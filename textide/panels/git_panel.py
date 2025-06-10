# textide/panels/git_panel.py
from textual.widget import Widget
from textual.reactive import reactive
from rich.text import Text
import subprocess

class GitPanel(Widget):
    commits = reactive("")

    def on_mount(self):
        self.update_commits()

    def update_commits(self):
        try:
            output = subprocess.check_output(
                ["git", "log", "--oneline", "-n", "10"],
                stderr=subprocess.DEVNULL,
                text=True
            )
            self.commits = output.strip()
        except subprocess.CalledProcessError:
            self.commits = "Not a git repository."

    def render(self) -> Text:
        return Text(self.commits, style="cyan")
