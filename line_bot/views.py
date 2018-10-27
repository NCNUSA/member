# import 必要的函式庫
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
from backend.models import *

# 這邊是Linebot的授權TOKEN(等等註冊LineDeveloper帳號會取得)，我們為DEMO方便暫時存在settings裡面存取，實際上使用的時候記得設成環境變數，不要公開在程式碼裡喔！

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):

    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                recv = event.message.text.strip()
                resp = None
                if recv.isdigit():
                    if len(recv) == 8 or len(recv) == 9:
                        M = GPM.objects.filter(GP=2, MEMBER__SID=recv)
                        if len(M) == 0:
                            M = Member.objects.filter(SID=recv)
                            if len(M) > 0:
                                resp = '非付費會員，' + M[0].DEP + M[0].GRADE
                            else:
                                resp = '找不到此人'

                        else:
                            resp = '付費會員！'
                            resp += M[0].MEMBER.CNAME + ': ' + M[0].MEMBER.DEP + M[0].MEMBER.GRADE
                    else:
                        resp = '學號格式不正確'
                else:
                    resp = recv
                line_bot_api.reply_message(
                    event.reply_token,
                   TextSendMessage(text=resp)
                )
                print(event.source)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
