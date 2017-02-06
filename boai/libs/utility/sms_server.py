# coding: utf-8

import http.client
import urllib
import requests

# 服务地址
host = "http://222.73.117.169"
# 端口号
port = 80
# 版本号
version = "v1.1"

# 查账户信息的URI
balance_get_uri = "/msg/QueryBalance"
# 智能匹配模版短信接口的URI
sms_send_uri = "/msg/HttpBatchSendSM"

# 创蓝账号
account = "#########"
# 创蓝密码
password = "#########"


def get_user_balance():
    """
    查询账户余额
    """
    conn = http.client.HTTPConnection(host, port=port)
    conn.request('GET', balance_get_uri + "?account=" + account + "&pswd=" + password)
    response = conn.getresponse()
    response_str = response.read().decode()
    conn.close()
    return response_str


def send_sms(mobile, content):
    """
    调用接口发短信
    """
    try:
        params = {
            'account': account,
            'pswd': password,
            'msg': content,
            'mobile': mobile,
            'needstatus': 'false',
            'extno': ''
        }
        result = requests.post(host + sms_send_uri, params)
        result_code = result.text.split(',')[1]
        if result_code == '0':
            return True
        return False
    except Exception as e:
        return False


if __name__ == '__main__':
    mobile = "18665937537"
    content = "【博爱】您的验证码是：1234"

    # 查账户余额
    # balance = get_user_balance()
    # print(balance)

    # 调用智能匹配模版接口发短信
    result = send_sms(mobile, content)
    print(result)
