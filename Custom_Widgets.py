import sys
from PyQt5.QtWidgets import (QApplication, QWidget,
    QPushButton,QLabel,QMainWindow,QHBoxLayout,QVBoxLayout,
    QLineEdit)
from PyQt5.QtCore import pyqtSignal


class ClickLineEdit(QLineEdit):
    clicked = pyqtSignal()
    def mousePressEvent(self,event):
        self.clicked.emit()
        QLineEdit.mousePressEvent(self,event)
