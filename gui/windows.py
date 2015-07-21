#-*- coding: utf-8 -*-

import sys
import time
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from config import configGui
from config import configCommon

QTextCodec.setCodecForTr(QTextCodec.codecForName(configGui.charset))

class BaseWidget(QWidget):
	def __init__(self, parent = None):
		super(BaseWidget, self).__init__(parent)

	def getLogoPixmap(self):
		return QPixmap(configGui.logoIconImage)

	def getLogoIcon(self):
		return QIcon(self.getLogoPixmap())

	@staticmethod
	def getCursorPos():
		return QCursor.pos()

	def question(self, text, button0 = u"确定", button1 = u"", button2 = u"", title = u"提示"):
		box = QMessageBox()
		box.setWindowTitle(self.tr(title))
		box.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowTitleHint)
		box.setIconPixmap(self.getLogoPixmap())
		box.setText(self.tr(text))

		buttons = []
		buttons.append(box.addButton(self.tr(button0), QMessageBox.YesRole))
		if button1:
			buttons.append(box.addButton(self.tr(button1), QMessageBox.NoRole))
		if button2:
			buttons.append(box.addButton(self.tr(button2), QMessageBox.DestructiveRole))

		box.exec_()

		for index, button in enumerate(buttons):
			if button == box.clickedButton():
				return index

class MainWindow(BaseWidget):
	conditionWidgets = {}
	triggerWidgets = {}

	def __init__(self, parent = None):
		super(MainWindow, self).__init__(parent)
		self.initBase()

	def initBase(self):
		self.setWindowTitle(configGui.windowTitle)
		self.setWindowIcon(self.getLogoIcon())
		self.resize(configGui.mainWindowWidth, configGui.mainWindowHeight)

		self.setWindowFlags(Qt.WindowMinimizeButtonHint)
		self.setFixedSize(self.width(), self.height())

		mainLayout = QVBoxLayout(self)
		mainLayout.addLayout(self.getSearchLayout())
		mainLayout.addLayout(self.getTrainDataLayout())
		mainLayout.addStretch()

	def getSearchLayout(self):
		searchBox = QHBoxLayout()

		conditionBox = QVBoxLayout()
		
		stationConditionBox = QHBoxLayout()
		trainTypeConditionBox = QHBoxLayout()
		seatTypeConditionBox = QHBoxLayout()

		self.conditionWidgets["startStation"] = self.triggerWidgets["startStation"] = QComboBox()
		self.conditionWidgets["endStation"] = self.triggerWidgets["endStation"] = QComboBox()
		self.conditionWidgets["startStation"].setEditable(True)
		self.conditionWidgets["endStation"].setEditable(True)

		self.triggerWidgets["turnStations"] = QPushButton(self.tr(u"<->"))

		self.conditionWidgets["startDate"] = self.triggerWidgets["startDate"] = self.getStartDateWidget()

		stationConditionBox.addWidget(QLabel(self.tr(u"出发")))
		stationConditionBox.addWidget(self.triggerWidgets["startStation"])
		stationConditionBox.addWidget(self.triggerWidgets["turnStations"])
		stationConditionBox.addWidget(QLabel(self.tr(u"目的")))
		stationConditionBox.addWidget(self.triggerWidgets["endStation"])
		stationConditionBox.addWidget(QLabel(self.tr(u"日期")))
		stationConditionBox.addWidget(self.triggerWidgets["startDate"])
		stationConditionBox.addStretch()

		self.conditionWidgets["trainTypes"] = self.triggerWidgets["trainTypes"] = {}
		self.triggerWidgets["trainTypeAll"] = QCheckBox(self.tr(u"全部"))
		trainTypeConditionBox.addWidget(QLabel(self.tr(u"车型")))
		trainTypeConditionBox.addWidget(self.triggerWidgets["trainTypeAll"])
		for trainType in configCommon.trainTypes:
			cb = QCheckBox(self.tr(trainType["des"]))
			cb.trainFirstChar = trainType["code"]

			self.conditionWidgets["trainTypes"][trainType["code"]] = self.triggerWidgets["trainTypes"][trainType["code"]] = cb
			trainTypeConditionBox.addWidget(self.triggerWidgets["trainTypes"][trainType["code"]])
		trainTypeConditionBox.addStretch()

		self.conditionWidgets["seatTypes"] = self.triggerWidgets["seatTypes"] = {}
		self.triggerWidgets["seatTypeAll"] = QCheckBox(self.tr(u"全部"))
		seatTypeConditionBox.addWidget(QLabel(self.tr(u"席别")))
		seatTypeConditionBox.addWidget(self.triggerWidgets["seatTypeAll"])
		for seatType in configCommon.seatTypes:
			if (seatType["des"]):
				cb = QCheckBox(self.tr(seatType["des"]))
				cb.seatCode = seatType["code"]
				cb.seatNum = seatType["num"]

				self.conditionWidgets["seatTypes"][seatType["code"]] = self.triggerWidgets["seatTypes"][seatType["code"]] = cb
				seatTypeConditionBox.addWidget(self.triggerWidgets["seatTypes"][seatType["code"]])
		seatTypeConditionBox.addStretch()

		conditionBox.addLayout(stationConditionBox)
		conditionBox.addLayout(trainTypeConditionBox)
		conditionBox.addLayout(seatTypeConditionBox)

		self.triggerWidgets["searchButton"] = QPushButton(self.tr(u"点击查询"))

		searchBox.addLayout(conditionBox)
		searchBox.addWidget(self.triggerWidgets["searchButton"], 1)

		return searchBox

	def getStartDateWidget(self):
		minDate = configCommon.getMinimumDate()
		maxDate = configCommon.getMaximumDate()

		startDateWidget = QDateTimeEdit()
		startDateWidget.setDateTime(QDateTime.currentDateTime())
		startDateWidget.setDisplayFormat("yyyy-mm-dd")
		startDateWidget.setCalendarPopup(True)
		startDateWidget.setDateRange(QDate(*minDate), QDate(*maxDate))

		return startDateWidget

	def getTrainDataLayout(self):
		trainDataLayout = QVBoxLayout()
		labelNames = [u"车次", u"出发地", u"目的地", u"历时", u"商务座", u"特等座", u"一等座", u"高等软座", u"软卧", u"硬卧", u"软座", u"硬座", u"无座", u"操作"]
		
		self.triggerWidgets["trainData"] = trainDataWidget = QTableWidget()
		trainDataWidget.setFixedHeight(configCommon.trainDataTableHeight)
		trainDataWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
		trainDataWidget.horizontalHeader().setStretchLastSection(True)
		trainDataWidget.setColumnCount(len(labelNames))

		headerLabels = QStringList()
		for labelName in labelNames:
			headerLabels.append(labelName)

		trainDataWidget.setHorizontalHeaderLabels(headerLabels)

		trainDataLayout.addWidget(trainDataWidget)

		return trainDataLayout

	def setTrainData(self, trainData):
		for i in range(self.triggerWidgets["trainData"].rowCount()):
			triggerWidgets["trainData"].removeRow(i)

		for train in trainData:
			pass

	def closeEvent(self, event):
		event.accept() if self.question(u"是否确定要退出？", button1 = u"取消") == 0 else event.ignore()