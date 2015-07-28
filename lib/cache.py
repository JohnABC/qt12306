#-*- coding: utf-8 -*-

import os
import pickle
from config import configCommon

def readCache(cacheType):
	rtn = None
	filename = configCommon.getCacheFile(cacheType)
	if (os.path.exists(filename) and os.path.isdir(filename)):
		with open(filename, "rb") as f:
			rtn = pickle.load(f)
			
	return rtn
	
def writeCache(cacheType, data):
	filename = configCommon.getCacheFile(cacheType)
	with open(filename, "wb") as f:
		pickle.dump(data, f)