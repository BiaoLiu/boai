# coding: utf-8
import json
import os
import time
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt


def test(request):
    xml = '<xml><return_code><![CDATA[{0}]]></return_code><return_msg><![CDATA[{1}]]></return_msg></xml>' \
        .format('200', 'OK')

    request.session['user_id'] = 1

    return redirect('/wechat/register/1/?next=/wechat/main/')

    # return HttpResponse(xml,content_type='text/xml')


@csrf_exempt
def uploadimg(request):
    if request.method == 'POST':
        file_obj = open("log.txt", "w+")
        buf = request.FILES.get('imgFile', None)
        print(file_obj, str(buf))
        file_buff = buf.read()
        time_format = str(time.strftime("%Y-%m-%d-%H%M%S", time.localtime()))
        try:
            file_name = "img_" + time_format + ".jpg"
            save_file("main/static/content_img", file_name, file_buff)
            dict_tmp = {}
            dict_tmp["error"] = 0
            dict_tmp["url"] = "/static/content_img/" + file_name
            return HttpResponse(json.dumps(dict_tmp))
        except Exception as e:
            dict_tmp = {}
            dict_tmp["error"] = 1
            print(file_obj, e)
            return HttpResponse(json.dumps(dict_tmp))


# 对path进行处理
def mkdir(path):
    # 去除左右两边的空格
    path = path.strip()
    # 去除尾部 \符号
    path = path.rstrip("\\")

    if not os.path.exists(path):
        os.makedirs(path)
    return path


# 保存相关的文件
def save_file(path, file_name, data):
    if data == None:
        return

    mkdir(path)
    if (not path.endswith("/")):
        path = path + "/"
    file = open(path + file_name, "wb")
    file.write(data)
    file.flush()
    file.close()
