from __future__ import unicode_literals
import os

from flask import Flask, request, abort, render_template

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

import configparser

import urllib
import re
import random
import requests

from custom_models import call_database

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


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/index")
def index():
    # calldatabase = call_database()
    python_records = call_database.web_select_overall()
    return render_template("index.html", html_records=python_records)


# get msg from user
@handler.add(MessageEvent, message=TextMessage)
def pixabay_isch(event):

    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":

        if event.message.text == "Hello":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Hi 傻逼！")
            )

        if event.message.text == "time":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.timestamp)
            )

        if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.message.text)
            )


# callBackTimeTreeApi
# 接收 LINE 的資訊
@app.route("/callBackTimeTreeApi", methods=['GET'])
def callBackTimeTreeApi():

    # api-endpoint
    URL = "https://timetreeapp.com/oauth/authorize?client_id=YSQLrHS4gy7nEPBQAOuYugsfDxb1UkLjV7Q5NkilEn8&response_type=code&state=04HeI1F3a2y8R_GIL50WysrtcDU7G0zRqKD6DCCB4g8"
    # location given here
    # location = "delhi technological university"
    # defining a params dict for the parameters to be sent to the API
    # PARAMS = {'address': location}
    # sending get request and saving the response as response object
    r = requests.get(url=URL)

    # extracting data in json format
    # data = r.json()

    responseStr = r.get_data
    # extracting latitude, longitude and formatted address
    # of the first matching location
    # latitude = data['results'][0]['geometry']['location']['lat']
    # longitude = data['results'][0]['geometry']['location']['lng']
    # formatted_address = data['results'][0]['formatted_address']

    # try:
    #     handler.handle(body, signature)
    # except InvalidSignatureError:
    #     abort(400)

    return 'OK' + responseStr


if __name__ == "__main__":
    app.run()
