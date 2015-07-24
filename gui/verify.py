#-*- coding: utf-8 -*-

import os
import sys
import time
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from config import configGui
from config import configCommon

class Verify(QDialog):
	imageLable = None
	refreshButton = None
	submitButton = None

	def __init__(self, parent = None):
		super(VerifyCodeDialog, self).__init__(parent)

		self.imageLabel = QLabel()
		self.imageLabel.setFixedSize(configGui.verifyCodeWidth, configGui.verifyCodeHeight)

		buttonBox = QDialogButtonBox()
		self.refreshButton = buttonBox.addButton(self.tr(u"刷新"), QDialogButtonBox.ResetRole)
		self.submitButton = buttonBox.addButton(self.tr(u"提交"), QDialogButtonBox.YesRole)

		vbox = QVBoxLayout()
		vbox.addWidget(self.imageLabel)
		vbox.addWidget(buttonBox)

		self.setLayout(vbox)

		self.setWindowTitle(self.tr(u"请点击对应图案"))
		self.setFixedSize(self.minimumSizeHint())

	def setImage(imageFileName):
		self.imageLabel.setPixmap(QPixmap(configCommon.getVCodeImageFile(imageFileName)))

