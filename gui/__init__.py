#-*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from base import Base
from init import Init
from main import Main
from login import Login
from splash import Splash
from verify import Verify

from config import configGui

QTextCodec.setCodecForTr(QTextCodec.codecForName(configGui.charset))

__all__ = ["Splash", "Login", "Main", "Verify", "Base"]