from PySide6.QtCore import QEvent
from PySide6.QtWidgets import QScrollArea


class FilterScrollArea(QScrollArea):
    """Keep filter labels visible when the application font or style changes."""

    def setWidget(self, widget):
        previous = self.widget()
        if previous is not None:
            previous.removeEventFilter(self)
        super().setWidget(widget)
        widget.installEventFilter(self)
        self._update_minimum_width()

    def eventFilter(self, watched, event):
        if watched is self.widget() and event.type() in (
            QEvent.Type.LayoutRequest,
            QEvent.Type.FontChange,
            QEvent.Type.StyleChange,
            QEvent.Type.Show,
        ):
            self._update_minimum_width()
        return super().eventFilter(watched, event)

    def _update_minimum_width(self):
        widget = self.widget()
        if widget is not None:
            self.setMinimumWidth(widget.minimumSizeHint().width() + 2 * self.frameWidth())
