#-*- coding: utf-8 -*-

import time

saleMinDelayDay = 0
saleMaxDelayDay = 59
saleStartTime = "07:00:00"
saleStopTime = "23:00:00"
rushRefreshMinTimeIntval = 2000
rushRefreshMaxTimeIntval = 3600000
rushRefreshTimeIntval = 100

trainTypes = [
	{"des": u"高/城/动", "code": "G|C|D"},
	{"des": u"Z开头", "code": "Z"},
	{"des": u"T开头", "code": "T"},
	{"des": u"K开头", "code": "K"},
	{"des": u"普快", "code": ""},
	{"des": u"临客", "code": "L"}
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