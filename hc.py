#!/usr/bin/python
# -*- coding: utf-8 -*-

from freeswitch import *

import time
import os
import hashlib
import requests


"""TTS"""
folder_path = '/usr/local/freeswitch/sounds'
ext = 'mp3'
tts_url = 'http://api.openfpt.vn/text2speech/v5'
tts_api_key = 'c5c86079c4ef4635a0449c7e7f7cc2f7'
file_error = '%s/%s' % (folder_path, 'acvlccxa.wav')

"""STT"""
folder_record_path = '/usr/local/freeswitch/recordings'
stt_url = 'https://api.openfpt.vn/fsr'
stt_api_key = 'c5c86079c4ef4635a0449c7e7f7cc2f7'

"""Predict Intent"""
predict_intent_url = 'https://v3-api.fpt.ai/api/v3/predict/intent'
"""Home Credit"""
hc_token = '720052620754ec80808f6f86510358fb'

voice = 'banmai'
speed = '0'
file_wait = '/usr/local/freeswitch/sounds/acvlccxa.wav'
file_beep = '/usr/local/freeswitch/sounds/beep.mp3'
folder_file_record_call = '/tmp'


def fpt_tts(text, voice='banmai', speed='0'):
    """
    :param voice:
    :param speed:
    :param text:
    :return:
    """
    md5 = hashlib.md5()
    md5.update('%s.%s.%s' % (voice, speed, text))
    file_name = md5.hexdigest()
    file_path = '%s/%s.%s' % (folder_path, file_name, ext)
    if os.path.isfile(file_path):
        consoleLog('info', 'TTS file %s existed' % file_path)
    else:
        consoleLog('info', 'TTS file %s not existed' % file_path)
        headers = {
            'api_key': tts_api_key,
            'speed': speed,
            'voice': voice,
        }
        try:
            r = requests.post(url=tts_url, data=text, headers=headers)
            resp = r.json()
            consoleLog('info', 'TTS Response: %s' % resp)
            if resp['error'] == 0:
                time.sleep(2)
                doc = requests.get(resp['async'])
                with open(file_path, 'wb') as f:
                    f.write(doc.content)
            else:
                return file_error
        except Exception as e:
            consoleLog('info', 'TTS Error: %s' % e)
            return file_error

    return file_path


def fpt_stt(file_path):
    """
    :param file_path:
    :return:
    """
    utterance = ''
    if os.path.isfile(file_path):
        consoleLog('info', 'STT file %s existed' % file_path)
        headers = {
            'api_key': stt_api_key,
        }
        try:
            with open(file_path, 'rb') as fh:
                my_data = fh.read()
                r = requests.put(stt_url, data=my_data, headers=headers)
                resp = r.json()
                consoleLog('info', 'STT Response: %s' % resp)
                if resp['status'] == 0:
                    utterance = resp['hypotheses'][0]['utterance']
        except Exception as e:
            consoleLog('info', 'STT Error: %s' % e)
    else:
        consoleLog('info', 'STT file %s not existed' % file_path)

    return utterance
    

def fpt_dialog_hc(content):
    """
    :param content:
    :return:
    """
    #content = str(content).replace('\n', '').replace('\r', '').strip()
    #consoleLog('info', 'Utterance: %s' % content)
    intent = ''
    headers = {
        'Authorization': 'Bearer %s' % hc_token,
    }
    data = {
        'content': content
    }
    try:        
        r = requests.post(url=predict_intent_url, json=data, headers=headers)        
        resp = r.json()        
        if resp['status']['code'] == 200:            
            intent = resp[u'data'][u'intents'][0]['label']            
    except Exception as e:
        pass

    return intent

def handler(session, args):
    session.answer()
    if session.ready() == True:
        call_id = session.get_uuid()
        consoleLog('info', 'Call ID: %s' % call_id)
        session.streamFile(fpt_tts(text='Chào mừng quý khách đã gọi đến Home Credit Việt Nam.', voice=voice, speed=speed))
        session.sleep(1000)
        session.streamFile(fpt_tts(voice=voice, speed=speed, text='Em thấy mình đã nhận tiền vay. Cho em hỏi mình đã, hoặc dự định, sử dụng khoản tiền này, cho mục đích nào ạ?'))
        #p = fpt_tts(voice=voice, speed=speed, text='Em thấy mình đã nhận tiền vay. Cho em hỏi mình đã, hoặc dự định, sử dụng khoản tiền này, cho mục đích nào ạ?')
        #session.execute("play_and_detect_speech","%s detect:unimrcp:java-mrcp-v2 {define-grammar=false,recognition-timeout=1000,start-input-timers=true,no-input-timeout=15000}builtin:mrcpv2" % p)
        file_record = '%s/%s.mp3' % (folder_file_record_call, call_id)
        consoleLog('info', 'File record path: %s' % file_record)
        session.streamFile(file_beep)
        session.recordFile(file_record, 5, 500, 5);
        session.streamFile(file_wait)
        #utterance = session.getVariable('detect_speech_result')
        #utterance = utterance.decode('base64')
        utterance = fpt_stt(file_record)
        repeat = 0
        while utterance == '' and repeat < 1:
            consoleLog('info', 'Not Recognition')
            repeat = repeat + 1
            session.streamFile(fpt_tts(voice=voice, speed=speed, text='Dạ vừa rồi em chưa nghe rõ, phiền anh chị nói lại ạ.'))
            #p = fpt_tts(voice=voice, speed=speed, text='Dạ vừa rồi em chưa nghe rõ, phiền anh chị nói lại ạ.')
            #session.execute("play_and_detect_speech","%s detect:unimrcp:java-mrcp-v2 {define-grammar=false,recognition-timeout=1000,start-input-timers=true,no-input-timeout=10000}builtin:mrcpv2" %p)
            session.streamFile(file_beep)
            session.recordFile(file_record, 5, 500, 5);
            session.streamFile(file_wait)
            utterance = fpt_stt(file_record)
            #utterance = session.getVariable('detect_speech_result')
            #utterance = utterance.decode('base64')
        if utterance != '':            
            intent = fpt_dialog_hc(utterance)
            if intent == 'phuong_tien':
                session.streamFile(fpt_tts(text='Em đã nhận được thông tin là tiền vay được dùng để mua phương tiện đi lại.', voice=voice, speed=speed))
            if intent == 'thiet_bi':
                session.streamFile(fpt_tts(text='Em đã nhận được thông tin là tiền vay được dùng để mua trang thiết bị gia đình.', voice=voice, speed=speed))
            if intent == 'tieu_dung':
                session.streamFile(fpt_tts(text='Em đã nhận được thông tin là tiền vay được dùng để mua hàng tiêu dùng.', voice=voice, speed=speed))
            if intent == 'hoc_tap':
                session.streamFile(fpt_tts(text='Em đã nhận được thông tin là tiền vay được dùng để dành cho chi phí học tập.', voice=voice, speed=speed))
            if intent == 'chua_benh':
                session.streamFile(fpt_tts(text='Em đã nhận được thông tin là tiền vay được dùng để dành cho chi phí chữa bệnh.', voice=voice, speed=speed))
            if intent == 'du_lich':
                session.streamFile(fpt_tts(text='Em đã nhận được thông tin là tiền vay được dùng để dành cho du lịch.', voice=voice, speed=speed))
            if intent == 'hieu_hi':
                session.streamFile(fpt_tts(text='Em đã nhận được thông tin là tiền vay được dùng để dành cho việc hiếu hỉ.', voice=voice, speed=speed))
            if intent == 'the_thao':
                session.streamFile(fpt_tts(text='Em đã nhận được thông tin là tiền vay được dùng để dành cho chi phí thể thao.', voice=voice, speed=speed))
            if intent == 'sua_nha':
                session.streamFile(fpt_tts(text='Em đã nhận được thông tin là tiền vay được dùng để dành cho việc sửa nhà.', voice=voice, speed=speed))
        session.sleep(1000)
        session.streamFile(fpt_tts(text='Cám ơn anh chị đã dành thời gian nghe điện thoại và tin tưởng lựa chọn Home Credit làm bạn đồng hành. Em chào anh chị!', voice=voice, speed=speed))
        session.sleep(1000)
    	session.hangup()
