from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

app = Flask(__name__)

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi('g62fEOo+1EOpCWsm9nk/HxJ6CE4d+s2Ooc1F4h59elp84ksecsI29/gFJR/CbVhPYyOvbFXKzuxhLLvJR77SVr5AEi9LIRbWlI27ZocxDVyPwAdKSf4HsHNAlvF94ff53PZ8WRYGUVDKjWc1sQ2cuwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('acdf47c028bbd0d84fa5074276e0c160')

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
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )

if __name__ == "__main__":
    app.run()