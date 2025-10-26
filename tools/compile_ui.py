from pathlib import Path
import subprocess


def compile_ui():
    ui_dir = Path("../src/gui/ui")
    out_dir = Path("../src/gui/compiled_ui")

    for ui_file in ui_dir.glob("*.ui"):
        out_file = out_dir / f"ui_{ui_file.stem}.py"
        subprocess.call(["pyside6-uic", str(ui_file), "-o", str(out_file)])
        print(f"Скомпилирован: {ui_file.name}")


if __name__ == "__main__":
    compile_ui()
