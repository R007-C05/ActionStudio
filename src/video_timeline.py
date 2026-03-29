# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6.QtWidgets import QWidget
from ui_video_timeline import Ui_VideoTimeline

class VideoTimeline(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_VideoTimeline()
        self.ui.setupUi(self)
