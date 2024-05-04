from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

from app.const import *


class LineBot:
    def __init__(self):
        self.channel_access_token = CHANNEL_ACCESS_TOKEN
        self.user_id = USER_ID
        self.line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

    def send_message(self, message):
        try:
            text_message = TextSendMessage(text=message)
            self.line_bot_api.push_message(self.user_id, messages=[text_message])
            print(f"Message sent: {message}")
        except LineBotApiError as e:
            print(f"Error sending message: {e}")

    def send_picture(self, picture):
        pass

    def send_video(self, video):
        pass

    def control_auto_feeder(self, amount):
        pass

    def control_camera_movement(self, command):
        pass

if __name__ == "__main__":
    LB = LineBot()
    LB.send_message('hello')