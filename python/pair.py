#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=utf-8
# Run as root

'''
 This script allows to pair our application with Latch in some UNIX systems (like Linux)
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


import sys
import os
import latch

from latchHelper import *
from translation import *


if len(sys.argv) == 4 and sys.argv[2] == "-f":
    secret_key = getConfigParameter("secret_key", sys.argv[3])
    app_id = getConfigParameter("app_id", sys.argv[3])
    if app_id == None or secret_key == None:
        print(CANT_READ_CONFIG_FILE_MSG);
        exit()

    replaceConfigParameters(app_id, secret_key)

elif len(sys.argv) != 2:
    print(INCORRECT_PAIR_USE_MSG);
    exit();

secret_key = getConfigParameter("secret_key");
app_id = getConfigParameter("app_id");

if app_id == None or secret_key == None:
    print(CANT_READ_CONFIG_FILE_MSG);
    exit()

user = os.getlogin()
if isPair(user):
    print(PAIRED_USER_MSG_PART_1 + user + PAIRED_USER_MSG_PART_2)
    exit()

api = latch.Latch(app_id, secret_key)
latch.Latch.set_host(LATCH_HOST)

reply = sys.argv[1]

if len(reply) != 6:
    print(BAD_PAIRING_CODE_LENGTH_MSG)
    exit()

token = reply;
try:
    res = api.pair(token)
except:
    print(SOME_EXCEPTION_MSG)
    exit()

responseData = res.get_data()
responseError = res.get_error()

if 'accountId' in responseData:
    accountId = responseData["accountId"]
    addAccount(user, accountId)
    print(PAIRED_SUCCESSFULLY_MSG);
elif responseError != "":
    if responseError.get_message() == 'Invalid application signature':
        print(INVALID_APP_SIGN_MSG)
    else:
        print(responseError.get_message())
