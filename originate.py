#!/usr/bin/python
# -*- coding: utf-8 -*-
from freeswitchESL import ESL
from optparse import OptionParser

con = ESL.ESLconnection("127.0.0.1", "8021", "ClueCon")
parser = OptionParser()
parser.add_option('-g', '--gender', dest='gender', default='anh')
parser.add_option('-n', '--name', dest='name', default='Minh')
parser.add_option('-c', '--callee', dest='callee', default='1002')
parser.add_option('-e', '--extension', dest='extension', default='110')
(options, args) = parser.parse_args()

if con.connected():
    print("connected")
    if options.callee != "" and options.extension != "":
        if options.name != "" and options.gender != "":
            res = con.bgapi("originate", "{gender="+options.gender+",name="+options.name+
                            "}user/"+options.callee+" "+options.extension)
            print("called")




