#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import base64
import time
import var


def request_bot_api(isWelcome=True, sender_id='0', uuid='0', *args):
    if isWelcome:
        type = 'payload'
        content = "Welcome#" + encode_base64(*args)
    else:
        type = 'text'
        content = args[0]

    url = var.URL_BOT
    h = {'Authorization': 'Bearer ' + var.API_TOKEN_BOT,
         'Cache-Control': 'no-cache',
         'Content-Type': 'application/json'}

    d = {'channel': 'api',
         'app_code': var.API_APP_BOT,
         'sender_id': uuid,
         'sender_name': sender_id,
         'type': type,
         'message': {
             'content': content,
             'type': type
         }
         }

    json_data = json.dumps(d)
    # print(json_data)

    response = requests.post(url,
                             headers=h,
                             data=json_data)
    r = response.json()
    status = r['Success']
    return status


def get_answer(sender_id):
    url = var.URL_WEBHOOK
    response = requests.get(url,
                            params={'sender_id': sender_id})
    r = response.content
    return r


def encode_base64(*args):
    js = {}
    js["set_attributes"] = {}
    for i in range(int(len(args) / 2)):
        js["set_attributes"][args[i * 2]] = args[i * 2 + 1]
    js_text = json.dumps(js)
    print(js_text)
    return base64.b64encode(js_text)


def check_end(text):
    if text[-3:] == '!!!':
        return True
    return False
