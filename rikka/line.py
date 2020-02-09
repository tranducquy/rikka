# -*- coding: utf-8 -*-

import requests


class Line:
    def __init__(self, token):
        self.line_notify_token = token
        self.line_notify_api = 'https://notify-api.line.me/api/notify'
        self.line_notify = None

    def send_message(self, message):
        if self.line_notify_token == '':
            return
        if not message or message == '':
            return
        payload = {'message': message}
        headers = {'Authorization': 'Bearer ' + self.line_notify_token} 
        self.line_notify =  requests.post(self.line_notify_api, data=payload, headers=headers)

