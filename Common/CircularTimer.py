# circular_timer.py

import os
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore    import Qt, QTimer, QRectF, QSize
from PyQt5.QtGui     import QPainter, QPen, QColor, QFont, QPixmap
import sys

# defaults:
DEFAULT_DURATION            = 60.0
DEFAULT_BG_COLOR_IDLE       = "#FFFFFF"      # before start
DEFAULT_BG_OPACITY_IDLE     = 1.0             # 0.0–1.0 alpha
DEFAULT_BG_COLOR_ACTIVE     = "#313132"      # after start
DEFAULT_BG_OPACITY_ACTIVE   = 1.0             # 0.0–1.0 alpha
DEFAULT_FG_COLOR            = "#FFFFFF"
DEFAULT_STROKE_WIDTH        = 6
DEFAULT_TEXT_SCALE          = 0.15           # fraction of diameter
DEFAULT_TEXT_SIZE           = None           # if set, overrides text_scale
DEFAULT_ICON_SCALE          = 0.5            # fraction of inner circle diameter
DEFAULT_ICON_IDLE_FILENAME  = "Icon_Timer.png"
DEFAULT_ICON_ACTIVE_FILENAME= "Icon_Timer_Grey.png"

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
    ):
        super().__init__(parent)
        self.duration        = duration_minutes
        self.elapsed         = 0.0
        self.bg_color_idle   = QColor(bg_color_idle)
        self.bg_color_active = QColor(bg_color_active)

        # build idle‐RGBA
        self.bg_color_idle   = QColor(bg_color_idle)
        self.bg_color_idle.setAlphaF(bg_opacity_idle)

        # build active‐RGBA
        self.bg_color_active = QColor(bg_color_active)
        self.bg_color_active.setAlphaF(bg_opacity_active)
        
        self.fg_qcolor       = QColor(fg_color)
        self.stroke_width    = stroke_width
        self.text_scale      = text_scale
        self.text_size       = text_size
        self.icon_scale      = icon_scale
        self._show_text      = False

        # load both idle/active pixmaps
        base = os.path.join(os.path.dirname(__file__), "..", "Assets")
        self._pix_idle   = QPixmap(os.path.join(base, icon_idle))
        self._pix_active = QPixmap(os.path.join(base, icon_active))

        # label for icon
        self._icon_label = QLabel(self)
        self._icon_label.setAttribute(Qt.WA_TranslucentBackground)
        self._icon_label.setScaledContents(False)

        # ticking timer
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._on_tick)

        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

    def sizeHint(self):
        return QSize(100,100)

    def start(self):
        """Start from zero, show text & run."""
        self.elapsed    = 0.0
        self._show_text = True
        self._icon_label.hide()
        self._timer.start(1000)
        self.update()

    def stop(self):
        """Pause."""
        self._timer.stop()

    def toggle(self):
        """Pause if running, else resume (showing text)."""
        if self._timer.isActive():
            self.stop()
        else:
            self._show_text = True
            self._icon_label.hide()
            self._timer.start(1000)
        self.update()

    def reset(self):
        """Back to idle: stop, clear, show idle icon."""
        self._timer.stop()
        self.elapsed    = 0.0
        self._show_text = False
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
        # choose pixmap: idle if never started, paused shows active icon
        if   not self._show_text:
            pix = self._pix_idle
        elif not self._timer.isActive():
            pix = self._pix_active
        else:
            # running → no icon
            self._icon_label.hide()
            return

        size   = min(self.width(), self.height())
        margin = size*0.1 + self.stroke_width/2
        inner  = size - 2*margin
        isz    = int(inner * self.icon_scale)
        if not pix.isNull() and isz>0:
            scaled = pix.scaled(isz,isz, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            w,h    = scaled.width(), scaled.height()
            x = (self.width()-w)//2
            y = (self.height()-h)//2
            self._icon_label.setPixmap(scaled)
            self._icon_label.setGeometry(x,y,w,h)
            self._icon_label.show()

    def paintEvent(self, ev):
        size   = min(self.width(), self.height())
        margin = size*0.1
        rect   = QRectF(margin, margin, size-2*margin, size-2*margin)

        # keep icon in sync
        if not self._show_text or not self._timer.isActive():
            self._position_icon()

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # pick BG color depending on idle vs active
        bg = self.bg_color_active if self._show_text else self.bg_color_idle
        p.setPen(QPen(bg, self.stroke_width))
        p.drawEllipse(rect)

        # progress arc
        p.setPen(QPen(self.fg_qcolor, self.stroke_width, cap=Qt.RoundCap))
        pct = min(self.elapsed/self.duration, 1.0)
        span = int(-pct*360*16)
        p.drawArc(rect, -90*16, span)

        # draw minutes once started
        if self._show_text:
            mins   = int(self.elapsed)
            text   = f"{mins:01d} min"
            if self.text_size is not None:
                pt = self.text_size
            else:
                pt = max(1, int(size*self.text_scale))
            f = QFont()
            f.setBold(True)
            f.setPointSize(pt)
            p.setFont(f)
            p.setPen(self.fg_qcolor)
            p.drawText(rect, Qt.AlignCenter, text)


def create_circular_timer(duration_minutes=DEFAULT_DURATION,
                          parent=None, **kwargs)->CircularTimer:
    return CircularTimer(duration_minutes, parent, **kwargs)


if __name__=="__main__":
    app = QApplication(sys.argv)
    w = create_circular_timer(
        30, None,
        bg_color_idle="#EEEEEE",
        bg_color_active="#313132",
        fg_color="#FFFFFF",
        stroke_width=10,
        text_scale=0.25,
        icon_scale=0.3,
        icon_idle="Icon_Timer.png",
        icon_active="Icon_Timer_Grey.png",
    )
    w.resize(150,150)
    w.show()
    # idle icon first, then start
    QTimer.singleShot(2000, w.start)
    sys.exit(app.exec_())
