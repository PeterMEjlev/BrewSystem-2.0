# circular_timer.py

import os, sys, math
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGraphicsOpacityEffect
from PyQt5.QtCore    import Qt, QTimer, QRectF, QSize, QPointF
from PyQt5.QtGui     import QPainter, QPen, QColor, QFont, QPixmap
from typing import Callable, Optional

# ─── DEFAULT CONFIG ─────────────────────────────────────────────────────────────
DEFAULT_DURATION             = 60.0
DEFAULT_BG_COLOR_IDLE        = "#FFFFFF"
DEFAULT_BG_OPACITY_IDLE      = 1.0
DEFAULT_BG_COLOR_ACTIVE      = "#313132"
DEFAULT_BG_OPACITY_ACTIVE    = 1.0
DEFAULT_FG_COLOR             = "#FFFFFF"
DEFAULT_STROKE_WIDTH         = 6
DEFAULT_TEXT_SCALE           = 0.15
DEFAULT_TEXT_SIZE            = None
DEFAULT_ICON_SCALE           = 0.5
DEFAULT_ICON_IDLE_FILENAME   = "Icon_Timer.png"
DEFAULT_ICON_ACTIVE_FILENAME = "Icon_Timer_Grey.png"
DEFAULT_ICON_OPACITY_IDLE    = 1.0
DEFAULT_ICON_OPACITY_ACTIVE  = 1.0
# ────────────────────────────────────────────────────────────────────────────────

class CircularTimer(QWidget):
    def __init__(
        self,
        duration_minutes: float = DEFAULT_DURATION,
        parent=None,
        *,
        progress_callback: Optional[Callable[[float], None]] = None,
        bg_color_idle: str = DEFAULT_BG_COLOR_IDLE,
        bg_opacity_idle: float = DEFAULT_BG_OPACITY_IDLE,
        bg_color_active: str = DEFAULT_BG_COLOR_ACTIVE,
        bg_opacity_active: float = DEFAULT_BG_OPACITY_ACTIVE,
        fg_color: str = DEFAULT_FG_COLOR,
        stroke_width: int = DEFAULT_STROKE_WIDTH,
        text_scale: float = DEFAULT_TEXT_SCALE,
        text_size: int  = DEFAULT_TEXT_SIZE,
        icon_scale: float = DEFAULT_ICON_SCALE,
        icon_idle: str = DEFAULT_ICON_IDLE_FILENAME,
        icon_active: str = DEFAULT_ICON_ACTIVE_FILENAME,
        icon_opacity_idle: float = DEFAULT_ICON_OPACITY_IDLE,
        icon_opacity_active: float = DEFAULT_ICON_OPACITY_ACTIVE,
    ):
        super().__init__(parent)
        # timing
        self.duration = duration_minutes
        self.elapsed  = 0.0
        self._state = "idle"    # idle | running | paused
        self._progress_callback = progress_callback

        # background colors
        self.bg_color_idle   = QColor(bg_color_idle)
        self.bg_color_idle.setAlphaF(bg_opacity_idle)
        self.bg_color_active = QColor(bg_color_active)
        self.bg_color_active.setAlphaF(bg_opacity_active)

        # foreground (arc + text)
        self.fg_qcolor    = QColor(fg_color)
        self.stroke_width = stroke_width

        # text sizing
        self.text_scale = text_scale
        self.text_size  = text_size

        # icons
        self.icon_scale          = icon_scale
        self.icon_opacity_idle   = icon_opacity_idle
        self.icon_opacity_active = icon_opacity_active
        base = os.path.join(os.path.dirname(__file__), "..", "Assets")
        self._pix_idle   = QPixmap(os.path.join(base, icon_idle))
        self._pix_active = QPixmap(os.path.join(base, icon_active))

        # icon label
        self._icon_label = QLabel(self)
        self._icon_label.setAttribute(Qt.WA_TranslucentBackground)

        # state flags
        self._show_text     = False
        self._show_triangle = False

        # cache pixmaps and font
        self._bg_pixmap_idle   = None
        self._bg_pixmap_active = None
        self._font             = QFont()
        self._font.setBold(True)

        # ticking timer
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._on_tick)

        # click‐through
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

    def sizeHint(self):
        return QSize(100, 100)

    def start(self):
        """Start from zero, show text & run."""
        self._state = "running"
        self.elapsed        = 0.0
        self._show_text     = True
        self._show_triangle = False
        self._icon_label.hide()
        self._timer.start(1000)
        self.update()

    def stop(self, show_triangle: bool = True):
        self._state = "paused"
        self._timer.stop()
        if show_triangle:
            self._show_text     = False
            self._show_triangle = True
        else:
            self._show_text     = True
            self._show_triangle = False
        self._icon_label.hide()
        self.update()

    def toggle(self):
        if self._timer.isActive():
            self.stop()
        else:
            # resume
            self._show_text     = True
            self._show_triangle = False
            self._icon_label.hide()
            self._timer.start(1000)
            self._state = "running"

    def reset(self):
        """Back to idle: stop, clear, show idle icon."""
        self._state = "idle"
        self._timer.stop()
        self.elapsed        = 0.0
        self._show_text     = False
        self._show_triangle = False
        self._icon_label.show()
        self.update()

    def setElapsed(self, minutes: float):
        self.elapsed = min(max(0.0, minutes), self.duration)
        self.update()

    def setTextScale(self, scale: float):
        self.text_scale = scale
        self.update()

    def setTextSize(self, pt: int):
        self.text_size = pt
        self.update()

    def _on_tick(self):
        self.elapsed += 1/60.0
        if self.elapsed >= self.duration:
            self.elapsed = self.duration
            self._timer.stop()
        if self._progress_callback:
            self._progress_callback(math.floor(self.elapsed))
        self.update()

    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        size   = min(self.width(), self.height())
        margin = size * 0.1
        self._rect = QRectF(margin, margin, size - 2*margin, size - 2*margin)

        # cache idle background
        pix_idle = QPixmap(self.width(), self.height())
        pix_idle.fill(Qt.transparent)
        p = QPainter(pix_idle)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(QPen(self.bg_color_idle, self.stroke_width))
        p.drawEllipse(self._rect)
        p.end()
        self._bg_pixmap_idle = pix_idle

        # cache active background
        pix_act = QPixmap(self.width(), self.height())
        pix_act.fill(Qt.transparent)
        p2 = QPainter(pix_act)
        p2.setRenderHint(QPainter.Antialiasing)
        p2.setPen(QPen(self.bg_color_active, self.stroke_width))
        p2.drawEllipse(self._rect)
        p2.end()
        self._bg_pixmap_active = pix_act

        # update font size
        if self.text_size is not None:
            pt = self.text_size
        else:
            pt = max(1, int(size * self.text_scale))
        self._font.setPointSize(pt)

        # reposition icon if needed
        self._position_icon()

    def _position_icon(self):
        if self._show_text or self._show_triangle:
            self._icon_label.hide()
            return
        pix     = self._pix_idle
        opacity = self.icon_opacity_idle
        size   = min(self.width(), self.height())
        margin = size * 0.1 + self.stroke_width / 2
        inner  = size - 2 * margin
        isz    = int(inner * self.icon_scale)
        if not pix.isNull() and isz > 0:
            scaled = pix.scaled(isz, isz, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            w, h   = scaled.width(), scaled.height()
            x = (self.width() - w) // 2
            y = (self.height() - h) // 2
            self._icon_label.setPixmap(scaled)
            self._icon_label.setGeometry(x, y, w, h)
            eff = QGraphicsOpacityEffect(self._icon_label)
            eff.setOpacity(opacity)
            self._icon_label.setGraphicsEffect(eff)
            self._icon_label.show()

    def paintEvent(self, ev):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # draw cached background
        idle_state = (not self._show_text and not self._show_triangle)
        bg_pix = self._bg_pixmap_idle if idle_state else self._bg_pixmap_active
        if bg_pix:
            painter.drawPixmap(0, 0, bg_pix)
        else:
            bg = self.bg_color_idle if idle_state else self.bg_color_active
            painter.setPen(QPen(bg, self.stroke_width))
            painter.drawEllipse(self._rect)

        # draw progress arc
        painter.setPen(QPen(self.fg_qcolor, self.stroke_width, cap=Qt.RoundCap))
        pct  = min(self.elapsed / self.duration, 1.0)
        span = int(-pct * 360 * 16)
        painter.drawArc(self._rect, -90 * 16, span)

        # draw minutes text
        if self._show_text:
            mins = int(self.elapsed)
            text = f"{mins:01d} min"
            painter.setFont(self._font)
            painter.setPen(self.fg_qcolor)
            painter.drawText(self._rect, Qt.AlignCenter, text)

        # draw pause-triangle
        elif self._show_triangle:
            size   = min(self.width(), self.height())
            margin = size * 0.1
            inner  = size - 2 * margin
            s      = inner * 0.4
            cx, cy = self._rect.center().x(), self._rect.center().y()
            dx     = inner * 0.05
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.fg_qcolor)
            pts = [
                QPointF(cx - s/2 + dx, cy - s/2),
                QPointF(cx - s/2 + dx, cy + s/2),
                QPointF(cx + s/2 + dx, cy)
            ]
            painter.drawPolygon(*pts)

        painter.end()


def create_circular_timer(duration_minutes=DEFAULT_DURATION,
                          parent=None, **kwargs) -> CircularTimer:
    return CircularTimer(duration_minutes, parent, **kwargs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = create_circular_timer(
        30, None,
        bg_color_idle     = "#000000",
        bg_opacity_idle   = 0.3,
        bg_color_active   = "#313132",
        bg_opacity_active = 1.0,
        fg_color          = "#FFFFFF",
        stroke_width      = 8,
        text_scale        = 0.25,
        icon_scale        = 0.3,
        icon_idle         = "Icon_Timer.png",
        icon_active       = "Icon_Timer_Grey.png",
        icon_opacity_idle   = 0.5,
        icon_opacity_active = 1.0,
    )
    w.resize(150, 150)
    w.show()

    # demo: start after 2s, then pause at 6s, resume at 10s
    QTimer.singleShot(2000, w.start)
    QTimer.singleShot(6000, w.stop)
    QTimer.singleShot(10000, w.toggle)
    sys.exit(app.exec_())
