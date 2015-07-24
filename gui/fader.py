#-*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class Fader(QWidget):
	def __init__(self, parent = None):
		super(Fader, self).__init__(parent)

		self.resize(parent.size())
		self.setAttribute(Qt.WA_DeleteOnClose)

		self.startColor = parent.palette().window().color() if parent else Qt.white

		self.currentAlpha = 0
		self.timer = QTimer(self)
		self.connect(self.timer, SIGNAL("timeout"), self.update)

	def start(self, duration = 1000):
		self.duration = duration
		self.currentAlpha = 255
		self.timer.start(100)
		self.show()

	def paintEvent(self, event):
		semiTransparentColor = self.startColor
		semiTransparentColor.setAlpha(self.currentAlpha)
		painter = QPainter(self)
		painter.fillRect(self.rect(), semiTransparentColor)
		self.currentAlpha -= (255 * self.timer.interval() / self.duration)

		if self.currentAlpha <= 0:
			self.timer.stop()
			self.close()