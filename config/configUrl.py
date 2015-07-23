urls = {
	"leftTicketInit": {
		"req_url": "https://kyfw.12306.cn/otn/leftTicket/init",
		"req_log_url": True
	},
	"leftTicketLog": {
		"req_url": "https://kyfw.12306.cn/otn/leftTicket/log?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT",
		"req_log_url": True
	},
	"leftTicketQuery": {
		"req_url": "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT",
		"req_log_url": True
	},
	"leftTicketQueryT": {
		"req_url": "https://kyfw.12306.cn/otn/leftTicket/queryT?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT",
		"req_log_url": True
	},
	"leftTicketQueryTicketPrice": {
		"req_url": "https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no=%s&from_station_no=%s&to_station_no=%s&seat_types=%s&train_date=%s",
		"req_log_url": True,
		"req_log_pdata": True
	},
	"loginStatus": {
		"req_url": "https://kyfw.12306.cn/otn/login/checkUser", #是否是登录状态
		"req_log_url": True,
		"req_log_pdata": True
	},
	"loginSuggest": {
		"req_url": "https://kyfw.12306.cn/otn/login/loginAysnSuggest", #登录表单请求地址
		"req_log_url": True,
		"req_log_qdata": True,
		"req_log_pdata": True
	},
	"loginCheck": {
		"req_url": "https://kyfw.12306.cn/otn/login/userLogin", #登录后查看用户状态是否正常
		"req_log_url": True
	},
	"codeGet": {
		"req_url": "https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=%s&rand=%s&%s",
		"req_log_url": True
	},
	"codeCheck": {
		"req_url": "https://kyfw.12306.cn/otn/passcodeNew/checkRandCodeAnsyn",
		"req_log_url": True,
		"req_log_pdata": True
	},
	"orderNoComplete": {
		"req_url": "https://kyfw.12306.cn/otn/queryOrder/queryMyOrderNoComplete",
		"req_log_url": True,
		"req_log_pdata": True
	},
	"orderInit": {
		"req_url": "https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest", #初始化订单页
		"req_log_url": True,
		"req_log_qdata": True,
		"req_log_pdata": True
	},
	"orderInitDc": {
		"req_url": "https://kyfw.12306.cn/otn/confirmPassenger/initDc", #获取单程票页面提交订单所用的token等
		"req_log_url": True
	},
	"orderCheck": {
		"req_url": "https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo", #预提交订单
		"req_log_url": True,
		"req_log_qdata": True,
		"req_log_pdata": True
	},
	"orderQueue": {
		"req_url": "https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount", #获取订单排队信息
		"req_log_url": True,
		"req_log_qdata": True,
		"req_log_pdata": True
	},
	"orderConfirmForQueue": {
		"req_url": "https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue", #排完队确认下单
		"req_log_url": True,
		"req_log_qdata": True,
		"req_log_pdata": True
	},
	"orderWait": {
		"req_url": "https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random=%s&tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN=%s",
		"req_log_url": True,
		"req_log_pdata": True
	},
	"orderResult": {
		"req_url": "https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue", #获取订单结果
		"req_log_url": True,
		"req_log_qdata": True,
		"req_log_pdata": True
	},
	"passengerAll": {
		"req_url": "https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs",
		"req_log_url": True
	},
	"passengerAdd": {
		"req_url": "https://kyfw.12306.cn/otn/passengers/realAdd",
		"req_log_url": True,
		"req_log_qdata": True,
		"req_log_pdata": True
	}
}

