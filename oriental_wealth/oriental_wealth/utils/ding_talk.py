import json
from scrapy.crawler import logger

import requests


def ding_push_message(url, tag, msg, is_all=False, at_mobiles=None):
    """
    钉钉推送
    :param is_all: @所有人
    :param tag: 任务标记
    :param url: https://oapi.dingtalk.com/robot/send?access_token=xxxxx
    :param msg:
    :param at_mobiles:
    :return:
    """
    msg = f'{tag}: ' + msg  # 关键词spider, 必加
    at_mobile_list = [] if not at_mobiles else at_mobiles
    # 构建请求头部
    headers = {"Content-Type": "application/json", "Charset": "UTF-8"}
    # 构建请求数据
    message = {"msgtype": "text", "text": {"content": msg},
               # atMobiles被@人的手机号,"isAtAll": False，True：控制@所有人
               "at": {"atMobiles": at_mobile_list, "isAtAll": is_all}
               }
    try:
        response = requests.post(
            url=url,
            data=json.dumps(message),
            headers=headers)
        response.close()
        result = response.json()
        if result.get("errcode") == 0:
            return True
        else:
            raise Exception(result.get("errmsg"))
    except Exception as e:
        logger.error("报警发送失败。 报警内容 {}, error: {}".format(message, e))
        return False
