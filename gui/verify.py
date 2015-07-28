#-*- coding: utf-8 -*-

import os
import sys
import time
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from gui import Base
from lib import train
from config import configGui, configCommon

class Verify(QDialog, Base):
	codeModule = ""
	codeRand = ""

	triggerWidgets = {}
	pointWidgets = []

	def __init__(self, parent = None):
		super(Verify, self).__init__(parent)

		self.triggerWidgets["imageLabel"] = QLabel()
		self.triggerWidgets["imageLabel"].setFixedSize(configGui.verifyCodeWidth, configGui.verifyCodeHeight)

		buttonBox = QDialogButtonBox()
		self.triggerWidgets["refreshButton"] = buttonBox.addButton(self.tr(u"刷新"), QDialogButtonBox.ResetRole)
		self.triggerWidgets["submitButton"] = buttonBox.addButton(self.tr(u"提交"), QDialogButtonBox.YesRole)

		vbox = QVBoxLayout()
		vbox.addWidget(self.triggerWidgets["imageLabel"])
		vbox.addWidget(buttonBox)

		self.setLayout(vbox)

		self.setWindowTitle(self.tr(u"请点击对应图案"))
		self.setFixedSize(self.minimumSizeHint())

		self.bindSignalSlot()
		
	def initPointWidgets(self):
		for pLabel in self.pointWidgets:
			pLabel.close()
		self.pointWidgets = []

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			cursorPos = QCursor.pos()
			labelSize = self.triggerWidgets["imageLabel"].size()
			labelPos = self.mapToGlobal(self.triggerWidgets["imageLabel"].pos())
			labelMinPos = labelPos + QPoint(0,configGui.vcodeImageTipHeight)
			labelMaxPos = labelPos + QPoint(labelSize.width(), labelSize.height())

			
			pixmap = QPixmap(configGui.getImage("logo.ico"))
			pixmapSize = pixmap.size()
			
			#需要在图片显示范围内
			if labelMinPos.x() <= cursorPos.x() <= labelMaxPos.x() and labelMinPos.y() <= cursorPos.y() <= labelMaxPos.y():
				delIndex = -1
				for index, p in enumerate(self.pointWidgets):
					pPoint = labelPos + p.pos()
					if 0 <= cursorPos.x() - pPoint.x() <= pixmapSize.width() and 0 <= cursorPos.y() - pPoint.y() <= pixmapSize.height():
						p.close()
						delIndex = index
						break
				
				if delIndex >= 0:
					del self.pointWidgets[delIndex]
				else:
					newLabel = QLabel(self.triggerWidgets["imageLabel"])
					newLabel.setPixmap(pixmap)
					newLabel.resize(pixmapSize)
					newLabel.move(cursorPos.x() - labelPos.x() - pixmapSize.width() / 2, cursorPos.y() - labelPos.y() - pixmapSize.height() / 2)
					newLabel.show()
					self.pointWidgets.append(newLabel)
					
	def bindSignalSlot(self):
		QObject.connect(self.triggerWidgets["refreshButton"], SIGNAL("clicked()"), self.showImage)
		QObject.connect(self.triggerWidgets["submitButton"], SIGNAL("clicked()"), self.submit)

	def toggleSelected(self):
		pixmap = QPixmap(configGui.getImage("logo.ico"))
		cursorPos = QCursor.pos()
		print cursorPos

	def showImage(self, codeModule = "", codeRand = ""):
		if codeModule and codeRand:
			self.codeModule = codeModule
			self.codeRand = codeRand
		
		self.initPointWidgets()
		
		train12306 = train.getInstance()
		imageRes = train12306.reqVCodeImage(self.codeModule, self.codeRand)
		pixmap = QPixmap()
		pixmap.loadFromData(imageRes)
		self.triggerWidgets["imageLabel"].setPixmap(pixmap)
		if self.isHidden():
			return self.exec_()
				
		return 0

	def submit(self):
		if len(self.pointWidgets) < 1:
			return
			
		self.done(1)
				
	def getPoints(self):
		return ",".join([str(label.pos().x() + int(label.size().width() / 2)) + "," + str(label.pos().y() + int(label.size().height() / 2) - configGui.vcodeImageTipHeight) for label in self.pointWidgets])
