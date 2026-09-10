from PySide6.QtCore import QEvent, Qt, Signal
from PySide6.QtWidgets import QApplication, QStyle, QStyledItemDelegate, QStyleOptionViewItem


class OriginalMessageDelegate(QStyledItemDelegate):
    message_clicked = Signal(str)

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.Type.MouseButtonRelease and event.button() == Qt.MouseButton.LeftButton:
            item_option = QStyleOptionViewItem(option)
            self.initStyleOption(item_option, index)
            style = item_option.widget.style() if item_option.widget else QApplication.style()
            icon_rect = style.subElementRect(
                QStyle.SubElement.SE_ItemViewItemDecoration, item_option, item_option.widget,
            )
            if icon_rect.contains(event.position().toPoint()):
                message = index.data(Qt.ItemDataRole.ToolTipRole)
                if message:
                    self.message_clicked.emit(message)
                    return True
        return super().editorEvent(event, model, option, index)
