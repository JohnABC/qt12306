#-*- coding: utf-8 -*-

import time
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from config import configGui

class Splash(QSplashScreen):
	def __init__(self, splashImage):
		super(Splash, self).__init__(splashImage)
		self.setWindowModality(Qt.ApplicationModal)
		self.resize(splashImage.size())

	def fadeInTicker(self):
		self.setWindowOpacity(0)
		self.show()

		while True:
			newOpacity = self.windowOpacity() + configGui.splashOpacityChangeNum
			if newOpacity > 1:
				break

			self.setWindowOpacity(newOpacity)
			self.show()

			time.sleep(configGui.splashOpacityChangeTime)

	def fadeOutTicker(self):
		while True:
			newOpacity = self.windowOpacity() - configGui.splashOpacityChangeNum
			if newOpacity < 0:
				self.close()
				break

			self.setWindowOpacity(newOpacity)
			self.show()

			time.sleep(configGui.splashOpacityChangeTime)