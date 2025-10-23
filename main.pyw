import sys

from core.application import Application

if __name__ == "__main__":
    app = Application(sys.argv)
    exit_code = app.exec()
    app.logger.info("Завершение приложения.")
    sys.exit(exit_code)
