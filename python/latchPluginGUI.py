#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=utf-8
# run as root

'''
 This plugin allows to pair and upair our application with Latch in some UNIX systems (like Linux)
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
import latch

from latchHelper import *
from translation import *



def pair_gui():

    secret_key = getConfigParameter("secret_key")
    app_id = getConfigParameter("app_id")

    if app_id == None or secret_key == None:
        print(CANT_READ_CONFIG_FILE_MSG)
        exit();

    api = latch.Latch(app_id, secret_key)
    latch.Latch.set_host(LATCH_HOST)

    reply = eg.enterbox(msg=INSERT_PAIRING_CODE_MSG, title=PAIR_TITLE, default='', strip=True, image=None, root=None);
    if reply == None:
        exit()

    if reply == "":
        eg.msgbox(msg=EMPTY_PAIRING_CODE_MSG,title=ERROR_TITLE)
        return

    if len(reply) != 6:
        eg.msgbox(msg=BAD_PAIRING_CODE_LENGTH_MSG,title=ERROR_TITLE)
        return

    token = reply
    try:
        res = api.pair(token)
    except:
        eg.msgbox(msg=SOME_EXCEPTION_MSG,title=ERROR_TITLE)
        return

    responseData = res.get_data();
    responseError = res.get_error();

    if 'accountId' in responseData:
        user = os.getlogin()
        accountId = responseData["accountId"]
        addAccount(user, accountId)
        eg.msgbox(msg=PAIRED_SUCCESSFULLY_MSG,title=PAIR_TITLE);
    elif responseError != "":
        if responseError.get_message() == 'Invalid application signature':
            eg.msgbox(msg=INVALID_APP_SIGN_MSG,title=ERROR_TITLE)
        else:
            eg.msgbox(msg=responseError.get_message(),title=ERROR_TITLE)
        

def unpair_gui():

    secret_key = getConfigParameter("secret_key");
    app_id = getConfigParameter("app_id");

    if app_id == None or secret_key == None:
        print(CANT_READ_CONFIG_FILE_MSG);
        exit();

    api = latch.Latch(app_id, secret_key);
    latch.Latch.set_host(LATCH_HOST)
    
    user = os.getlogin()
    accountId = getAccountId(user)
    if accountId == None:
        eg.msgbox(msg=CANT_READ_ACCOUNTS_FILE_MSG,title=ERROR_TITLE)
        return;

    try:
        res = api.unpair(accountId)
    except:
        eg.msgbox(msg=SOME_EXCEPTION_MSG,title=ERROR_TITLE)
        return

    responseError = res.get_error()

    if responseError != "" and responseError.get_message() != 'Account not paired':
        if responseError.get_message() == 'Invalid application signature':
            eg.msgbox(msg=INVALID_APP_SIGN_MSG,title=ERROR_TITLE)
        else:
            eg.msgbox(msg=responseError.get_message(),title=ERROR_TITLE)
    else:
        deleteAccount(accountId)
        eg.msgbox(msg=UNPAIRED_SUCCESSFULLY_MSG,title=UNPAIR_TITLE)




operations = [PAIR_TITLE,UNPAIR_TITLE,EXIT_TITLE]
user = os.getlogin()

while 1:
    if isPair(user):
        operations = [UNPAIR_TITLE,EXIT_TITLE]
        message = UNPAIR_MSG
    else:
        operations = [PAIR_TITLE,EXIT_TITLE]
        message = PAIR_MSG

    reply = eg.buttonbox(msg=message, title=PLUGIN_NAME,image=None, choices=operations)

    if reply == PAIR_TITLE:
        pair_gui()
    elif reply == UNPAIR_TITLE:
        unpair_gui()
    elif reply == EXIT_TITLE:
        exit();

