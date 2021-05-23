from __future__ import unicode_literals
import os
import psycopg2
import configparser
import requests
import json
import datetime
from pathlib import Path
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage

app = Flask(__name__)

# basic information for LINE Chatbot
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

# set LINE Chatbot rich menu

"""
headers = {"Authorization":"Bearer "+config.get('line-bot', 'channel_access_token'),"Content-Type":"application/json"}

body = {
    "size": {"width": 2500, "height": 1686},
    "selected": "true",
    "name": "Controller",
    "chatBarText": "Controller",
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
richmenu_id = "richmenu-bca18a3ad10c9ffc246895d3dfbaf564"
headers = {"Authorization":"Bearer "+config.get('line-bot', 'channel_access_token'),"Content-Type":"application/json"}
"""
f = open("images/richmenu.jpg", 'rb')
line_bot_api.set_rich_menu_image(richmenu_id, "image/jpeg", f.read())
"""
req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/'+richmenu_id, 
                       headers=headers)
#print(req.text)

# connect to database and create table
try:
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    create_table_query = '''CREATE TABLE todo_list(
        record_no serial PRIMARY KEY,
        name VARCHAR (100) NOT NULL,
        todo VARCHAR (100) NOT NULL,
        deadline DATE NOT NULL
    );'''

    cursor.execute(create_table_query)
    conn.commit()

    cursor.close()
    conn.close()
except Exception:
    pass


# get information from LINE
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

# replies
@handler.add(MessageEvent, message=TextMessage)
def echo(event):
    
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":

        message_replied = False

        try:
            filename = event.message.text.replace(' ', '')
            txt = Path('replies/'+filename.lower()+'.txt').read_text()
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
                FlexSendMessage('Message',FlexMessage)
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

        try:
            filename = event.message.text.replace(' ','')
            filename = filename.replace('-','')
            txt = Path('replies/extracurricularactivities/'+filename.lower()+'.txt').read_text()
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
            txt = Path('replies/certifications/'+filename.lower()+'.txt').read_text()
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=txt)
            )
            message_replied = True
        except Exception:
            pass

        if event.message.text.split('\n')[0].lower() == 'add':
            todo_list = prepare_todo_list(event.message.text, event.source.user_id)
            txt = insert_todo_list(todo_list)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=txt)
            )
            message_replied = True
        elif event.message.text.split('\n')[0].lower() == 'delete':
            todo_list = prepare_todo_list(event.message.text, event.source.user_id)
            txt = delete_todo(todo_list)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=txt)
            )
            message_replied = True
        elif event.message.text.lower() == 'delete all':
            txt = delete_all_todos(event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=txt)
            )
            message_replied = True
        elif event.message.text.lower() == 'list all':
            txt = list_all_todos(event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=txt)
            )
            message_replied = True
        
        if message_replied == False:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.message.text)
            )

# prepare todo list
def prepare_todo_list(text, username):
    text_list = text.split('\n')
    todo_list = []

    for todo_item in text_list[1:]:
        temp_date = todo_item.split(' ')[0].split('/')
        todo_name = todo_item.split(' ', 1)[1]
        deadline = datetime.date(int(temp_date[0]), int(temp_date[1]), int(temp_date[2]))
        todo = (username, todo_name, deadline)
        todo_list.append(todo)
    
    return todo_list

# add todo list to database
def insert_todo_list(todo_list):
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    table_columns = '(name, todo, deadline)'
    postgres_insert_query = f"""INSERT INTO todo_list {table_columns} VALUES (%s,%s,%s)"""

    cursor.executemany(postgres_insert_query, todo_list)
    conn.commit()

    message = f"{cursor.rowcount} todo(s) added to the todo list"

    cursor.close()
    conn.close()

    return message

# delete todo
def delete_todo(todo_list):
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    postgres_delete_query = f"""Delete from todo_list where name = %s and todo = %s and deadline = %s"""

    cursor.executemany(postgres_delete_query, todo_list)
    conn.commit()

    message = f"{cursor.rowcount} todo(s) deleted!"

    cursor.close()
    conn.close()

    return message

# delete all todos
def delete_all_todos(username):
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    postgres_delete_query = f"""Delete from todo_list where name = %s"""
    
    cursor.execute(postgres_delete_query, (username,))
    conn.commit()

    message = f"{cursor.rowcount} todo(s) deleted!"

    cursor.close()
    conn.close()

    return message

# list all todos
def list_all_todos(username):
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    postgres_select_query = f"""SELECT * FROM todo_list where name = %s"""

    cursor.execute(postgres_select_query, (username,))
    todo_list = cursor.fetchall()

    if cursor.rowcount == 0:
        message = "No Todos"
    else: 
        message = "Todos\n"

        for todo in todo_list:
            todo_name = todo[2]
            todo_date = todo[3]
            message = message + str(todo_date.year)+'/'+str(todo_date.month)+'/'+str(todo_date.day)+' '+todo_name+'\n'
        
        message = message[0:-1]

    cursor.close()
    conn.close()

    return message


if __name__ == "__main__":
    app.run()