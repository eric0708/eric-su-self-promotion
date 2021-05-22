from __future__ import unicode_literals
import os
import configparser
import json
from pathlib import Path
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def echo(event):
    
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":

        message_replied = False

        try:
            filename = event.message.text.replace(' ', '')
            txt = Path('replies/'+filename.lower()+'.txt').read_text()
            txt = txt.replace('\n', '')
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=txt)
            )
            message_replied = True
        except Exception:
            pass

        try:
            filename = event.message.text.replace(' ', '')
            FlexMessage = json.load(open('replies/'+filename.lower()+'.json','r',encoding='utf-8'))
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage('projects',FlexMessage)
            )
            message_replied = True
        except Exception:
            pass
        
        try:
            filename = event.message.text.replace(' ','')
            filename = filename.replace('-','')
            txt = Path('replies/projects/'+filename.lower()+'.txt').read_text()
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=txt)
            )
            message_replied = True
        except Exception:
            pass

        try:
            filename = event.message.text.replace(' ','')
            filename = filename.replace('-','')
            txt = Path('replies/researches/'+filename.lower()+'.txt').read_text()
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=txt)
            )
            message_replied = True
        except Exception:
            pass

        if message_replied == False:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.message.text)
            )

if __name__ == "__main__":
    app.run()