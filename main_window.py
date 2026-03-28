# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QMainWindow
from ui_main_window import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Action Studio")