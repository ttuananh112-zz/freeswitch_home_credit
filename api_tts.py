#!/usr/env/python
# -*- coding: utf-8 -*-

import requests
import urllib2
from os import listdir
import os
import time
import var


def check_remaining_character():
    url = var.URL_TTS_CHECK_REMAINING_KEY
    response = requests.get(url,
                            data="Hello world",
                            params={'api_key': var.API_KEY_TTS})
    r = response.json()
    error = r['error']
    remaining_free = r['remaining_free']
    return error, remaining_free


def speech_synthesis(text):
    success = False
    while not success:
        try:
            url = var.URL_TTS
            response = requests.post(url,
                                     data=text,
                                     headers={'api_key': var.API_KEY_TTS,
                                              'speed': var.SPEED,
                                              'voice': var.VOICE})
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
    for f in listdir(var.SOUNDS_DIR):
        if hash_code == f:
            return True
    return False


def download_audio(audio_url):
    success = False
    while not success:
        try:
            u = urllib2.urlopen(audio_url)
            file_name = get_hash_audio(audio_url) + var.EXTEND
            f = open(var.SOUNDS_DIR + file_name, 'w+')
            # os.chmod(audio_path+file_name, 0o777)
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
