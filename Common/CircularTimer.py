# circular_timer.py

import os
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGraphicsOpacityEffect
from PyQt5.QtCore    import Qt, QTimer, QRectF, QSize, QPointF
from PyQt5.QtGui     import QPainter, QPen, QColor, QFont, QPixmap

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
        self._state = "idle"    # possible values: "idle", "running", "paused"

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

    def stop(self):
        """Pause: hide text, show triangle (but don’t redraw arc)."""
        self._state = "paused"
        self._timer.stop()
        self._show_text     = False
        self._show_triangle = True
        self._icon_label.hide()
        # no self.update() here — arc stays exactly as it was

    def toggle(self):
        """
        Toggle between paused and running without resetting:
         - if running, pause (show triangle),
         - if paused, resume (show text and arc stays at current elapsed).
        """
        if self._timer.isActive():
            # running → pause
            self.stop()
        else:
            # paused or idle → resume
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
        self.update()

    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        self._position_icon()

    def _position_icon(self):
        # only show icon in true idle (no text, no triangle)
        if self._show_text or self._show_triangle:
            self._icon_label.hide()
            return

        pix     = self._pix_idle
        opacity = self.icon_opacity_idle

        size   = min(self.width(), self.height())
        margin = size*0.1 + self.stroke_width/2
        inner  = size - 2*margin
        isz    = int(inner * self.icon_scale)
        if not pix.isNull() and isz>0:
            scaled = pix.scaled(isz, isz, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            w, h   = scaled.width(), scaled.height()
            x = (self.width()-w)//2
            y = (self.height()-h)//2

            self._icon_label.setPixmap(scaled)
            self._icon_label.setGeometry(x, y, w, h)

            eff = QGraphicsOpacityEffect(self._icon_label)
            eff.setOpacity(opacity)
            self._icon_label.setGraphicsEffect(eff)
            self._icon_label.show()

    def paintEvent(self, ev):
        size   = min(self.width(), self.height())
        margin = size * 0.1
        rect   = QRectF(margin, margin, size - 2*margin, size - 2*margin)

        # in true‐idle (never started), show the icon; otherwise hide it
        if not self._show_text and not self._show_triangle:
            self._position_icon()

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # ─── draw background circle ───────────────────────────────────────────────
        # idle state (never started) uses idle color; paused or running use active
        bg = self.bg_color_idle if (not self._show_text and not self._show_triangle) else self.bg_color_active
        p.setPen(QPen(bg, self.stroke_width))
        p.drawEllipse(rect)

        # ─── draw progress arc ────────────────────────────────────────────────────
        p.setPen(QPen(self.fg_qcolor, self.stroke_width, cap=Qt.RoundCap))
        pct  = min(self.elapsed / self.duration, 1.0)
        span = int(-pct * 360 * 16)
        p.drawArc(rect, -90 * 16, span)

        # ─── if running, draw minutes text ────────────────────────────────────────
        if self._show_text:
            mins = int(self.elapsed)
            text = f"{mins:01d} min"
            pt   = self.text_size if self.text_size else max(1, int(size * self.text_scale))
            font = QFont()
            font.setBold(True)
            font.setPointSize(pt)
            p.setFont(font)
            p.setPen(self.fg_qcolor)
            p.drawText(rect, Qt.AlignCenter, text)

        # ─── if paused, draw right‐pointing triangle ──────────────────────────────
        elif self._show_triangle:
            inner = size - 2*margin
            s     = inner * 0.4
            cx, cy = rect.center().x(), rect.center().y()
            dx = inner * 0.05
            p.setPen(Qt.NoPen)
            p.setBrush(self.fg_qcolor)
            pts = [
                QPointF(cx - s/2 + dx, cy - s/2),
                QPointF(cx - s/2 + dx, cy + s/2),
                QPointF(cx + s/2 + dx, cy)
            ]
            p.drawPolygon(*pts)



def create_circular_timer(duration_minutes=DEFAULT_DURATION,
                          parent=None, **kwargs) -> CircularTimer:
    return CircularTimer(duration_minutes, parent, **kwargs)


if __name__=="__main__":
    app = QApplication(sys.argv)
    w = create_circular_timer(
        30, None,
        bg_color_idle    = "#000000",
        bg_opacity_idle  = 0.3,
        bg_color_active  = "#313132",
        bg_opacity_active= 1.0,
        fg_color         = "#FFFFFF",
        stroke_width     = 8,
        text_scale       = 0.25,
        icon_scale       = 0.3,
        icon_idle        = "Icon_Timer.png",
        icon_active      = "Icon_Timer_Grey.png",
        icon_opacity_idle  = 0.5,
        icon_opacity_active= 1.0,
    )
    w.resize(150, 150)
    w.show()

    # demo: start after 2s, then pause at 6s, resume at 10s
    QTimer.singleShot(2000, w.start)
    QTimer.singleShot(6000, w.stop)
    QTimer.singleShot(10000, w.toggle)
    sys.exit(app.exec_())
