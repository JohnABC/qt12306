#-*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from config import configGui

class Base(QWidget):
	def __init__(self, parent = None):
		super(Base, self).__init__(parent)
		self.setLogoIcon()

	@staticmethod
	def getLogoPixmap():
		return QPixmap(configGui.getImage("logo.ico"))

	@staticmethod
	def getLogoIcon():
		return QIcon(Base.getLogoPixmap())

	def setLogoIcon(self):
		self.setWindowIcon(Base.getLogoIcon())

	def getLinkLabel(self, label, link, style = "color:blue"):
		labelWidget = QLabel(self.tr('<a href="%s" style="%s">%s</a>' % (link, style, label)))
		labelWidget.setOpenExternalLinks(True)
		return labelWidget

	@staticmethod
	def question(text, button0 = u"确定", button1 = u"", button2 = u"", title = u"提示"):
		obj = QObject()

		box = QMessageBox()
		box.setWindowTitle(obj.tr(title))
		box.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowTitleHint)
		box.setIconPixmap(Base.getLogoPixmap())
		box.setText(obj.tr(text))

		buttons = []
		buttons.append(box.addButton(obj.tr(button0), QMessageBox.YesRole))
		if button1:
			buttons.append(box.addButton(obj.tr(button1), QMessageBox.NoRole))
		if button2:
			buttons.append(box.addButton(obj.tr(button2), QMessageBox.DestructiveRole))

		box.exec_()

		for index, button in enumerate(buttons):
			if button == box.clickedButton():
				return index
