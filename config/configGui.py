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
logoIconImage = os.path.join(configCommon.getWorkDir(), "gui", "images", "logo.ico")

def getLinkLabel(label, link, style = "color:blue"):
	labelWidget = QLabel(QWidget.tr('<a href="%s" style="%s">%s</a>' % (link, style, label)))
	labelWidget.setOpenExternalLinks(True)