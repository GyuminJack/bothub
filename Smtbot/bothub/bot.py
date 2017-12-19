# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function, unicode_literals)

from bothub_client.bot import BaseBot
from .smt import Translate


class Bot(BaseBot):
    """Represent a Bot logic which interacts with a user.
    BaseBot superclass have methods belows:
    * Send message
      * self.send_message(message, user_id=None, channel=None)
    * Data Storage
      * self.set_project_data(data)
      * self.get_project_data()
      * self.set_user_data(data, user_id=None, channel=None)
      * self.get_user_data(user_id=None, channel=None)
    When you omit user_id and channel argument, it regarded as a user
    who triggered a bot.
    """

    def handle_message(self, event, context):
        """I have two arguments.
        event is a dict and contains trigger info.
        {
           "trigger": "webhook",
           "channel": "<name>",
           "sender": {
              "id": "<chat_id>",
              "name": "<nickname>"
           },
           "content": "<message content>",
           "raw_data": <data itself webhook receives>
        }
        """
        message = event.get('content')
        if message == '/start':
	        self.send_start_message()
        else:
            self.translate_message(message)

    def send_start_message(self):
        self.send_message('안녕하세요. 인공신경망(N2MT) 기술이 적용된 네이버 파파고 번역 챗봇 입니다.\n'\
                          '한국어를 입력하시면 영어로 번역해 드립니다.')

    def translate_message(self, text):
        client_id = self.get_project_data()['client_id']
        secret = self.get_project_data()['secret']
        t = Translate(client_id, secret)
        msg = t.smt_translate(text)
        self.send_message(msg)
