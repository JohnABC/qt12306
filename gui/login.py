#-*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from lib import train
from base import Base
from verify import Verify
from config import configGui, configCommon

class Login(Base):
	triggerWidgets = {}
	postWidgets = {}

	def __init__(self, parent = None):
		super(Login, self).__init__(parent)
		self.initDialog()
		self.bindSignalSlot()

	def initDialog(self):
		mainLayout = QGridLayout()
		linkBox = QHBoxLayout()
		
		maxDate = "/".join(map(str, configCommon.getMaximumDate()))

		self.triggerWidgets["username"] = self.postWidgets["username"] = QComboBox()
		self.triggerWidgets["username"].setEditable(True)
		self.triggerWidgets["password"] = self.postWidgets["password"] = QLineEdit()
		self.triggerWidgets["password"].setEchoMode(QLineEdit.Password);
		self.triggerWidgets["password"].setStyleSheet("lineedit-password-character: 42")
		self.triggerWidgets["submitButton"] = QPushButton(self.tr(u"登录"))
		self.triggerWidgets["message"] = QLabel(self.tr(u"今天可预定" + maxDate + u"的票"))

		linkBox.addWidget(self.getLinkLabel(u"忘记密码", configGui.forgetUrl))
		linkBox.addWidget(self.getLinkLabel(u"注册", configGui.registerUrl))

		mainLayout.addWidget(QLabel(self.tr(u"用户名:")), 0, 0)
		mainLayout.addWidget(self.triggerWidgets["username"], 0, 1)
		mainLayout.addWidget(QLabel(self.tr(u"密　码:")), 1, 0)
		mainLayout.addWidget(self.triggerWidgets["password"], 1, 1)
		mainLayout.addWidget(self.triggerWidgets["submitButton"], 2, 0, 1, 2)
		mainLayout.addLayout(linkBox, 3, 0, 1, 2, Qt.AlignHCenter)
		mainLayout.addWidget(self.triggerWidgets["message"], 4, 0, 1, 2, Qt.AlignHCenter)

		self.setLayout(mainLayout)

		self.setWindowTitle(u"12306登录")
		self.setWindowIcon(Base.getLogoIcon())
		self.setFixedSize(self.sizeHint())

	def bindSignalSlot(self):
		QObject.connect(self.triggerWidgets["submitButton"], SIGNAL("clicked()"), self.login)
		
	def updateMessage(self, text, color = ""):
		if color:
			text = '<font color="%s">%s</font>' % (color, text)
		self.triggerWidgets["message"].setText(self.tr(text))

	def login(self):
		username = self.postWidgets["username"].currentText()
		if username.isEmpty():
			QToolTip.showText(self.postWidgets["username"].mapToGlobal(QPoint(0, 0)), self.tr(u"请输入12306账号"))
			return

		password = self.postWidgets["password"].text()
		if password.isEmpty():
			QToolTip.showText(self.mapToGlobal(self.postWidgets["password"].pos()), self.tr(u"请输入12306密码"))
			return

		while True:
			vcode = self.getLoginVCode()
			if not vcode:
				break
				
			train12306 = train.getInstance()
			if (train12306.isVCodeRight(train12306.reqVCodeCheck("sjrand", vcode))):
				loginRes = train12306.reqLoginSuggest({					#可以获取和展示登录失败原因
					"loginUserDTO.user_name": str(username),
					"userDTO.password": str(password),
					"randCode": vcode,
					"randCode_validate": '',
				})
				
				if not train12306.isLoginSuccess(loginRes):
					self.updateMessage(train12306.getLoginFailedReason(loginRes), color = "red")
				else:
					self.updateMessage(u"登录成功", color = "green")
					
				break

	def getLoginVCode(self):
		codeDialog = Verify()
		if codeDialog.showImage("login", "sjrand"):
			return codeDialog.getPoints()
			
		return ""