#-*- coding: utf-8 -*-
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from gui import windows

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = windows.MainWindow()
	window.show()
	sys.exit(app.exec_())	