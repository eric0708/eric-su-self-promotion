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

        if event.message.text == "self introduction":
            txt = Path('replies/intro.txt').read_text()
            txt = txt.replace('\n', '')
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=txt)
            )
        elif event.message.text == "projects":
            FlexMessage = json.load(open('replies/projects.json','r',encoding='utf-8'))
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage('projects',FlexMessage)
            )
        elif event.message.text == "Lazy Travel":
            txt = Path('replies/projects/lazytravel.txt').read_text()
            txt = txt.replace('\n', '')
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=txt)
            )
        elif event.message.text == "Financial Advisory Bot":
            txt = Path('replies/projects/financialadvisorybot.txt').read_text()
            txt = txt.replace('\n', '')
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=txt)
            )
        elif event.message.text == "Multi-Player Karting":
            txt = Path('replies/projects/multiplayerkarting.txt').read_text()
            txt = txt.replace('\n', '')
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=txt)
            )
        elif event.message.text == "Auto Shift Arrangement":
            txt = Path('replies/projects/autoshiftarrangement.txt').read_text()
            txt = txt.replace('\n', '')
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=txt)
            )
        elif event.message.text == "Anti-Thief System":
            txt = Path('replies/projects/antithiefsystem.txt').read_text()
            txt = txt.replace('\n', '')
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=txt)
            )
        elif event.message.text == "Classifiable Closet":
            txt = Path('replies/projects/classifiablecloset.txt').read_text()
            txt = txt.replace('\n', '')
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=txt)
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.message.text)
            )

if __name__ == "__main__":
    app.run()