#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=utf-8

'''
 This script allows to integrate Latch in SSH Server with publickey authentication.
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
import syslog

sys.path.append('/usr/lib/latch/openssh/')

import latch
from latchHelper import *



def send_syslog_alert(msg): 
    syslog.openlog('syslog',syslog.LOG_PID, syslog.LOG_AUTH) 
    syslog.syslog('Latch ssh warning: Someone tried to access. ' + msg)
    syslog.closelog()



secret_key = getConfigParameter("secret_key");
app_id = getConfigParameter("app_id");

if app_id == None or secret_key == None:
    print("Can't read config file");
    exit();

user = os.getlogin();
accountId = getAccountId(user);
if accountId == None:
    sys.exit(0);

api = latch.Latch(app_id, secret_key)
latch.Latch.set_host(LATCH_HOST)

try:
    result = api.status(accountId); 
except:
    sys.exit(0)

if ('operations' in result.data) and (app_id in result.data['operations']) and ('status' in result.data['operations'][app_id]): 
    if result.data['operations'][app_id]['status'] == "off":
        send_syslog_alert('Latch locked.')
        sys.exit(1)
    if result.data['operations'][app_id]['status'] == "on":
        if 'two_factor' in result.data['operations'][app_id]:
            if sys.version_info < (3,0):
                input_token = raw_input("One-time code: ")
            else:
                input_token = input("One-time code: ")
            if 'token' in result.data['operations'][app_id]['two_factor']:
                if result.data['operations'][app_id]['two_factor']['token'] != input_token:
                    send_syslog_alert('Bad OTP.')
                    sys.exit(1)
sys.exit(0)
