#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import var


def speech_recognition(file_path):
    success = False
    while not success:
        try:
            audio = audio_to_byte(file_path)

            url = var.URL_STT
            response = requests.post(url,
                                     data=audio,
                                     headers={'api_key': var.API_KEY_STT,
                                              'Content-Type': ''})
            r = response.json()
            status = r['status']
            text = ''
            # print(json.dumps(r))
            if status == 0:
                text = r['hypotheses'][0]['utterance']
            success = True
        except:
            print("FAILED")
    return status, text.encode('utf-8')


def audio_to_byte(file_path):
    # file_path =  record_path + record_file
    audio_in_byte = ''
    # max_size = 1024
    with open(file_path, 'rb') as f:
        while True:
            buf = f.read()
            if not buf:
                break
            audio_in_byte += buf

    return audio_in_byte
