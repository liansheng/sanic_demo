#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: tools.py
@time: 8/13/18 3:34 AM
"""
import random
import re
import string
from functools import wraps
from sanic_jwt import utils
from marshmallow import fields
import sanic.request

from util.config import do_main, default_head_portrait


def format_res(obj):
    print("obj is ", obj)
    if isinstance(obj, (list, tuple)) and isinstance(obj[0], (list, tuple)):
        l = []
        for tmp in obj:
            l += list(tmp)
        return format_res(l)
    if isinstance(obj, (list, tuple)) and isinstance(obj[0], dict):
        # [ {} ]
        d = {}
        for tmp in obj:
            d.update(tmp)
        for k, v in d.items():
            if isinstance(v, list):
                d[k] = " ".join(v)
        return " ".join(["{} {}".format(k, v) for k, v in d.items()])
    elif isinstance(obj, (list, tuple)):
        return obj[0]
    elif isinstance(obj, dict):
        return " ".join(["{} {}".format(k, v) for k, v in obj.items()])
    else:
        return str(obj)


def singleton(cls):
    """
    A singleton created by using decorator
    :param cls: cls
    :return: instance
    """
    _instances = {}

    @wraps(cls)
    def instance(*args, **kw):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kw)
        return _instances[cls]

    return instance


RANDOM_CHAR_SET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def random_str(l=8):
    res = ""
    for i in range(l):
        res += random.choice(RANDOM_CHAR_SET)
    return res


#
# def random_int(a=0, b=9, l=5):
#     res = ""
#     for i in range(l):
#         res += str(random.randint(a, b))
#     return res
import time


def exeTime(func):
    def newFunc(*args, **args2):
        t0 = time.time()
        print("@%s, {%s} start" % (time.strftime("%X", time.localtime()), func.__name__))
        back = func(*args, **args2)
        print("@%s, {%s} end" % (time.strftime("%X", time.localtime()), func.__name__))
        print("@%.3fs taken for {%s}" % (time.time() - t0, func.__name__))
        return back

    return newFunc


async def get_user_id_by_request(request):
    payload = request.app.auth.extract_payload(request, verify=False)
    user = await utils.call(
        request.app.auth.retrieve_user, request, payload=payload
    )
    user_id = await request.app.auth._get_user_id(user)
    return user_id


class ObjectID(fields.Field):
    """
    custom field or bson.ObjectID
    """

    def _serialize(self, value, attr, obj):
        return str(value)


async def head_portrait_change_change_change(res, default_key="head_portrait"):
    if isinstance(res, dict) and default_key in res.keys():
        pass
    else:
        return res
    head_portrait = res.pop(default_key, None)
    if head_portrait:
        res[default_key] = do_main + head_portrait
    else:
        res[default_key] = do_main + default_head_portrait
    return res


async def get_extra(request):
    """
    headers host request
    :param request:
    :return:
    """
    extra = {
        # 'method': getattr(request, 'method', 0),
        "headers": getattr(request, 'headers', ""),
    }

    # if isinstance(request, sanic_request):
    #     extra['byte'] = len(request.body)
    # else:
    #     extra['byte'] = -1

    extra['host'] = 'UNKNOWN'
    if request is not None:
        if request.ip:
            extra['host'] = '{0[0]}:{0[1]}'.format(request.ip)

        extra['request'] = '{0} {1}'.format(request.method,
                                            request.url)
    else:
        extra['request'] = 'nil'

    return extra


async def get_login_device(request):
    """
    :param request: http request
    :return: mobile | pc
    """
    if check_mobile(request):
        return "mobile"
    else:
        return "pc"


def check_mobile(request):
    """
    判断网站来自mobile还是pc
    demo :
        @app.route('/m')
        def is_from_mobile():
            if checkMobile(request):
                return 'mobile'
            else:
                return 'pc'
    :param request:
    :return:
    """
    if isinstance(request, str):
        userAgent = request
    else:
        userAgent = request.headers['User-Agent']
    # userAgent = env.get('HTTP_USER_AGENT')

    _long_matches = r'googlebot-mobile|android|avantgo|blackberry|blazer|elaine|hiptop|ip(hone|od)|kindle|midp|mmp|mobile|o2|opera mini|palm( os)?|pda|plucker|pocket|psp|smartphone|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce; (iemobile|ppc)|xiino|maemo|fennec'
    _long_matches = re.compile(_long_matches, re.IGNORECASE)
    _short_matches = r'1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|e\-|e\/|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|xda(\-|2|g)|yas\-|your|zeto|zte\-'
    _short_matches = re.compile(_short_matches, re.IGNORECASE)

    if _long_matches.search(userAgent) != None:
        return True
    user_agent = userAgent[0:4]
    if _short_matches.search(user_agent) != None:
        return True
    return False


if __name__ == '__main__':
    # print(random_str(5))
    # # print(random_int())
    # print(format_res(([{'registered_phone': '18119871135 已被注册'}],)))
    r = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
    res = check_mobile(r)
    print("check_mobile results is : ", res)
