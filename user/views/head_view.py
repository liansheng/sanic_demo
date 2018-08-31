#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: head_view.py
@time: 8/30/18 7:50 PM
"""
import hashlib
import os
from sanic.response import json
from sanic.views import HTTPMethodView

from models.user_model import UserModel
from util.config import HEAD_PATH
from PIL import Image


# 获取图片后缀名
from util.setting import app
from util.tools import get_user_id_by_request


def get_suffix(filename):
    temp_addr = filename.split('.')
    suffix = temp_addr[-1]
    file_type = ['jpg', 'jpeg', 'bmp', 'png']
    assert len(temp_addr) >= 2, ("错误的文件名", "upload file name is {}".format(filename))
    assert suffix.lower() in file_type, ("错误的文件格式", "upload file name is {}".format(filename))
    return suffix


class UploadImageView(HTTPMethodView):
    """
         上传图片文件接口,
         business and functionality should be separated, and, too lazy to write
    """
    def __init__(self):
        self.collection = app.mongo["account_center"].user
        self.user_model = UserModel(self.collection)

    async def post(self, request):
        user_id = await get_user_id_by_request(request)

        return_data = {
            "message": "success",
            "code": "200",
            "results": {}
        }

        image = request.files.get('file', None)
        assert image, "文件对象名字不正确"
        image = image.body
        # 判断文件是否支持
        image_name = request.files.get('file').name
        image_suffix = get_suffix(image_name)
        if 'error' in image_suffix:
            return_data['code'] = "300"
            return_data['message'] = "图片不支持"
            return json(return_data)
        # 组织图片存储路径
        m1 = hashlib.md5()
        m1.update(image)
        md5_name = m1.hexdigest()

        # 用 md5 的前两位来建文件夹，防止单个文件夹下图片过多，又或者根目录下建立太多的文件夹
        save_dir = HEAD_PATH + md5_name[0:2] + '/'
        save_path = save_dir + md5_name[2:] + '.' + image_suffix
        res_path = '/' + md5_name[0:2] + '/' + md5_name[2:] + '.' + image_suffix

        # 如果文件夹不存在，就创建文件夹
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # 将文件写入到硬盘
        temp_file = open(save_path, 'wb')
        temp_file.write(image)
        temp_file.close()
        #
        im = Image.open(HEAD_PATH + res_path)

        sum_path = "/static/img/user/head/" + res_path
        print(sum_path, res_path)

        await self.user_model.update_head(user_id, sum_path)
        # 给客户端返回结果
        return_data['results']['path'] = sum_path
        return_data['results']['width'] = im.size[0]
        return_data['results']['height'] = im.size[1]
        return json(return_data)
