# This Python file uses the following encoding: utf-8
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QWidget, QStackedWidget
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import Qt


class VideoViewport(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Page 0: plain black widget shown when idle (no native subsurface)
        self._black = QWidget(self)
        self._black.setAutoFillBackground(True)
        pal = self._black.palette()
        pal.setColor(QPalette.ColorRole.Window, QColor(Qt.GlobalColor.black))
        self._black.setPalette(pal)

        # Page 1: actual video widget (native subsurface only created here)
        self._video = QVideoWidget(self)

        self.addWidget(self._black)
        self.addWidget(self._video)
        self.setCurrentWidget(self._black)

    def videoWidget(self) -> QVideoWidget:
        return self._video

    def show_black_screen(self, visible: bool):
        self.setCurrentWidget(self._black if visible else self._video)