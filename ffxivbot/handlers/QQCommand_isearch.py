from .QQEventHandler import QQEventHandler
from .QQUtils import *
from ffxivbot.models import *
import logging
import random
import logging
import traceback


def QQCommand_isearch(*args, **kwargs):
    action_list = []
    receive = kwargs["receive"]
    try:
        receive_msg = receive["message"].replace("/isearch", "", 1).strip()
        msg_list = receive_msg.split(" ")
        if len(msg_list) != 2:
            msg = "参数不足。\n用法：/isearch ja/zh/en/fr/de item"
        else:
            language = msg_list[0]
            name = msg_list[1]
            count = 0
            if language in ["ja", "zh", "en", "fr", "de"]:
                with open("all-items.json", "r", encoding='utf-8') as f:
                    items = json.loads(f.read())
                msg = ""
                for id in items:
                    if name in items[id]["zh"]:
                        count += 1
                        tmp = ""
                        for l, n in items[id].items():
                            if l in ["ja", "zh", "en"]:
                                tmp += "[" + l + ":" + n + "]"
                        msg += tmp + "\n"
                    if count == 5:
                        msg += "检索结果超过5条，请提高精确度。"
                        break
                print(msg)
            else:
                msg = "不可接受的语言。\n用法：/isearch ja/zh/en/fr/de item"
    except:
        msg = "未知错误"

    reply_action = reply_message_action(receive, msg)
    action_list.append(reply_action)
    return action_list
