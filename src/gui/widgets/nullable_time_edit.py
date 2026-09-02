from datetime import time as PythonTime

from PySide6.QtCore import QTime, Signal
from PySide6.QtWidgets import QTimeEdit


class NullableTimeEdit(QTimeEdit):
    """QTimeEdit, в котором отсутствие границы обозначается прочерком."""

    valueChanged = Signal(object)
    EMPTY_TIME = QTime(0, 0, 0, 0)
    MIDNIGHT_TIME = QTime(0, 0, 0, 1)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._has_value = False
        self._updating = False
        self._last_emitted_value = None
        self.setDisplayFormat("HH:mm:ss")
        self.setSpecialValueText("—")
        self.setAccelerated(True)
        self.lineEdit().setPlaceholderText("00:00:00")
        self.timeChanged.connect(self._on_time_changed)
        self.lineEdit().textEdited.connect(self._on_text_edited)
        self.setValue(None)

    def value(self) -> PythonTime | None:
        if not self._has_value:
            return None
        value = self.time()
        return PythonTime(value.hour(), value.minute(), value.second())

    def setValue(self, value: PythonTime | QTime | None):
        self._updating = True
        try:
            if value is None:
                self._has_value = False
                self.setTime(self.EMPTY_TIME)
            else:
                qt_time = (
                    value
                    if isinstance(value, QTime)
                    else QTime(value.hour, value.minute, value.second)
                )
                if qt_time == self.EMPTY_TIME:
                    qt_time = self.MIDNIGHT_TIME
                self._has_value = True
                self.setTime(qt_time)
        finally:
            self._updating = False
        self._emit_value_if_changed()

    def clear(self):
        if not hasattr(self, "_updating"):
            super().clear()
            return
        self.setValue(None)

    def stepBy(self, steps: int):
        if not self._has_value:
            self.setValue(PythonTime())
        super().stepBy(steps)
        self._emit_value_if_changed()

    def _on_time_changed(self, value: QTime):
        if self._updating:
            return
        if value == self.EMPTY_TIME:
            self.setValue(PythonTime())
            return
        self._has_value = True
        self._emit_value_if_changed()

    def _on_text_edited(self, text: str):
        if not text.strip() or text == self.specialValueText():
            self.setValue(None)
            return

        parsed_time = QTime.fromString(text, self.displayFormat())
        if parsed_time.isValid() and parsed_time == self.EMPTY_TIME:
            self.setValue(PythonTime())

    def _emit_value_if_changed(self):
        value = self.value()
        if value == self._last_emitted_value:
            return
        self._last_emitted_value = value
        self.valueChanged.emit(value)
