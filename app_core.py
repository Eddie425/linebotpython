from __future__ import unicode_literals

from flask import Flask, request, abort, render_template

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
from timetree_sdk import TimeTreeApi
import configparser

import requests
import json

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
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.timestamp)
            )

        if event.message.text == "event":

            client_id = "YSQLrHS4gy7nEPBQAOuYugsfDxb1UkLjV7Q5NkilEn8"
            api = TimeTreeApi(csrf_token)

            event = Event(
                data=EventData(
                    attributes=EventAttributes(
                        title='Zoe Teacher',
                        category='schedule',
                        all_day=False,
                        start_at='2021-01-27T11:00:00.000Z',
                        end_at='2021-01-27T13:00:00.000Z',
                        description='Description',
                        location='Taipei',
                        start_timezone='Asia/Taipei',
                        end_timezone='Asia/Taipei'
                    ),
                    relationships=EventRelationships(
                        label=EventRelationshipsLabel(
                            data=EventRelationshipsLabelData(
                                id='1',
                                type='label'
                            )
                        ),
                        # attendees=EventRelationshipsAttendees(
                        #     data=[EventRelationshipsAttendeesData(
                        #         id='USER_ID',
                        #         type='user'
                        #     )]
                        # )
                    )
                )
            )
            response = api.create_event('zizBvYcXdFur', event)
            print(response.data.attributes.title)  # Title

            calendar = api.get_calendar('zizBvYcXdFur')
            print(" Calendar = " + calendar.data.attributes.name)

            events = api.get_upcoming_events('zizBvYcXdFur', 'Asia/Taiwan', 7)
            print("title : " + events.data[0].attributes.title)
            print("category : " + events.data[0].attributes.category)
            print("all_day : " + str(events.data[0].attributes.all_day))
            print("start_at : " + events.data[0].attributes.start_at)
            print("start_timezone : " + events.data[0].attributes.start_timezone)
            print("end_at : " + events.data[0].attributes.end_at)
            print("end_timezone : " + events.data[0].attributes.end_timezone)
            print("description : " + events.data[0].attributes.description)
            print("location : " + events.data[0].attributes.location)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Create Event OK~" + "  title : " + events.data[0].attributes.title)
            )


        if "https://" in event.message.text:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="user_id = " + event.source.user_id)
            )


# callBackTimeTreeApi
# 接收 LINE 的資訊
@app.route("/callBackTimeTreeApi", methods=['GET'])
def callBackTimeTreeApi():

    redirect_uri = "https://lineboteddie.herokuapp.com/callBackTimeTreeApi"
    # client_id = "YSQLrHS4gy7nEPBQAOuYugsfDxb1UkLjV7Q5NkilEn8"
    api = TimeTreeApi(csrf_token)
    calendar = api.get_calendar('zizBvYcXdFur')

    print(" Calendar = " + calendar.data.attributes.name)

    events = api.get_upcoming_events('zizBvYcXdFur', 'Asia/Taiwan', 7)
    print("title : " + events.data[0].attributes.title)
    print("category : " + events.data[0].attributes.category)
    print("all_day : " + str(events.data[0].attributes.all_day))
    print("start_at : " + events.data[0].attributes.start_at)
    print("start_timezone : " + events.data[0].attributes.start_timezone)
    print("end_at : " + events.data[0].attributes.end_at)
    print("end_timezone : " + events.data[0].attributes.end_timezone)
    print("description : " + events.data[0].attributes.description)
    print("location : " + events.data[0].attributes.location)
    # print("url : " + events.data[0].attributes.url)
    # print("title : " + events.data[0].attributes.label)
    # most recent event title in 7 days
    # for k, v in calendar:
    #     print(k, v)
    # calendar_json = json.dumps(calendar.data.__dict__)
    # print(calendar_json)
    # print(calendar_json.toString())
    # print(calendar.data.attributes)
    # print(oauth_authorize_url)
    return render_template("home.html")

    # calendar name
    # api-endpoint
    # location given here
    # location = "delhi technological university"
    # defining a params dict for the parameters to be sent to the API
    # PARAMS = {'address': location}
    # sending get request and saving the response as response object
    # r = requests.get(url=URL)

    # extracting data in json format
    # data = r.json()

    # responseStr = r.text
    # extracting latitude, longitude and formatted address
    # of the first matching location
    # latitude = data['results'][0]['geometry']['location']['lat']
    # longitude = data['results'][0]['geometry']['location']['lng']
    # formatted_address = data['results'][0]['formatted_address']

    # try:
    #     handler.handle(body, signature)
    # except InvalidSignatureError:
    #     abort(400)

    # return 'OK' + responseStr


if __name__ == "__main__":
    app.run()
