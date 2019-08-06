#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json


record_path = '/home/user/sounds_homecredit/'
record_file = '0a0c59afbe28ec0097f76fb00d28fa54.wav'
API_KEY = "Vmskg4YjulqM9ZffofBXvRTGVqrFIDZh"
API_TOKEN_BOT = "720052620754ec80808f6f86510358fb"

def speech_recognition(file_path):
    success = False
    while not success:
        try:

            audio = audio_to_byte(file_path)

            url = "https://api.fpt.ai/hmi/asr/general"
            response = requests.post(url,
                    data= audio,
                    headers={'api_key':API_KEY,
                        'Content-Type': ''})
            r = response.json()
            status = r['status']
            text = ''
            #print(json.dumps(r))
            if status == 0:
                text = r['hypotheses'][0]['utterance']
            success = True
        except:
            print("FAILED")
    return status, text.encode('utf-8')

def audio_to_byte(file_path):

    #file_path =  record_path + record_file
    audio_in_byte = ''
    #max_size = 1024    
    with open(file_path, 'rb') as f:
        while True:
            buf = f.read()
            if not buf:
                break
            audio_in_byte += buf

    return audio_in_byte

def get_intent(text):
    url = "https://v3-api.fpt.ai/api/v3/predict/intent"
    d = {}
    d['content'] = text
    #d['save_history'] = 'false'
    json_data = json.dumps(d)
    #print(json_data)
    
    response = requests.post(url,
            headers={'Authorization': API_TOKEN_BOT},
            data=json_data)
    r = response.json()
    #print(json.dumps(r))
    status = r['status']['code']
    intent = ''
    if status == 200:
        intent = r['data']['intents'][0]['label']
    return status, intent

#status, text = speech_recognition(record_path + record_file)
#print(status)
#print(text)
#print(type(text))
#print(type(text.encode('utf-8')))
#status, intent = get_intent(text)
#print(intent)


