#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# vim: set fileencoding=utf-8
# run as root

'''
 This plugin allows to config latch settings in some UNIX systems (like Linux)
 Copyright (C) 2013 Eleven Paths

 This library is free software; you can redistribute it and/or
 modify it under the terms of the GNU Lesser General Public
 License as published by the Free Software Foundation; either
 version 2.1 of the License, or (at your option) any later version.
 
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 Lesser General Public License for more details.
 
 You should have received a copy of the GNU Lesser General Public
 License along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
'''


import easygui as eg
import sys
import os
import urllib.request

sys.path.append('/etc/ssh/latch/')
import latch


def getConfigParameter(name):

    # read latch config file
    f = open("/etc/pam.d/latch.conf","r");
    lines = f.readlines();
    f.close();

    # find parameter
    for line in lines:
        if line.find(name) != -1:
            break;

    words = line.split();   
    if len(words) == 3:
        return words[2];
    return None;


   
secret_key = getConfigParameter("secret_key");
app_id = getConfigParameter("app_id");

if app_id == None or secret_key == None:
    print("Can't read config file");
    exit();

msg = "Identify your application"
title = "Settings"
fieldNames = ["Application ID","Secret key"]
fieldValues = [app_id, secret_key]  # we start with blanks for the values
fieldValues = eg.multenterbox(msg,title, fieldNames, fieldValues)
 
# make sure that none of the fields was left blank
while 1:
    if fieldValues == None: break
    errmsg = ""
    for i in range(len(fieldNames)):
        if fieldValues[i].strip() == "":
            errmsg += ('"%s" is a required field.\n\n' % fieldNames[i])
    if errmsg == "":
        # write config file
        fd = os.open ("/etc/pam.d/latch.conf", os.O_WRONLY | os.O_CREAT, int("0600",8))
        f = os.fdopen(fd,"w")
        f.write("#\n")
        f.write("# Configuration file for the latch PAM module\n")
        f.write("#\n")
        f.write("\n")
        f.write("# Identify your Application\n")
        f.write("# Secret key value\n")
        f.write("#\n")
        f.write("app_id = " + fieldValues[0] + "\n")
        f.write("\n")
        f.write("# Application ID value\n")
        f.write("#\n")
        f.write("secret_key = " + fieldValues[1] + "\n")
        f.close()
        secret_key = fieldValues[1]
        app_id = fieldValues[0]
        break # no problems found
    fieldValues = eg.multenterbox(errmsg, title, fieldNames, fieldValues)




