#!/usr/env/python
# -*- coding: utf-8 -*-

import requests
import urllib2
from os import listdir
import os
import time

API_KEY = "Vmskg4YjulqM9ZffofBXvRTGVqrFIDZh"
audio_path = '/home/user/sounds_homecredit/'
speed = '0'
voice = 'banmai'

def check_remaining_character(api_key):
    url = 'https://dev.openfpt.vn/balance/tts'
    response = requests.get(url,
        data="Hello world",
        params={'api_key':api_key})
    r = response.json()
    error = r['error']
    remaining_free = r['remaining_free']
    return error, remaining_free

def speech_synthesis(api_key, text):
    success = False
    while not success:
        try:

            url = "https://api.fpt.ai/hmi/tts/v5"
            response = requests.post(url,
                    data= text,
                    headers={'api_key':API_KEY,
                        'speed': speed,
                	'voice': voice})
            r = response.json()
            error = r['error']
            message = r['message']
            audio = r['async']
            success = True
        except:
            print("FAILED")
    return error, message, audio

def get_hash_audio(audio):
    hash_code = audio.split('.')[4]
    return hash_code

def is_audio_exist(hash_code):
    for f in listdir(audio_path):
        if hash_code+'.wav' == f:
            return True
    return False

def download_audio(audio_url):
    success = False
    while not success:
        try:

            u = urllib2.urlopen(audio_url)
            file_name = get_hash_audio(audio_url) + '.mp3'
            f = open(audio_path+file_name, 'w+')
            #os.chmod(audio_path+file_name, 0o777)
            meta = u.info()
            file_size = int(meta.getheaders("Content-Length")[0])

            file_size_dl = 0
            block_sz = 8192
            is_downloaded = False
            while True:
                buff = u.read(block_sz)
                if not buff:
                    break

                file_size_dl += len(buff)
                f.write(buff)
                status = file_size_dl * 100. / file_size
        
                if status == 100.:
                    is_downloaded = True
        

            f.close()
            success = True
        except:
             print("FAILED")
    return is_downloaded
    
#print check_remaining_character(API_KEY)

def get_audio(text):
    _,_,audio_url = speech_synthesis(API_KEY, text)
    time.sleep(0.5)
    hash_code = get_hash_audio(audio_url)
    done_downloaded = False
    if not is_audio_exist(hash_code):
        done_downloaded = download_audio(audio_url)
    return str(hash_code), done_downloaded

def welcome():
    text = 'Em thấy mình đã nhận tiền vay, cho em hỏi mình đã hoặc dự định sử dụng khoản tiền này cho mục đích nào ạ?'
    audio_file, is_downloaded = get_audio(text)
    return audio_file, is_downloaded

def wait():
    text = 'Anh chị vui lòng chờ chút xíu ạ.'
    audio_file, is_downloaded = get_audio(text)
    return audio_file, is_downloaded

def phuong_tien():
    text = 'Em đã nhận được thông tin là tiền vay được dùng để mua phương tiện đi lại.'
    audio_file, is_downloaded = get_audio(text)
    return audio_file, is_downloaded

def thiet_bi():
    text = 'Em đã nhận được thông tin là tiền vay được dùng để mua trang thiết bị gia đình.'
    audio_file, is_downloaded = get_audio(text)
    return audio_file, is_downloaded

def tieu_dung():
    text = 'Em đã nhận được thông tin là tiền vay được dùng để mua hàng tiêu dùng.'
    audio_file, is_downloaded = get_audio(text)
    return audio_file, is_downloaded

def hoc_tap():
    text = 'Em đã nhận được thông tin là tiền vay được dùng để dành cho chi phí học tập.'
    audio_file, is_downloaded = get_audio(text)
    return audio_file, is_downloaded

def chua_benh():
    text = 'Em đã nhận được thông tin là tiền vay được dùng để dành cho chi phí chữa bệnh.'
    audio_file, is_downloaded = get_audio(text)
    return audio_file, is_downloaded

def du_lich():
    text = 'Em đã nhận được thông tin là tiền vay được dùng để dành cho du lịch.'
    audio_file, is_downloaded = get_audio(text)
    return audio_file, is_downloaded

def hieu_hi():
    text = 'Em đã nhận được thông tin là tiền vay được dùng để dành cho việc hiếu hỉ.'
    audio_file, is_downloaded = get_audio(text)
    return audio_file, is_downloaded

def the_thao():
    text = 'Em đã nhận được thông tin là tiền vay được dùng để dành cho chi phí thể thao.'
    audio_file, is_downloaded = get_audio(text)
    return audio_file, is_downloaded

def sua_nha():
    text = 'Em đã nhận được thông tin là tiền vay được dùng để dành cho việc sửa nhà.'
    audio_file, is_downloaded = get_audio(text)
    return audio_file, is_downloaded

def goodbye():
    text = 'Cám ơn anh chị đã dành thời gian nghe điện thoại và tin tưởng lựa chọn Home Credit làm bạn đồng hành. Em chào anh chị!'
    audio_file, is_downloaded = get_audio(text)
    return audio_file, is_downloaded


