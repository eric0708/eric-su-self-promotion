from linebot import (
    LineBotApi, WebhookHandler
)
import configparser
import requests
import json

config = configparser.ConfigParser()
config.read('config.ini')

headers = {"Authorization":"Bearer "+config.get('line-bot', 'channel_access_token'),"Content-Type":"application/json"}
"""
body = {
    "size": {"width": 2500, "height": 1686},
    "selected": "true",
    "name": "Control Panel",
    "chatBarText": "Control Panel",
    "areas":[
        {
          "bounds": {"x": 0, "y": 0, "width": 625, "height": 843},
          "action": {"type": "message", "text": "self introduction"}
        },
        {
          "bounds": {"x": 625, "y": 0, "width": 625, "height": 843},
          "action": {"type": "message", "text": "education"}
        },
        {
          "bounds": {"x": 1250, "y": 0, "width": 625, "height": 843},
          "action": {"type": "message", "text": "research interests"}
        },
        {
          "bounds": {"x": 1875, "y": 0, "width": 625, "height": 843},
          "action": {"type": "message", "text": "research experiences"}
        },
        {
          "bounds": {"x": 0, "y": 843, "width": 625, "height": 843},
          "action": {"type": "message", "text": "projects"}
        },
        {
          "bounds": {"x": 625, "y": 843, "width": 625, "height": 843},
          "action": {"type": "message", "text": "skills"}
        },
        {
          "bounds": {"x": 1250, "y": 843, "width": 625, "height": 843},
          "action": {"type": "message", "text": "certifications"}
        },
        {
          "bounds": {"x": 1875, "y": 843, "width": 625, "height": 843},
          "action": {"type": "message", "text": "extracurricular activities"}
        }
    ]
  }

req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu', 
                       headers=headers,data=json.dumps(body).encode('utf-8'))
print(req.text)
"""
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))

with open("images/richmenu.jpg", 'rb') as f:
    line_bot_api.set_rich_menu_image("richmenu-31fa38a0b19f247efda2df3b494e767f", "image/jpeg", f)

