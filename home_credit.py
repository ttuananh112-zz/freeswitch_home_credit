#!/usr/bin/python
# -*- coding: utf-8 -*-
#from freeswitch import *
from home_credit_outbound import *
import var


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
        name = "Tuấn Anh"
    r = Round(session, name, "gender", gender, "name", name)
    while True:
        if r.one_round():
            break
    session.hangup()
