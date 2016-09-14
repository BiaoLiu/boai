# coding: utf-8

import http.client
import urllib

# 服务地址
host = "sapi.253.com"
# 端口号
port = 80
# 版本号
version = "v1.1"

# 查账户信息的URI
balance_get_uri = "/msg/QueryBalance"
# 智能匹配模版短信接口的URI
sms_send_uri = "/msg/HttpBatchSendSM"

# 创蓝账号
account = "jiekou-ceshi-yzm"
# 创蓝密码
password = "HJield565"


def get_user_balance():
    """
    取账户余额
    """
    conn = http.client.HTTPConnection(host, port=port)
    conn.request('GET', balance_get_uri + "?account=" + account + "&pswd=" + password)
    response = conn.getresponse()
    response_str = response.read().decode()
    conn.close()
    return response_str


def send_sms(text, mobile):
    """
    使用接口发短信
    """
    params = urllib.parse.urlencode({'account': account, 'pswd': password, 'msg': text, 'mobile': mobile, 'needstatus': 'false', 'extno': ''})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection(host, port=port, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read().decode()
    conn.close()
    return response_str


if __name__ == '__main__':
    mobile = "18665937537"
    text = "您的验证码是1234"

    # 查账户余额
    # print(get_user_balance())

    # 调用智能匹配模版接口发短信
    print(send_sms(text, mobile))
