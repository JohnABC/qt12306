#-*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from base import Base
from config import configGui

class Login(QDialog, Base):
	triggerWidgets = {}
	postWidgets = {}

	def __init__(self, parent = None):
		super(Login, self).__init__(parent)
		self.initDialog()
		self.bindSignalSlot()

	def initDialog(self):
		mainLayout = QGridLayout()
		linkBox = QHBoxLayout()

		self.triggerWidgets["username"] = self.postWidgets["username"] = QComboBox()
		self.triggerWidgets["username"].setEditable(True)
		self.triggerWidgets["password"] = self.postWidgets["password"] = QLineEdit()
		self.triggerWidgets["password"].setEchoMode(QLineEdit.Password);
		self.triggerWidgets["submitButton"] = QPushButton(self.tr(u"登录"))

		linkBox.addWidget(self.getLinkLabel(u"忘记密码", configGui.forgetUrl))
		linkBox.addWidget(self.getLinkLabel(u"注册", configGui.registerUrl))

		mainLayout.addWidget(QLabel(self.tr(u"用户名:")), 0, 0)
		mainLayout.addWidget(self.triggerWidgets["username"], 0, 1)
		mainLayout.addWidget(QLabel(self.tr(u"密　码:")), 1, 0)
		mainLayout.addWidget(self.triggerWidgets["password"], 1, 1)
		mainLayout.addWidget(self.triggerWidgets["submitButton"], 2, 0, 1, 2)
		mainLayout.addLayout(linkBox, 3, 0, 1, 2, Qt.AlignHCenter)

		self.setLayout(mainLayout)

		self.setWindowTitle(u"12306登录")
		self.setWindowIcon(Base.getLogoIcon())
		self.setFixedSize(self.sizeHint())

	def bindSignalSlot(self):
		QObject.connect(self.triggerWidgets["submitButton"], SIGNAL("clicked()"), self.checkAndShowVerify)

	def checkAndShowVerify(self):
		username = self.postWidgets["username"].currentText()
		if username.isEmpty():
			QToolTip.showText(self.postWidgets["username"].mapToGlobal(QPoint(0, 0)), self.tr(u"请输入12306账号"))
			return

		password = self.postWidgets["password"].text()
		if password.isEmpty():
			QToolTip.showText(self.mapToGlobal(self.postWidgets["password"].pos()), self.tr(u"请输入12306账号"))
			return

		