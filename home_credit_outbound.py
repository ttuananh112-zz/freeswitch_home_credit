#!/usr/bin/env python
# -*- coding: utf-8 -*-
import api_answer
import api_tts
import api_stt
import var
from freeswitch import *
import os

class Round:
    def __init__(self, session, name, *args):
        api_answer.request_bot_api(True, name, session.uuid, *args) # "gender", "anh", "name", "Tuan Anh"
        self.session = session
        self.name = name

    def one_round(self):
        while True:
            # Get answer from web hook
            answer = api_answer.get_answer(self.session.uuid)
            if answer != "":
                print("Answer: " + answer)
                consoleLog("info", "ANSWER " + str(answer))
                # TTS
                is_success = False
                audio_file, is_downloaded = api_tts.get_audio(answer)
                consoleLog("info", "-----REQUEST SUCCESSFULLY-----")

                consoleLog("info", "AUDIO " + str(audio_file))
                self.session.execute("playback", var.SOUNDS_DIR + str(audio_file) + var.EXTEND)
                break

        if api_answer.check_end(answer):
            return True

        # RECORD
        consoleLog("info", "RECORDING")
        self.session.recordFile(var.RECORD_DIR + self.session.uuid + var.EXTEND, 5, 500, 3)
        
        consoleLog("info", "RECORDED")

        # STT
        status, req = api_stt.speech_recognition(var.RECORD_DIR + self.session.uuid + var.EXTEND)
        consoleLog("info", "request: " + str(req))
        api_answer.request_bot_api(False, self.name, self.session.uuid, req)
        return False


