# 載入需要的模組
from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

import configparser

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

# LINE 聊天機器人的基本資料
# line_bot_api = LineBotApi('9avKOw7GijsNNXTwd3HcaD5cxa80jjkWue+YrDR8m7f9tmf7e2JjmOPyRwTrT7tkYjbzio0KjOM1ocHGgR2JHFZYxEAxN1wHRRcrxIo1iaWax7FONdhJDsu3lzrWZtZKZ5M23MJ/kgUqoLtLvKh/zgdB04t89/1O/w1cDnyilFU=')
# handler = WebhookHandler('514dc4daa432d2c264ed0ab85ad62b73')

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

    if event.message.text == "Hello":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Hi 傻逼！")
        )

    if event.message.text == "time":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = event.timestamp)
        )


    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )

if __name__ == "__main__":
    app.run()
