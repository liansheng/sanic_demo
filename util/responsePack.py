#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: responsePack.py
@time: 2017/12/8 17:28
"""

# # 3字头request参数校验异常
# "300": "请求参数异常",
# "360": "分页信息非数字类型",
# "370": "债券类型参数必须为字符串或None",
#
# # 4字头服务异常
# "400": None,
#
# # 5字头数据库异常
# "500": None,
#


# pack_mapping = {
#
#     # 100-199 用于指定客户端应相应的某些动作。
#
#     # 200-299 用于表示请求成功。
#     "2000": "OK",
#     "2001": "部分未成功",
#     "2010": "创建成功",
#
#     # 300-399 用于已经移动的文件并且常被包含在定位头信息中指定新的地址信息。
#
#     # 400-499 客户端原因导致服务器无法处理请求
#     "4000": "请求语法错误或者参数错误",
#     "4001": "请求条件不满足",
#     "4010": "没有登陆",
#     "4020": "用户不存在",
#     "4030": "没有权限",
#     "4040": "请求资源不存在",
#
#     # 500-599 服务器原因导致处理请求出错。
#     "5999": "服务器发生未知异常",
#     # 持仓
#     "5101": "债券:{0[0]} 日期:{0[1]} 账户:{0[2]} 不存在，请联系管理员！",
#     "5102": "新增每日持仓变动失败，原因: {0[0]}",
#     "5103": "指令单 [ {0[0]} ] 不存在！",
#     "5104": "创建每日持仓信息时获取昨日日期异常，异常日期: {0[0]}",
#     "5105": "标准券可用券[{0[0]}]小于质押量[{0[1]}]",
#     "5106": "持仓流中不存在该记录或该记录已经失效",
#
#     # 资金
#     "5111": "债券:{0[0]} 日期:{0[1]} 账户:{0[2]} 不存在，请联系管理员！",
#     "5112": "新增每日资金变动失败，原因: {0[0]}",
#     "5114": "创建每日资金信息时获取昨日日期异常，异常日期: {0[0]}",
#
#     "5120": "创建每日资金失败，原因: {0[0]}",
#     "5121": "当前日期[ {0[0]} ]不存在{0[1]}资金信息",
#     "5130": "创建每日持仓失败，原因: {0[0]}",
#
#     # 账户
#     "5201": "账户[ {0[0]} ]不存在!",
#     "5202": "执行指令单缺失账户",
#     "5203": "用户[ {0[0]} ]缺失{0[1]}账户!",
#
#     # fund依赖指令单
#     "5230": "指令单缺失业务类型",
#     "5231": "债券信息不存在",
#     "5232": "{0[0]}不存在，无法计算资金",
#     "5233": "每日资金、持仓计算发现未知的交易类型，未知交易类型代码：{0[0]}",
#     "5234": "缺失 {0[0]} 数据，无法录入资金、持仓",
#     "5235": "指令单 {0[0]} : {0[1]} 异常",
#     "5236": "指令单缺失 {0[0]} 信息",
#
#     # 财务拆借
#     "5240": "提交数据关键字 {0[0]} 不可为空！",
#     "5241": "{0[0]} : {0[1]} 值无效",
#     "5242": "财务拆借新增异常，异常信息：{0[0]}",
#     "5243": "删除记录不成功，原因：{0[0]}{0[1]}",
#
#     # 交易日历
#     "5210": "{0[0] 不为 {0[1]} 市场交易日}",
#     "5211": "市场为空不可查询当前日期是否为交易日",
#
#     "5301": "指令单[ {0[0]} ]不存在!",
#     "5302": "指令单交易场所非交易所",
#     "5303": "指令单缺失{0[0]}",
#     "5304": "指令单标准券出入库方向不为{0[0]}",
#     "5305": "{0[0]}不支持{0[1]}",
#     "5306": "交易类型{0[0]}{0[1]}[{0[2]}] 大于可操作总量[{0[3]}]",
#     "5307": "每日持仓流缺失对冲数据，执行失败",
#     # 债券
#     "5401": "债券基础信息 {0[0]} : {0[1]} 异常。",
#
#     # 6000-6999 查询出错
#     "6001": "数据库{0[0]}信息不存在或并不唯一",
#     "6002": "数据库{0[0]}信息为空",
#     "6003": "数据库{0[0]}不存在{0[1]}数据",
#
#     # 7000-8000 请求参数校验异常
#     "7001": "无效的请求日期",
#     "7002": "请求缺失必需参数 [ {0[0]} ]",
#     "7003": "请求参数[{0[0]} : {0[1]}]异常",
#     "7004": "无法识别的条件关系 : {0[0]}",
#     "7005": "范围过滤条件范围异常 : {0[0]}",
#     "7006": "不能识别的结算登记机构 : {0[0]}",
#     "7007": "接口只支持数组类型请求数据！",
#     "7008": "该债券不存在，请验证债券ID:{0[0]}",
#     "7009": "到期日期不可早于首期日期",
#     "7010": "请求参数 {0[0]} : {0[1]} ,不是有效参数。",
#     "7011": "请求参数 {0[0]} 不可为空",
#     "7012": "债券信息 {0[0]} 为空，请先编辑债券。",
#     "7013": "请求参数 {0[0]} 必须为{0[1]}类型",
#     "7014": "无法识别的请求参数{0[0]}",
#
#     # 8001 - 8999,内部接口数据校验异常
#     "8001": "{0[0]}不可为负",
#     "8002": "{0[0]}模块{0[1]},数据主键{0[2]}",
#     "8003": "{}非交易日不可执行操作",
#     "8004": "{}缺失关键信息:{}",
#     "8005": "{0[0]}未知{0[1]}",
#     "8006": "{0[0]}不可为空",
#     "8007": "{0[0]}存在不可识别的:{0[1]}",
#     "8008": "{0[0]}数据类型必须为:{0[1]}",
#     "8009": "{0[0]}无法识别的交易类型",
#     "8010": "文本识别异常:{0[0]}",
#
#     # 9000- 其他异常
#     "9000": "不存在债券 [ {0[0]} ] 现金流信息",
#     "9001": "保存数据发生错误:{0[0]}",
#     "9002": "数据库{0[0]}不存在[ {0[1]} ]的数据记录",
#     "9003": "存在无权访问信息:{0[0]}",
#     "9004": "用户[id:{0[0]}]不存在账户信息，请联系管理员添加",
#     "9005": "计算异常，{0[0]}不可为{0[1]}",
#     "9006": "数据库{0[0]}已经存在{0[1]}",
#     "9007": "Redis{0[0]}不存在{0[1]}",
#     "9008": "{0[0]}无法识别{0[1]}",
#
# }
pack_mapping = {
    "200": "成功",

    "400": "权限",
    "401": "用户权限不足",
    "404": "访问资源不存在",

    "500": "逻辑",
    "590": "kafka连接超时",
    "591": "kafka连接失败",

    "600": "参数校验",

    "601": "缺失用户身份信息",

    "700": "数据库",

    "701": "数据库已经存在该数据（违反唯一约束）",
    "790": "连接数据库超时",
    "791": "连接数据库失败",

    "999": "未捕获异常",
}


def response_package(code, results, message=None):
    """
    统一返回函数。没有code 添加。支持自定义message
    :param code:
    :param results:
    :param message:
    :return:
    """
    result = {}
    if pack_mapping.get(code):
        result['code'] = code
        if message:
            result["message"] = message
        else:
            result['message'] = pack_mapping.get(code)
        result['results'] = results
    else:
        result['code'] = "999"
        result['message'] = "响应代码未定义"
        result['results'] = {"code": code}
    return result


# results
# page_num
# page_size

# get list
"""
{
    "code":
    "message":
    "results":{
        "page_size":
        "page_num":
        "count":
        ...
    }
}
"""

# get detail
"""
{
    "code":
    "message":
    "results": serializer.data   
}
"""
# if __name__ == '__main__':
#     response = response_package("", {}, append=("山证", "2017-12-12", "main"))
#     print(response)
