# coding:utf-8
import json

res_code = {
    'success': '10000',
    'error': '10001'
}

res_msg = {
    'msg': '',
    'data': '',
    'recode': res_code['success'],
}


class APIResponse:
    def __init__(self):
        self.ret = res_code['success']
        self.msg = ''
        self.data = ''

    def set_status(self, is_success, msg='', data=None):
        self.ret = res_code['success'] if is_success else res_code['error']
        self.msg = msg
        if not msg:
            self.msg = '操作成功' if is_success else '系统异常'
        self.data = data or ''

    def to_dict(self):
        res_msg['recode'] = self.ret
        res_msg['msg'] = self.msg
        res_msg['data'] = self.data

        return res_msg

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)
