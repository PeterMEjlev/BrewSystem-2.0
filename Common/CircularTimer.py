# circular_timer.py

import os
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore    import Qt, QTimer, QRectF, QSize
from PyQt5.QtGui     import QPainter, QPen, QColor, QFont, QPixmap
import sys

# defaults:
DEFAULT_DURATION      = 60.0
DEFAULT_BG_COLOR      = "#313132"
DEFAULT_FG_COLOR      = "#FFFFFF"
DEFAULT_STROKE_WIDTH  = 7
DEFAULT_TEXT_SCALE    = 0.15  # fraction of diameter
DEFAULT_TEXT_SIZE     = None  # if set, overrides text_scale
DEFAULT_ICON_SCALE    = 0.5   # fraction of inner circle diameter
ICON_FILENAME         = "Icon_Timer.png"

class CircularTimer(QWidget):
    def __init__(
        self,
        duration_minutes: float = DEFAULT_DURATION,
        parent=None,
        bg_color: str = DEFAULT_BG_COLOR,
        fg_color: str = DEFAULT_FG_COLOR,
        stroke_width: int = DEFAULT_STROKE_WIDTH,
        text_scale: float = DEFAULT_TEXT_SCALE,
        text_size: int  = DEFAULT_TEXT_SIZE,
        icon_scale: float = DEFAULT_ICON_SCALE,
    ):
        super().__init__(parent)
        self.duration       = duration_minutes
        self.elapsed        = 0.0
        self.bg_qcolor      = QColor(bg_color)
        self.fg_qcolor      = QColor(fg_color)
        self.stroke_width   = stroke_width
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        # text-size controls
        self.text_scale     = text_scale
        self.text_size      = text_size
        # icon-sizing
        self.icon_scale     = icon_scale

        # only show text after start() is called
        self._show_text     = False

        # load icon pixmap
        base_path = os.path.join(os.path.dirname(__file__), "..", "Assets")
        icon_path = os.path.join(base_path, ICON_FILENAME)
        self._icon_pixmap = QPixmap(icon_path)
        self._icon_label  = QLabel(self)
        self._icon_label.setAttribute(Qt.WA_TranslucentBackground)
        self._icon_label.setScaledContents(False)

        # timer for auto‐tick every second
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._on_tick)

    def sizeHint(self):
        return QSize(100, 100)

    def start(self):
        """Begin ticking and show the minutes label."""
        self.elapsed    = 0.0
        self._show_text = True
        self._icon_label.hide()
        self._timer.start(1000)
        self.update()

    def stop(self):
        self._timer.stop()

    def toggle(self):
        """
        Toggle between running and paused.  
        - If currently active, stops (pauses),  
        - otherwise resumes (or starts) and shows text.
        """
        if self._timer.isActive():
            self.stop()
        else:
            self._show_text = True
            self._icon_label.hide()
            self._timer.start(1000)
        self.update()
        
    def reset(self):
        """
        Reset the timer back to its initial (idle) state:
        - stops any running countdown,
        - clears elapsed time,
        - hides the minutes text,
        - shows the icon again,
        - repaints.
        """
        self._timer.stop()
        self.elapsed = 0.0
        self._show_text = False
        self._icon_label.show()
        self.update()


    def setElapsed(self, minutes: float):
        self.elapsed = max(0.0, minutes)
        if self.elapsed > self.duration:
            self.elapsed = self.duration
        self.update()

    def setTextScale(self, scale: float):
        self.text_scale = scale
        self.update()

    def setTextSize(self, pt_size: int):
        self.text_size = pt_size
        self.update()

    def _on_tick(self):
        self.elapsed += 1.0/60.0
        if self.elapsed >= self.duration:
            self.elapsed = self.duration
            self._timer.stop()
        self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_icon_geometry()

    def _update_icon_geometry(self):
        # center icon inside inner circle
        size     = min(self.width(), self.height())
        margin   = size * 0.1 + self.stroke_width/2
        inner    = size - 2 * margin
        icon_sz  = int(inner * self.icon_scale)
        if self._icon_pixmap and icon_sz > 0:
            scaled = self._icon_pixmap.scaled(
                icon_sz, icon_sz,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self._icon_label.setPixmap(scaled)
            w, h = scaled.width(), scaled.height()
            x = (self.width()  - w) // 2
            y = (self.height() - h) // 2
            self._icon_label.setGeometry(x, y, w, h)
            self._icon_label.show() if not self._show_text else self._icon_label.hide()

    def paintEvent(self, event):
        size   = min(self.width(), self.height())
        margin = size * 0.1
        rect   = QRectF(margin, margin, size - 2*margin, size - 2*margin)

        # ensure icon is properly positioned
        if not self._show_text:
            self._update_icon_geometry()

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)


        # background circle: white until started, then use configured bg_color
        bg_pen_color = QColor("#FFFFFF") if not self._show_text else self.bg_qcolor
        p.setPen(QPen(bg_pen_color, self.stroke_width))
        p.drawEllipse(rect)

        # progress arc
        p.setPen(QPen(self.fg_qcolor, self.stroke_width, cap=Qt.RoundCap))
        pct        = min(self.elapsed / self.duration, 1.0)
        span_angle = int(-pct * 360 * 16)
        p.drawArc(rect, -90 * 16, span_angle)

        # only draw the minutes text after `start()` has been called
        if self._show_text:
            minutes  = int(self.elapsed)
            time_str = f"{minutes:01} min"

            if self.text_size is not None:
                pt = self.text_size
            else:
                pt = max(1, int(size * self.text_scale))

            font = QFont()
            font.setBold(True)
            font.setPointSize(pt)
            p.setFont(font)
            p.setPen(self.fg_qcolor)
            p.drawText(rect, Qt.AlignCenter, time_str)


def create_circular_timer(
    duration_minutes: float = DEFAULT_DURATION,
    parent=None,
    **kwargs
) -> CircularTimer:
    return CircularTimer(duration_minutes=duration_minutes, parent=parent, **kwargs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = create_circular_timer(
        30,
        None,
        bg_color="#313132",
        fg_color="#FFFFFF",
        stroke_width=10,
        text_scale=0.25,
        icon_scale=0.25
    )
    w.resize(150, 150)
    w.show()
    # text will remain hidden until .start()
    QTimer.singleShot(2000, w.start)
    sys.exit(app.exec_())
