#!/usr/bin/python
# -*- coding: utf-8 -*-
#from freeswitch import *
from home_credit_outbound import *
import time

sounds_dir = '/home/user/sounds_homecredit/'
record_file = 'record.mp3'
#welcome_file = '0a0c59afbe28ec0097f76fb00d28fa54.wav'
wait_file = 'dc1f60dc8f233e6e4ef9cd246a65f3b7.wav'
#goodbye_file = '88280e87c24da1d4183e4cbf500f0ca3.wav'


def handler(session, args):
    session.answer()
    #session.getDigits(10, "#", 5000)
    callerid = session.getVariable("callerid")
    consoleLog("info", "CALLER ID NUMBER " + str(callerid))
    gender = session.getVariable("gender")
    name = session.getVariable("name")
    #consoleLog("info", gender + " " + name)
    #digit = session.getDigits(1, "#", 5000)
    session.execute("sleep", "1000") 
    
    if gender == None and name == None:
        gender = "anh"
        name = "Hà"
    r = Round(session, sounds_dir, record_file, wait_file, name, "gender", gender, "name", name)
    while True:
        if r.one_round():
            break
    session.hangup()
