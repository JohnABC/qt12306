#-*- coding: utf-8 -*-
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from gui import windows
from lib import logger

app = QApplication(sys.argv)
loginDialog = windows.LoginDialog()
loginDialog.show()
"""
app.processEvents()
splash = QSplashScreen(QPixmap("gui/images/splash.png"))
splash.show()
window = windows.MainWindow()
window.show()
splash.finish(window)
"""
sys.exit(app.exec_())