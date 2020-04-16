from .QQEventHandler import QQEventHandler
from .QQUtils import *
from ffxivbot.models import *
import logging
import random
import requests
import traceback
import os
import json
import re


def get_price(id):
    result = ""
    SALE = False
    cookies = {
        "mogboard_server": "Shinryu",
        "mogboard_language": "ja",
        "mogboard_timezone": "Asia/Tokyo"
    }
    urlget = requests.get("https://universalis.app/market/" + str(id), cookies=cookies)
    data = re.findall("<div class=\"cheapest\">(.*?)</div>", urlget.text, re.S)
    date = re.findall("<div>.*?<h4>(.*?)</h4>.*?<div>(.*?)</div>", urlget.text, re.S)[:11]
    server_update_time={}
    for each in date:
        SALE = True
        server_update_time[each[0]]=each[1]

    for each in data:
        itype = re.findall("<h2>(.*?)</h2>", each, re.S)[0]
        try:
            icount = re.findall("<em>(.*?)</em>", each, re.S)[0]
            iserver = re.findall("Server: <strong>(.*?)</strong>", each, re.S)[0]
            iprice = re.findall("<span class=\"cheapest_value\">(.*?)</span>", each, re.S)[0]
            result += "{} {} {} {} {}\n".format(itype, iserver, icount, iprice, server_update_time[iserver])
        except:
            result += "{} 没有数据\n".format(itype)
    if not SALE:
        result = "此物品不可出售\n"
    return result

def QQCommand_price(*args, **kwargs):
    action_list = []
    receive = kwargs["receive"]
    try:
        receive_msg = receive["message"].replace("/price", "").strip()
        msg_list = receive_msg.split(" ")
        msg = ""
        if len(msg_list) != 2:
            msg = "参数不足。\n用法：/price ja/zh/en/fr/de item"
        else:
            language = msg_list[0]
            name = msg_list[1]
            count = 0
            if language in ["ja", "zh", "en", "fr", "de"]:
                with open("handlers/all-items.json", "r", encoding='utf-8') as f:
                    items = json.loads(f.read())
                for id in items:
                    if name in items[id][language]:
                        msg += "id: " + id + " | "
                        count += 1
                        for l, n in items[id].items():
                            if l in ["ja", "zh", "en"]:
                                msg += n + " | "
                        msg += "\n"
                        msg += "https://universalis.app/market/" + str(id) +"\n"
                        msg += get_price(id)
                    if count == 3:
                        msg += "检索结果超过3条，请提高精确度。"
                        break
                if count == 0:
                    msg = "没有找到数据"
            else:
                msg = "不可接受的语言。\n用法：/price ja/zh/en/fr/de item"
    except Exception as e:
        msg = "Error: {}".format(type(e))

    reply_action = reply_message_action(receive, msg)
    action_list.append(reply_action)
    return action_list

