#-*- coding: utf-8 -*-

import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from base import Base
from config import configGui
from config import configCommon

class Main(Base):
	data = {}
	conditionWidgets = {}
	triggerWidgets = {}
	postWidgets = {}
	rushWidgets = {}
	printerWidgets = {}

	def __init__(self, parent = None):
		super(Main, self).__init__(parent)
		self.initBase()
		QThread.sleep(10)

	def closeEvent(self, event):
		event.accept() if self.question(u"是否确定要退出？", button1 = u"取消") == 0 else event.ignore()


	def initBase(self):
		self.setWindowTitle(configGui.windowTitle)
		self.setWindowIcon(Base.getLogoIcon())
		self.resize(configGui.mainWindowWidth, configGui.mainWindowHeight)

		self.setWindowFlags(Qt.WindowMinimizeButtonHint)
		self.setFixedSize(self.width(), self.height())

		mainLayout = QVBoxLayout(self)
		mainLayout.addLayout(self.getSearchLayout())
		mainLayout.addLayout(self.getTrainDataLayout())
		mainLayout.addLayout(self.getBottomLayout())
		mainLayout.addStretch()

	def getSearchLayout(self):
		searchBox = QHBoxLayout()

		conditionBox = QVBoxLayout()
		
		stationConditionBox = QHBoxLayout()
		trainTypeConditionBox = QHBoxLayout()
		seatTypeConditionBox = QHBoxLayout()

		searchButtonBox = QHBoxLayout()

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
		searchButtonBox.addWidget(self.triggerWidgets["searchButton"])
		self.triggerWidgets["searchButton"].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		searchBox.addLayout(conditionBox)
		searchBox.addLayout(searchButtonBox)

		return searchBox

	def getStartDateWidget(self):
		minDate = configCommon.getMinimumDate()
		maxDate = configCommon.getMaximumDate()

		startDateWidget = QDateTimeEdit()
		startDateWidget.setDateTime(QDateTime.currentDateTime())
		startDateWidget.setDisplayFormat("yyyy-MM-dd")
		startDateWidget.setCalendarPopup(True)
		startDateWidget.setDateRange(QDate(*minDate), QDate(*maxDate))

		return startDateWidget

	def getTrainDataLayout(self):
		trainDataLayout = QVBoxLayout()
		labelNames = [u"车次", u"出发地" + os.linesep + u"目的地", u"出发时间" + os.linesep + u"到达时间", u"历时", u"商务座", u"特等座", u"一等座", u"高等软座", u"软卧", u"硬卧", u"软座", u"硬座", u"无座", u"操作"]
		
		self.triggerWidgets["trainData"] = trainDataWidget = QTableWidget()
		trainDataWidget.setFixedHeight(configGui.trainTableHeight)
		trainDataWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
		trainDataWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
		trainDataWidget.horizontalHeader().setStretchLastSection(True)
		trainDataWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)
		trainDataWidget.setColumnCount(len(labelNames))

		headerLabels = QStringList()
		for labelName in labelNames:
			headerLabels.append(labelName)

		trainDataWidget.setHorizontalHeaderLabels(headerLabels)

		trainDataLayout.addWidget(trainDataWidget)

		return trainDataLayout

	def getBottomLayout(self):
		hbox = QHBoxLayout()
		hbox.addLayout(self.getSelectionLayout())
		hbox.addLayout(self.getRushLayout())
		hbox.addLayout(self.getPrinterLayout())
		return hbox

	def getSelectionLayout(self):
		hbox = QHBoxLayout()
		hbox.addLayout(self.getSelectionPassengerLayout())
		hbox.addLayout(self.getSelectionSeatLayout())
		hbox.addLayout(self.getSelectionTrainLayout())

		return hbox

	def getSelectionPassengerLayout(self):
		vbox = QVBoxLayout()

		self.postWidgets["passengerList"] = self.triggerWidgets["passengerList"] = QListWidget()
		self.postWidgets["passengerList"].setFixedWidth(configGui.postListWidth)

		vbox.addWidget(QLabel(self.tr(u"*选择乘客")))
		vbox.addWidget(self.postWidgets["passengerList"])

		return vbox

	def getSelectionSeatLayout(self):
		vbox = QVBoxLayout()
		
		self.postWidgets["seatList"] = self.triggerWidgets["seatList"] = listWidget = QListWidget()
		self.postWidgets["seatList"].setFixedWidth(configGui.postListWidth)
		for seatType in configCommon.seatTypes:
			if seatType["des"]:
				item = QListWidgetItem()
				checkbox = QCheckBox(seatType["des"])
				checkbox.seatCode = seatType["code"]
				checkbox.seatNum = seatType["num"]
				listWidget.addItem(item)
				listWidget.setItemWidget(item, checkbox)

		vbox.addWidget(QLabel(self.tr(u"*选择席别")))
		vbox.addWidget(listWidget)
		
		return vbox

	def getSelectionTrainLayout(self):
		vbox = QVBoxLayout()

		self.postWidgets["trainList"] = self.triggerWidgets["trainList"] = QListWidget()
		self.postWidgets["trainList"].setFixedWidth(configGui.postListWidth)

		vbox.addWidget(QLabel(self.tr(u"*选择车次")))
		vbox.addWidget(self.postWidgets["trainList"])
		
		return vbox

	def getRushLayout(self):
		vbox = QVBoxLayout()
		timeOnBox = QHBoxLayout()
		timeIntervalBox = QHBoxLayout()
		advanceRadioBox = QHBoxLayout()

		self.rushWidgets["isTimeOn"] = QCheckBox(self.tr(u"定时启动"))
		self.rushWidgets["timeOnValue"] = self.getTimeOnWidget()
		self.rushWidgets["isTimeOn"].setFixedWidth(configGui.rushTextWidth)
		self.rushWidgets["timeOnValue"].setFixedWidth(configGui.rushWidgetWidth)

		self.rushWidgets["isTimeInterval"] = QCheckBox(self.tr(u"查询间隔"))
		self.rushWidgets["timeIntvalValue"] = self.getTimeIntervalWidget()
		self.rushWidgets["isTimeInterval"].setFixedWidth(configGui.rushTextWidth)
		self.rushWidgets["timeIntvalValue"].setFixedWidth(configGui.rushWidgetWidth)

		self.rushWidgets["isSeatAdvance"] = QRadioButton(self.tr(u"坐席优先"))
		self.rushWidgets["isTrainAdvance"] = QRadioButton(self.tr(u"车次优先"))
		self.rushWidgets["isSeatAdvance"].setChecked(True)

		timeOnBox.addWidget(self.rushWidgets["isTimeOn"])
		timeOnBox.addWidget(self.rushWidgets["timeOnValue"])

		timeIntervalBox.addWidget(self.rushWidgets["isTimeInterval"])
		timeIntervalBox.addWidget(self.rushWidgets["timeIntvalValue"])

		advanceRadioBox.addWidget(self.rushWidgets["isSeatAdvance"])
		advanceRadioBox.addWidget(self.rushWidgets["isTrainAdvance"])

		self.triggerWidgets["rushButton"] = QPushButton(self.tr(u"开始抢票"))
		self.triggerWidgets["rushButton"].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

		vbox.addWidget(QLabel(self.tr(u"抢票设置")))
		vbox.addLayout(timeOnBox)
		vbox.addLayout(timeIntervalBox)
		vbox.addLayout(advanceRadioBox)
		vbox.addWidget(self.triggerWidgets["rushButton"])

		return vbox

	def getTimeOnWidget(self):
		minTime = configCommon.getMinimumTime()
		maxTime = configCommon.getMaximumTime()

		timeOnWidget = QTimeEdit()
		timeOnWidget.setTime(QTime.fromString(configCommon.saleStartTime, "hh:mm:ss"))
		timeOnWidget.setDisplayFormat("hh:mm:ss")
		timeOnWidget.setTimeRange(QTime(*minTime), QTime(*maxTime))
		timeOnWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

		return timeOnWidget

	def getTimeIntervalWidget(self):
		timeIntervalWidget = QSpinBox()
		timeIntervalWidget.setRange(configCommon.rushRefreshMinTimeIntval, configCommon.rushRefreshMaxTimeIntval)
		timeIntervalWidget.setSingleStep(configCommon.rushRefreshTimeIntval)
		timeIntervalWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

		return timeIntervalWidget

	def getPrinterLayout(self):
		vbox = QVBoxLayout()
		
		self.triggerWidgets["printer"] = QTextEdit()
		self.triggerWidgets["printer"].setReadOnly(True)

		vbox.addWidget(QLabel(self.tr(u"输出日志")))
		vbox.addWidget(self.triggerWidgets["printer"])

		return vbox

	def setStationData(self, stationData):
		pass

	def setTrainData(self, trainData):
		#需要获取 车型/席别 筛选
		#根据数组长度设置表格行数
		trainDataWidget = self.triggerWidgets["trainData"]
		for i in range(trainDataWidget.rowCount()):
			trainDataWidget.removeRow(i)

		trainDataWidget.setRowCount(len)
		for train in trainData:
			pass

	def setPassengerData(self, passengerData):
		for passenger in passengerData:
			pass
			"""
			item = QListWidgetItem()
			checkbox = QCheckBox(self.tr(u"随永杰"))

			self.postWidgets["passengerList"].addItem(item)
			self.postWidgets["passengerList"].setItemWidget(item, checkbox)
			"""