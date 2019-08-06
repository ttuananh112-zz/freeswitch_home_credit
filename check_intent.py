#!/usr/env/python
from api_tts import *

def check_intent(intent):
    if intent == 'phuong_tien':
        f, is_downloaded = phuong_tien()
    elif intent == 'thiet_bi':
        f, is_downloaded = thiet_bi()
    elif intent == 'tieu_dung':
        f, is_downloaded = tieu_dung()
    elif intent == 'hoc_tap':
        f, is_downloaded = hoc_tap()
    elif intent == 'chua_benh':
        f, is_downloaded = chua_benh()
    elif intent == 'du_lich':
        f, is_downloaded = du_lich()
    elif intent == 'hieu_hi':
        f, is_downloaded = hieu_hi()
    elif intent == 'the_thao':
        f, is_downloaded = the_thao()
    elif intent == 'sua_nha':
        f, is_downloaded = sua_nha()
    else:
        f = 'none'
        is_downloaded = False
    return f, is_downloaded

