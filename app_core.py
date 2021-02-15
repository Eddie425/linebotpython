from __future__ import print_function
from __future__ import unicode_literals

from flask import Flask, request, abort, render_template

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
from timetree_sdk import TimeTreeApi
import configparser

from timetree_sdk.models import Event, EventData, EventAttributes, EventRelationships, EventRelationshipsLabel, \
    EventRelationshipsLabelData, EventRelationshipsAttendees, EventRelationshipsAttendeesData

from custom_models import call_database

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
csrf_token = "bEWJkgE2sU9-7FKEVIdItGhgw9bBGNf3wxkhHvv_moLJW9gw"


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


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/index")
def index():

    python_records = call_database.web_select_overall()
    return render_template("index.html", html_records=python_records)


# get msg from user
@handler.add(MessageEvent, message=TextMessage)
def pixabay_isch(event):
    print(event)
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":

        if event.message.text == "Hello":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Hi 傻逼！")
            )

        if event.message.text == "time":
            event.reply({
                "type": 'template',
                "altText": 'this is a buttons template',
                "template": {
                    "type": 'buttons',
                    "thumbnailImageUrl": 'https://example.com/bot/images/image.jpg',
                    "title": '開啟菜單',
                    "text": '❗️注意:請先確認您line版本在7.12.0以上',
                    "actions": [{
                        "type": 'datetimepicker',
                        "label": '我要新增',
                        "data": 'create',
                        "mode": 'datetime',
                    }, {
                        "type": 'datetimepicker',
                        "label": '我要查詢',
                        "data": 'search',
                        "mode": 'datetime',
                    }]
                }
            })

        if "https://" in event.message.text:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="user_id = " + event.source.user_id)
            )


if __name__ == "__main__":
    app.run()
