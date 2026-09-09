from dataclasses import dataclass
from datetime import datetime

from PySide6.QtCore import QRect, QSize, Qt, Signal
from PySide6.QtGui import QBrush, QColor, QPainter, QPalette, QPen
from PySide6.QtWidgets import QSizePolicy, QToolTip, QWidget

from core.parser.event_log import CombatSegment


@dataclass(frozen=True)
class TimelineSection:
    kind: str
    start: datetime
    end: datetime
    segment_index: int | None = None

    @property
    def duration_seconds(self) -> int:
        return max(0, round((self.end - self.start).total_seconds()))


class CombatTimeline(QWidget):
    selection_changed = Signal(object)

    BAR_HEIGHT = 36
    MIN_COMBAT_WIDTH = 110
    MIN_GAP_WIDTH = 90

    def __init__(self, parent=None):
        super().__init__(parent)
        self._segments: list[CombatSegment] = []
        self._hit_areas: list[tuple[QRect, int]] = []
        self._selected_section_indexes: set[int] = set()
        self._drag_section_index: int | None = None
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumHeight(82)
        self.setAccessibleName("Временная шкала боя")

    def set_segments(self, segments: list[CombatSegment]):
        self._segments = list(segments)
        self._hit_areas.clear()
        self._drag_section_index = None
        self._selected_section_indexes.clear()
        sections = self._sections()
        minimum_width = sum(
            self.MIN_GAP_WIDTH if section.kind == "gap" else self.MIN_COMBAT_WIDTH
            for section in sections
        )
        self.setMinimumWidth(max(560, minimum_width + 16))
        self.updateGeometry()
        self.update()

    def clear_selection(self):
        self._drag_section_index = None
        self._selected_section_indexes.clear()
        self.update()

    def selected_sections(self) -> list[TimelineSection]:
        sections = self._sections()
        return [
            sections[index]
            for index in sorted(self._selected_section_indexes)
            if index < len(sections)
        ]

    def sizeHint(self):
        return QSize(max(720, self.minimumWidth()), 82)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._hit_areas.clear()

        if not self._segments:
            self._paint_empty_state(painter)
            return

        sections = self._sections()
        combat_duration = sum(round(segment.duration.total_seconds()) for segment in self._segments)
        gap_duration = sum(section.duration_seconds for section in sections if section.kind == "gap")
        summary = (
            f"Отрезков боя: {len(self._segments)}  •  "
            f"время боя: {self._format_duration(combat_duration)}  •  "
            f"паузы: {self._format_duration(gap_duration)}"
        )
        painter.setPen(self.palette().color(self.foregroundRole()))
        painter.drawText(QRect(8, 2, self.width() - 16, 20), Qt.AlignmentFlag.AlignVCenter, summary)

        bar_rect = QRect(8, 25, self.width() - 16, self.BAR_HEIGHT)
        widths = self._section_widths(sections, bar_rect.width())
        x = bar_rect.left()
        for section_index, (section, width) in enumerate(zip(sections, widths)):
            rect = QRect(x, bar_rect.top(), width, bar_rect.height())
            self._paint_section(painter, rect, section, section_index)
            x += width

        first = self._segments[0].start.strftime("%H:%M:%S")
        last = self._segments[-1].end.strftime("%H:%M:%S")
        painter.setPen(self.palette().color(self.foregroundRole()))
        painter.drawText(QRect(8, 63, 100, 17), Qt.AlignmentFlag.AlignLeft, first)
        painter.drawText(
            QRect(self.width() - 108, 63, 100, 17),
            Qt.AlignmentFlag.AlignRight,
            last,
        )

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_section_index = None
            for rect, section_index in self._hit_areas:
                if rect.contains(event.position().toPoint()):
                    self._drag_section_index = section_index
                    selection = {section_index}
                    if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                        selection |= self._selected_section_indexes
                    self._set_selection(selection)
                    QToolTip.hideText()
                    event.accept()
                    return
        super().mousePressEvent(event)

    def _set_selection(self, indexes: set[int]):
        if indexes != self._selected_section_indexes:
            self._selected_section_indexes = indexes
            self.update()
            self.selection_changed.emit(self.selected_sections())

    def _extend_drag_selection(self, position):
        for rect, section_index in self._hit_areas:
            if rect.contains(position):
                first, last = sorted((self._drag_section_index, section_index))
                self._drag_section_index = section_index
                self._set_selection(
                    self._selected_section_indexes | set(range(first, last + 1))
                )
                return

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self._drag_section_index is not None:
            self._extend_drag_selection(event.position().toPoint())
            self._drag_section_index = None
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        position = event.position().toPoint()
        if self._drag_section_index is not None:
            if event.buttons() & Qt.MouseButton.LeftButton:
                self._extend_drag_selection(position)
                QToolTip.hideText()
                event.accept()
                return
            self._drag_section_index = None
        sections = self._sections()
        for rect, section_index in self._hit_areas:
            if not rect.contains(position):
                continue
            section = sections[section_index]
            selection_hint = (
                "Нажмите, чтобы выбрать только этот отрезок\n"
                "Ctrl + щелчок — добавить к выбору\n"
                "Удерживайте левую кнопку и ведите мышь, чтобы выбрать несколько отрезков"
            )
            if section.kind == "combat":
                segment_index = section.segment_index or 0
                segment = self._segments[segment_index]
                tooltip = (
                    f"Бой {segment_index + 1}\n"
                    f"{section.start:%H:%M:%S} — {section.end:%H:%M:%S}\n"
                    f"Длительность: {self._format_duration(section.duration_seconds)}\n"
                    f"Записей: {segment.end_index - segment.start_index + 1}\n"
                    f"{selection_hint}"
                )
            else:
                tooltip = (
                    "Пауза\n"
                    f"{section.start:%H:%M:%S} — {section.end:%H:%M:%S}\n"
                    f"Длительность: {self._format_duration(section.duration_seconds)}\n"
                    f"{selection_hint}"
                )
            QToolTip.showText(
                event.globalPosition().toPoint(),
                tooltip,
                self,
                rect,
            )
            return
        QToolTip.hideText()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        QToolTip.hideText()
        super().leaveEvent(event)

    def _paint_empty_state(self, painter: QPainter):
        rect = QRect(8, 18, self.width() - 16, 42)
        palette = self.palette()
        painter.setPen(
            QPen(palette.color(QPalette.ColorRole.Mid), 1, Qt.PenStyle.DashLine)
        )
        painter.setBrush(palette.color(QPalette.ColorRole.Base))
        painter.drawRoundedRect(rect, 4, 4)
        painter.setPen(palette.color(QPalette.ColorRole.PlaceholderText))
        painter.drawText(
            rect,
            Qt.AlignmentFlag.AlignCenter,
            "Загрузите лог боя, чтобы увидеть временную шкалу",
        )

    def _paint_section(
        self,
        painter: QPainter,
        rect: QRect,
        section: TimelineSection,
        section_index: int,
    ):
        inner_rect = rect.adjusted(1, 0, -1, 0)
        palette = self.palette()
        selected = section_index in self._selected_section_indexes
        if section.kind == "gap":
            background = palette.color(QPalette.ColorRole.Base)
            border = palette.color(
                QPalette.ColorRole.Text if selected else QPalette.ColorRole.Mid
            )
            text_color = palette.color(QPalette.ColorRole.Text)
            hatch_color = QColor(palette.color(QPalette.ColorRole.Mid))
            hatch_color.setAlpha(110)

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(background)
            painter.drawRoundedRect(inner_rect, 3, 3)
            painter.setPen(QPen(border, 3 if selected else 1))
            painter.setBrush(QBrush(hatch_color, Qt.BrushStyle.BDiagPattern))
            label = f"Пауза {self._format_duration(section.duration_seconds)}"
        else:
            segment_index = section.segment_index or 0
            color = self._combat_color(segment_index)
            border = palette.color(
                QPalette.ColorRole.Text if selected else QPalette.ColorRole.Mid
            )
            text_color = palette.color(QPalette.ColorRole.ButtonText)
            painter.setPen(QPen(border, 3 if selected else 1))
            painter.setBrush(color)
            label = f"Бой {segment_index + 1} · {self._format_duration(section.duration_seconds)}"

        painter.drawRoundedRect(inner_rect, 3, 3)
        self._hit_areas.append((rect, section_index))
        painter.setPen(text_color)
        label = painter.fontMetrics().elidedText(
            label,
            Qt.TextElideMode.ElideRight,
            max(0, inner_rect.width() - 10),
        )
        painter.drawText(inner_rect.adjusted(5, 0, -5, 0), Qt.AlignmentFlag.AlignCenter, label)

    def _combat_color(self, segment_index: int) -> QColor:
        color = QColor(self.palette().color(QPalette.ColorRole.Button))
        if segment_index % 2:
            return color.lighter(112) if color.lightness() < 128 else color.darker(106)
        return color

    def _sections(self) -> list[TimelineSection]:
        sections = []
        for index, segment in enumerate(self._segments):
            if index:
                previous = self._segments[index - 1]
                sections.append(TimelineSection("gap", previous.end, segment.start))
            sections.append(TimelineSection("combat", segment.start, segment.end, index))
        return sections

    def _section_widths(self, sections: list[TimelineSection], available_width: int) -> list[int]:
        minimum_widths = [
            self.MIN_GAP_WIDTH if section.kind == "gap" else self.MIN_COMBAT_WIDTH
            for section in sections
        ]
        minimum_total = sum(minimum_widths)
        if minimum_total >= available_width:
            widths = minimum_widths
        else:
            weights = [max(1, section.duration_seconds) for section in sections]
            remaining = available_width - minimum_total
            weight_total = sum(weights)
            widths = [
                minimum + round(remaining * weight / weight_total)
                for minimum, weight in zip(minimum_widths, weights)
            ]

        if widths:
            widths[-1] += available_width - sum(widths)
        return widths

    @staticmethod
    def _format_duration(seconds: float) -> str:
        total_seconds = max(0, round(seconds))
        minutes, seconds = divmod(total_seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"
