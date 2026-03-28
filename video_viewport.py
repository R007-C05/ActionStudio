# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QOpenGLWidget
from PySide6.QtGui import QPainter, QColor

class VideoViewport(QOpenGLWidget):
    def paintGL(self):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("black"))
        painter.end()