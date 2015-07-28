#-*- coding: utf-8 -*-

import random
from request import Request
from config import configUrl

_instance = None
def getInstance():
	global _instance
	if not _instance:
		_instance = Train()
	return _instance

class Train(Request):
	_vcode = None

	def reqVCodeImage(self, module, rand):
		return self.get("codeImage", (module, rand, str(random.random())))

	def reqVCodeCheck(self, rand, randCode):
		return self.postj("codeCheck", {"rand": rand, "randCode": randCode})
		
	def reqLoginStatus(self):
		return self.getj("loginStatus")

	def reqLoginSuggest(self, data):
		data.update({"myversion": "undefined"})
		return self.postj("loginSuggest", data)

	def reqLoginCheck(self):
		#此方法暂时没有用上, 本应在登录成功后请求
		return self.postj("loginCheck", {"_json_att": ""})
		
	def reqNoCompleteOrder(self):
		return self.getj("orderNoComplete")
		
	def isLoginSuccess(self, data):
		return "data" in data and "loginCheck" in data["data"] and data["data"]["loginCheck"] == "Y"
		
	def isVCodeRight(self, data):
		return "data" in data and "result" in data["data"] and data["data"]["result"] == "1"

	def isLoginStatus(self, data):
		return "data" in data and flag in data["data"] and data["data"]["flag"]
		
	def getLoginFailedReason(self, data):
		if "messages" in data and len(data) > 0:
			return data["messages"][0]
		else:
			return ""