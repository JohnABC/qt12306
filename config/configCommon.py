#-*- coding: utf-8 -*-

import os
import time

saleMinDelayDay = 0
saleMaxDelayDay = 59
saleStartTime = "07:00:00"
saleStopTime = "23:00:00"
rushRefreshMinTimeIntval = 2000
rushRefreshMaxTimeIntval = 3600000
rushRefreshTimeIntval = 100

RS_SUC = 0
RS_TIMEOUT = 1
RS_JSON_ERROR = 2
RS_OTHER_ERROR = 3

trainTypes = [
	{"des": u"G/C-高铁/城际", "code": "G|C"},
	{"des": u"D-动车", "code": "D"},
	{"des": u"Z-直达", "code": "Z"},
	{"des": u"T-特快", "code": "T"},
	{"des": u"K-快速", "code": "K"},
	{"des": u"L-临客", "code": "L"},
	{"des": u"普快", "code": ""}
]

seatTypes = [
	{"des": u"商务座", "code": "swz", "num": ("A9", "9")},
	{"des": u"特等座", "code": "tz", "num": ("P", "P")},
	{"des": u"一等座", "code": "zy", "num": ("M", "M")},
	{"des": u"二等座", "code": "ze", "num": ("O", "O")},
	{"des": u"高级软卧", "code": "gr", "num": ("A6", "6")},
	{"des": u"软卧", "code": "rw", "num": ("A4", "4")},
	{"des": u"硬卧", "code": "yw", "num": ("A3", "3")},
	{"des": u"软座", "code": "rz", "num": ("A2", "2")},
	{"des": u"硬座", "code": "yz", "num": ("A1", "1")},
	{"des": u"无座", "code": "yz", "num": ("A1", "1")},
	{"des": u"", "code": "wz", "num": ("WZ", "WZ")},
	{"des": u"", "code": "wz", "num": ("A9", "9")}
]

def getNowTimestamp():
	return time.time()

def getMinimumDate():
	return time.localtime(getNowTimestamp() + saleMinDelayDay * 24 * 3600)[:3]

def getMaximumDate():
	return time.localtime(getNowTimestamp() + saleMaxDelayDay * 24 * 3600)[:3]

def getMinimumTime():
	return [int(x) for x in saleStartTime.split(":")]

def getMaximumTime():
	return [int(x) for x in saleStopTime.split(":")]

def decMakeDir(func):
	def handleFunc(*args, **kwargs):
		dirname = func(*args, **kwargs)
		if not os.path.exists(dirname):
			os.makedirs(dirname)
		elif not os.path.isdir(dirname):
			pass

		return dirname
	return func

def getWorkDir():
	return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@decMakeDir
def getTmpDir():
	return os.path.join(getWorkDir(), "tmp")

@decMakeDir
def getLogDir():
	return os.path.join(getTmpDir(), "log")

@decMakeDir
def getDataDir():
	return os.path.join(getTmpDir(), "data")

@decMakeDir
def getVCodeDir():
	return os.path.join(getTmpDir(), "vcode")

def getVCodeImageFile(imageName):
	return os.path.join(getVCodeDir(), imageName + ".jpg")