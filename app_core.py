# 載入需要的模組
from __future__ import unicode_literals
import os
import configparser
import urllib
import requests
from bs4 import BeautifulSoup
import json
import update_game_info 
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError,LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, StickerMessage,ImageSendMessage, FlexSendMessage
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

@handler.add(MessageEvent, message=TextMessage)
def show_past_games(messevent):
    if messevent.message.text == "過去比賽資訊":
        all_past_games = update_game_info.update_past_games()
        all_past_games_carousel = FlexSendMessage(
                        alt_text='過去比賽資訊',
                        contents={
                            "type": "carousel",
                            "contents":all_past_games
                        }
                    )
        line_bot_api.reply_message(
            messevent.reply_token,
            all_past_games_carousel
            )
    elif messevent.message.text == "近期比賽資訊":
        all_future_games = update_game_info.update_future_games()
        all_future_games_carousel = FlexSendMessage(
                        alt_text='近期比賽資訊',
                        contents={
                            "type": "carousel",
                            "contents":all_future_games
                        }
                    )
        line_bot_api.reply_message(
            messevent.reply_token,
            all_future_games_carousel
            )
    elif messevent.message.text == "各隊資訊":
        all_team_info = update_game_info.update_teams()
        all_team_carousel = FlexSendMessage(
                        alt_text='全部隊伍資訊',
                        contents={
                            "type": "carousel",
                            "contents":all_team_info
                        }
                    )
        line_bot_api.reply_message(
            messevent.reply_token,
            all_team_carousel
            )
        



if __name__ == "__main__":
    app.run()