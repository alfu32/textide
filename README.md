# requirements

The bottom line is that I want an editor that has roughly the same functionality as VS Code, but is written in Python, renders to console/VT/TUI. And the functionality I'm referring about is to have the left-hand panel with a list of open files and also on the left-hand panel the current project. On the content panel I want to see the code editor with highlighted syntax and supporting navigating with the mouse and also supporting alt-click for multiple carets. And also to be able to integrate it with LSP servers to support text-made syntax. And also a second left-hand panel that will support listing git commits and committing with a text message.


__
There isn’t yet a drop-in, VS Code-equivalent TUI IDE written entirely in Python — but you can assemble one from Python building blocks. Here’s how you’d stitch together the pieces you need:
__

## 1. Panel layout and rendering
Textual (by Will McGugan)

A high-level TUI framework using Rich for styling.

Allows you to define resizable panels (file tree, git panel, editor pane).

Handles mouse input and key bindings out of the box.

## 2. File / project explorer
Use Textual’s TreeControl widget to build your project/file tree on the left.

Hook selection events to load files into your editor buffer.

## 3. Code editor widget
prompt_toolkit

Its Buffer + Document model gives you syntax highlighting, multiline editing, multi-cursor support (via its “multiple cursors” extension).

You can embed a PromptToolkit Application inside a Textual panel via a custom widget.

## 4. Syntax highlighting
Use Pygments lexers hooked into prompt_toolkit’s Lexer interface.

## most of it is ready

## 5. LSP integration
python-lsp-jsonrpc + python-lsp-server

Spin up an LSP server process (e.g. pylsp, clangd, etc.).

## ok baby

Send/receive JSON-RPC messages to power “go to definition,” diagnostics, auto-complete.

Or leverage textual-lsp (community project) which wraps much of this boilerplate.

## 6. Multi-carets & mouse support
prompt_toolkit’s built-in mouse support lets you click to position the cursor.

Its multi-cursor extension (prompt_toolkit.shortcuts.multi_cursor) supports Alt+Click to add new carets.

## 7. Git panel
On a second left panel, use Textual’s ListView to show recent commits (git log --oneline).

Provide an input box (Textual Input) for commit messages, then on submit run git commit via Python’s subprocess.

## Putting it all together

Layout

Top-level Grid / Dock layout in Textual:

Left TreeControl (files & commits stacked vertically).

Center EditorWidget (prompt_toolkit editor).

Event wiring

File selection loads buffer.

Text edits send LSP notifications for textDocument/didChange.

Mouse and keybindings handled by prompt_toolkit.

Packaging

Bundle as a single Python package.

Entry point launches your Textual App.

## scaffolding:


```
.
├── README.md
├── requirements.txt
└── textide
    ├── app.css
    ├── app.py
    ├── lsp
    │   └── client.py
    ├── __main__.py
    └── panels
        ├── editor.py
        ├── editor_screen.py
        ├── file_tree.py
        └── git_panel.py
```