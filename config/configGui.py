#-*- coding: utf-8 -*-

import os
import configCommon
from PyQt4.QtGui import *
from PyQt4.QtCore import *

charset = "utf8"
windowTitle = u"刷票小助手"
mainWindowWidth = 900
mainWindowHeight = 600
trainTableHeight = 350
postListWidth = 100
rushTextWidth = 70
rushWidgetWidth = 75
verifyCodeWidth = 293
verifyCodeHeight = 190
splashKeepTime = 2
splashOpacityChangeNum = 0.02
splashOpacityChangeTime = 0.04
registerUrl = "https://kyfw.12306.cn/otn/regist/init"
forgetUrl = "https://kyfw.12306.cn/otn/forgetPassword/initforgetMyPassword"
vcodeImageTipHeight = 30

def imageDir():
	return os.path.join(configCommon.getWorkDir(), "gui", "images")

def getImage(imageName):
	return os.path.join(imageDir(), imageName)