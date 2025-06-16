# textide/main.py
import sys
from pathlib import Path

from textide.app import TextIDEApp

if __name__ == "__main__":
    print("starting application")
    TextIDEApp(base=Path(sys.argv[1] if len(sys.argv) >1 else ".")).run()
