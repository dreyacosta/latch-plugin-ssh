#!/usr/bin/env python3
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


import urllib.request
import sys
import os

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

def getAccountId(user, lines):

    for line in lines:
        if line.find(user) != -1:
            words = line.split();
            if len(words) == 2:
                return words[1];
            break; 
    return None;


secret_key = getConfigParameter("secret_key");
app_id = getConfigParameter("app_id");

if app_id == None or secret_key == None:
    print("Can't read config file");
    exit();

# read latch_accounts file
f = open("/etc/pam.d/latch_accounts","r");
lines = f.readlines();
f.close();

user = os.getlogin();
accountId = getAccountId(user, lines);
if accountId == None:
    sys.exit(0);

api = latch.Latch(app_id, secret_key)
latch.Latch.set_host("https://latch.elevenpaths.com")

accountIdUrl = urllib.request.pathname2url(accountId)
try:
    result = api.status(accountIdUrl); 
except:
    sys.exit(0)

if ('operations' in result.data) and (app_id in result.data['operations']) and ('status' in result.data['operations'][app_id]): 
    if result.data['operations'][app_id]['status'] == "off":
        sys.exit(1)
    if result.data['operations'][app_id]['status'] == "on":
        if 'two_factor' in result.data['operations'][app_id]:
            input_token = input("One-time code: ")
            if 'token' in result.data['operations'][app_id]['two_factor']:
                if result.data['operations'][app_id]['two_factor']['token'] != input_token:
                    sys.exit(1)
sys.exit(0)
