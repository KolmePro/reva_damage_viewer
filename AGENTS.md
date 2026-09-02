# DamageViewer contributor guide

## Project overview

DamageViewer is a Windows desktop application for analyzing Revelation Online combat-log HTML files. It uses Python 3.10+ and PySide6; the application entry point is `src/main.pyw`.

## Environment and common commands

- Create and activate the virtual environment: `python -m venv .venv` then `./.venv/Scripts/Activate.ps1`.
- Install dependencies: `pip install -r requirements.txt`.
- Run the application: `python src/main.pyw`.
- Run the test suite: `python -m unittest discover -s tests`.
- Build the Windows executable: `pyinstaller main.spec`.
- After changing `src/gui/ui/main_window.ui`, regenerate `src/gui/compiled_ui/ui_main_window.py` with `cd tools; python compile_ui.py; cd ..`.

## Source layout

- `src/core/`: application orchestration, configuration, actions, logging, parsing, and plugin loading.
- `src/core/parser/`: combat-log parsing, record types, and table model logic.
- `src/gui/windows/`: window behavior and event wiring.
- `src/gui/widgets/`: reusable custom Qt widgets.
- `src/gui/ui/`: Qt Designer source files.
- `src/gui/compiled_ui/`: generated Python from Qt Designer sources; do not edit it by hand.
- `src/filter_plugins/`: dynamically loaded filter definitions. Follow `src/filter_plugins/README.md` when adding or changing a filter.
- `tests/`: unit and behavior tests using the standard library `unittest` framework.
- `tools/compile_ui.py`: UI-code generation helper.

## Implementation guidelines

- Keep parsing and data-model behavior independent of Qt where practical; cover it with tests in `tests/`.
- Preserve the existing plugin contract: filter modules expose their definitions through `FILTERS`.
- Treat log input as untrusted: tolerate malformed or unknown records without crashing the UI.
- Keep user-facing strings consistent with the Russian interface.
- Make UI changes in `.ui` files first, then regenerate the matching compiled module.
- Do not commit local build output, virtual environments, caches, or user-specific IDE settings.

## Validation

- Add or update focused tests for parser, filter, merge, selection, and state-management changes.
- Run `python -m unittest discover -s tests` before submitting changes.
- For UI changes, launch the app and verify the affected interaction manually in addition to unit tests.

## Working tree safety

- The worktree may contain changes from other contributors. Preserve unrelated edits and avoid reverting, reformatting, or regenerating files outside the requested scope.
