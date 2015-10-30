#coding:utf-8

from lifePy.Bord import MainWindow
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
main = MainWindow()
sys.exit(app.exec_())
