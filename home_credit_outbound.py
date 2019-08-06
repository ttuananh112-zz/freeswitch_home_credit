#!/usr/bin/env python
# -*- coding: utf-8 -*-
import api_answer
import api_tts
import api_stt
import time
from pydub import AudioSegment
from freeswitch import *
import os

class Round:
    def __init__(self, session, sounds_dir, record_file, wait_file, name, *args):
        api_answer.request_bot_api(True, name, session.uuid, *args) # "gender", "anh", "name", "Tuan Anh"
        self.session = session
        self.sounds_dir = sounds_dir
        self.record_file = record_file
        self.wait_file = wait_file
        self.name = name
        self.exten = '.mp3'

    def one_round(self):
        while True:
            # Get answer from web hook
            answer = api_answer.get_answer(self.session.uuid)
            if answer != "":
                print "Answer: " + answer
                consoleLog("info", "ANSWER " + str(answer))
                # TTS
                is_success = False
                audio_file, is_downloaded = api_tts.get_audio(answer)
                consoleLog("info", "-----REQUEST SUCCESSFULLY-----")

                consoleLog("info", "AUDIO " + str(audio_file))
                # convert mp3 to wav
                #if not api_tts.is_audio_exist(audio_file):
                #    consoleLog("info", "AUDIO_DIR " + self.sounds_dir + str(audio_file) + '.mp3')
                #    os.system('mpg123 -w '+self.sounds_dir+audio_file+'.wav '+self.sounds_dir+audio_file+'.mp3')
                self.session.execute("playback", self.sounds_dir + str(audio_file) + self.exten)

                break

        if api_answer.check_end(answer):
            return True

        # RECORD
        consoleLog("info", "RECORDING")
        self.session.recordFile(self.sounds_dir + self.record_file, 5, 500, 3)
        
        consoleLog("info", "RECORDED")

        # STT
        status, req = api_stt.speech_recognition(self.sounds_dir + self.record_file)
        consoleLog("info", "request: " + str(req))
        api_answer.request_bot_api(False, self.name, self.session.uuid, req)
        return False


