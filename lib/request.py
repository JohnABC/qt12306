#coding: utf-8

import random
import requests
from lib import logger
from config import configCommon, configUrl

class Request(object):
	s = None

	def __init__(self):
		self.initS()

	def initS(self):
		self.s = requests.Session()
		self.s.verify = False #默认不验证对方证书
		self.setHeaders(self.getHeaders()) #默认header配置为get_headers方法中的配置

		return self
	
	def getUserAgent(self):
		userAgents = {
			"Safari_MAC": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
			"IE7": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
			"IE8": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
			"IE9": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
			"IE10": "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
			"Firefox4.0.1": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
			"Firefox5.0.1": "Mozilla/5.0 (Windows NT 6.1; rv:34.0) Gecko/20100101 Firefox/34.0",
			"Opera11.11_MAC": "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
			"Opera11.11_WIN": "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11"
		}
		return userAgents[random.choice(userAgents.keys())]

	def getHeaders(self):
		return {
			"Accept": "*/*",
			"Accept-Encoding": "gzip, deflate",
			"Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
			"Cache-Control": "no-cache",
			"Connection": "keep-alive",
			"If-Modified-Since": "0",
			"User-Agent": self.getUserAgent(),
			"X-Requested-With": 'XMLHttpRequest',
			"X-Forwarded-For": str(random.randint(58, 61)) + '.' + str(random.randint(10, 200)) + '.' + str(random.randint(10, 200)) + '.' + str(random.randint(10, 200))
		}

	def setHeaders(self, headers):
		self.s.headers.update(headers)
		return self

	def getHeadersHost(self):
		return self.s.headers["Host"]

	def setHeadersHost(self, host):
		self.s.headers.update({"Host": host})
		return self

	def getHeadersReferer(self):
		return self.s.headers["Referer"]
		
	def setHeadersReferer(self, referer):
		self.s.headers.update({"Referer": referer})
		return self

	def request(self, reqType, data = (), gp = 'GET', dataIsConfig = False, getR = False):
		"""
		真正执行请求的方法
		status分为6种 0 成功 1 超时 2返回码错误 3 不能被JSON 4 其他 5 页面返回码
		req_前缀防止与自定义POST时data重复
		"""
		
		rtn = {"status": configCommon.RS_SUC, "data": {}, "r": None}

		timeout = 20
		oldHost = ''
		oldReferer = ''

		urlData = configUrl.urls[reqType] if not dataIsConfig else data

		url = urlData["req_url"] % data if gp in ("GET", "GETJ") else urlData["req_url"]

		isLogResponseData = False

		if "req_log_url" in urlData and urlData["req_log_url"]:
			logger.log(u"url: %s" % url)
			if dataIsConfig:
				del urlData["req_log_url"]
		if "req_log_qdata" in urlData and urlData["req_log_qdata"]:
			if data:
				if (type(data) == type(()) and len(data) > 0):
					format = u"qdata:" + u":" .join([u"%s"] * len(data))
				else:
					format = u"qdata:%s"
				logger.log(format % data)
		if "req_log_pdata" in urlData and urlData["req_log_pdata"]:
			isLogResponseData = True
			if dataIsConfig:
				del urlData["req_log_pdata"]
		if "req_timeout" in urlData:
			timeout = urlData["req_timeout"]
			if dataIsConfig:
				del urlData["req_timeout"]
		if "req_host" in urlData:
			oldHost = self.getHeadersHost()
			self.setHeadersHost(urlData["req_host"])
			if dataIsConfig:
				del urlData["req_host"]
		if "req_referer" in urlData:
			oldReferer = self.getHeadersReferer()
			self.setHeadersReferer(urlData["req_referer"])
			if dataIsConfig:
				del urlData["req_referer"]

		r = None
		try:
			if gp in ('GET', 'GETJ'):
				r = self.s.get(url, timeout = timeout)
			else:
				r = self.s.post(url, data = data, timeout = timeout)

			if getR:
				rtn["r"] = r
			
			if r.status_code != 200:
				rtn["status"] = r.status_code
			elif gp in ('GETJ', 'POSTJ'):
				rtn["data"] = r.json()
			elif gp in ('GET', 'POST'):
				rtn["data"] = r.content

			if isLogResponseData:
				logger.log(u"pdata: %s" % rtn["data"])

		except (requests.ConnectionError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
			rtn["status"] = configCommon.RS_TIMEOUT
		except ValueError:
			#No JSON object could be decoded
			rtn["status"] = configCommon.RS_JSON_ERROR
			if r:
				rtn["data"] = r.content
		except (AttributeError, Exception) as e:
			#AttributeError 时为 'Session' object has no attribute 'redirect_cache'
			rtn["status"] = configCommon.RS_OTHER_ERROR

		if oldHost:
			self.setHeadersHost(oldHost)
		if oldReferer:
			self.setHeadersReferer(oldReferer)
		return rtn

	def get(self, type, params = (), getR = False):
		return self.request(type, params, 'GET', getR = getR)

	def getj(self, type, params = (), getR = False):
		return self.request(type, params, 'GETJ', getR = getR)

	def post(self, type, data = {}, getR = False):
		return self.request(type, data, 'POST', getR = getR)

	def postj(self, type, data = {}, getR = False):
		return self.request(type, data, 'POSTJ', getR = getR)