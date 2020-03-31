from .QQEventHandler import QQEventHandler
from .QQUtils import *
from ffxivbot.models import *
import logging
import random
import requests
import traceback
import os
import json
from urllib.parse import quote

def QQCommand_isearch(*args, **kwargs):
    action_list = []
    receive = kwargs["receive"]
    msg = ""
    try:
        receive_msg = receive["message"].replace("/isearch", "").strip()
        msg_list = receive_msg.split(" ")
        if len(msg_list) != 2:
            msg = "参数不足。\n用法：/isearch ja/zh/en/fr/de item"
        else:
            language = msg_list[0]
            name = msg_list[1]
            count = 0
            if language in ["ja", "zh", "en", "fr", "de"]:
                with open("handlers/all-items.json", "r", encoding='utf-8') as f:
                    items = json.loads(f.read())
                for id in items:
                    if name in items[id][language]:
                        url = "https://xivapi.com/Item?ids=" + str(id) + "&columns=ID,Name_*,Icon,Recipes,GameContentLinks"
                        icon=json.loads(requests.get(url).text)["Results"][0]["Icon"]
                        msg += "[CQ:image,file=https://xivapi.com/" + icon + "]"
                        msg += "https://ff14.huijiwiki.com/index.php?search=" + quote(items[id]["zh"],'utf-8') + "\n| "
                        count += 1
                        for l, n in items[id].items():
                            if l in ["ja", "zh", "en"]:
                                msg += n + " | "
                        msg += "\n"
                    if count == 3:
                        msg += "检索结果超过3条，请提高精确度。"
                        break
                if count == 0:
                    msg = "没有找到数据"
            else:
                msg = "不可接受的语言。\n用法：/isearch ja/zh/en/fr/de item"
    except Exception as e:
        msg = "Error: {}".format(type(e))

    reply_action = reply_message_action(receive, msg)
    action_list.append(reply_action)
    return action_list
