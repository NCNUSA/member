from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from backend.models import GroupMember, Member

from .models import RecvMSG, Staff

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


def is_staff(user_id):
    """檢查是不是工作人員（幹部），才能查詢特殊資料"""

    return Staff.objects.filter(user_id=user_id).exists()


def is_chinese(word):
    """檢查是否每個字都是中文"""

    return all(u"\u4e00" <= c <= u"\u9fff" for c in word)


def ncnu_staff_contact(name):
    """查詢教職員資料"""
    import requests
    import json

    r = requests.get("https://bot.moli.rocks/ncnu-staff-contact/" + name)
    r = json.loads(r.text)
    total = len(r) - 1
    text = ""
    for index, val in enumerate(r):
        if index == 0:
            continue
        else:
            for f_index, i in enumerate(r[0]):
                text += i + "：" + val[f_index] + "\n"
            text += "\n"
    return total, text


def is_sid(recv):
    """檢查是不是學號格式"""
    # 檢查學號長度
    if len(recv) == 8 or len(recv) == 9:
        # 假定學生會付費會員在 2
        M = GroupMember.objects.filter(GP=2, MEMBER__SID=recv)
        if len(M) == 0:
            M = Member.objects.filter(SID=recv)
            if len(M) > 0:
                resp = "非付費會員，" + M[0].DEP + M[0].GRADE
            else:
                resp = "找不到此人"

        else:
            resp = "付費會員！"
            resp += M[0].MEMBER.CNAME + ": " + M[0].MEMBER.DEP + M[0].MEMBER.GRADE
    else:
        resp = "學號格式不正確"

    return resp


@csrf_exempt
def callback(request):

    if request.method == "POST":
        signature = request.META["HTTP_X_LINE_SIGNATURE"]
        body = request.body.decode("utf-8")

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                recv = event.message.text.strip()  # 收到的訊息
                resp = None  # 打算回覆的訊息
                user_id = event.source.user_id  # 傳訊息 LINE 帳號的 ID
                # 都是整數就準備來檢查看看是不是學號
                if recv.isdigit() and is_staff(user_id):
                    # 回傳學號資料
                    resp = is_sid(recv)
                elif is_chinese(recv):
                    total, contact = ncnu_staff_contact(recv)
                    if total > 0:
                        resp = contact
                    else:
                        resp = recv
                else:
                    resp = recv
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=resp))
                profile = line_bot_api.get_profile(user_id)
                RecvMSG.objects.create(user_id=user_id, display_name=profile.display_name, MSG=recv)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
