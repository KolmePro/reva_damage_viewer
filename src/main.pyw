import argparse
import os
import sys

from core.application import Application


def parse_args(argv):
    parser = argparse.ArgumentParser(description="DamageViewer")
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enable debug mode and debug-only UI actions.",
    )
    args, qt_args = parser.parse_known_args(argv[1:])
    env_debug = os.environ.get("DAMAGEVIEWER_DEBUG", "").lower() in {"1", "true", "yes", "on"}
    return args.debug or env_debug, [argv[0], *qt_args]


if __name__ == "__main__":
    debug_mode, qt_argv = parse_args(sys.argv)
    app = Application(qt_argv, debug_mode=debug_mode)
    exit_code = app.exec()
    app.logger.info("Завершение приложения.")
    sys.exit(exit_code)
