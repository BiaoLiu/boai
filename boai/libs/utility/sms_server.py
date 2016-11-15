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
account = "18665937537"
# 创蓝密码
password = "boai2016"


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

    data = {
        'account': account,
        'pswd': password,
        'msg': content,
        'mobile': mobile,
        'needstatus': 'false',
        'extno': ''
    }

    try:
        params = urllib.parse.urlencode(data)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = http.client.HTTPConnection(host, port=port, timeout=30)
        conn.request("POST", sms_send_uri, params, headers)
        response = conn.getresponse()
        result = response.read().decode()
        result_code = result.split(',')[1]
        conn.close()
        if result_code == '0':
            return True
        return False
    except Exception as e:
        return False


if __name__ == '__main__':
    mobile = "18665937537"
    content = "您的验证码是1234"

    # 查账户余额
    # print(get_user_balance())

    # 调用智能匹配模版接口发短信
    result = send_sms(mobile, content)
    print(result)
