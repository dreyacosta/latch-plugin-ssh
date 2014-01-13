'''
 This script allows to pair our ssh Server with Latch in some UNIX systems (like Linux)
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

#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# vim: set fileencoding=utf-8
# Run as root

import sys
import os
import urllib.request
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


if len(sys.argv) == 4 and sys.argv[2] == "-f":
    # read config file
    f = open(sys.argv[3],"r");
    lines = f.readlines();
    f.close();
    # write config file
    f = open("/etc/pam.d/latch.conf","w");
    f.writelines(lines);
    f.close();

elif len(sys.argv) != 2:
    print("use 'pair.py <TOKEN> [ -f <file.conf> ]'");
    exit();

secret_key = getConfigParameter("secret_key");
app_id = getConfigParameter("app_id");

if app_id == None or secret_key == None:
    print("Can't read config file");
    exit();

api = latch.Latch(app_id, secret_key);

latch.Latch.set_host("https://latch.elevenpaths.com")

user = os.getlogin();
if os.path.isfile("/etc/pam.d/latch_accounts"):
    # read latch_accounts file
    f = open("/etc/pam.d/latch_accounts","r")
    lines = f.readlines()
    f.close()
    # find user
    found = False 
    for line in lines:
        if line.find(user) != -1:
            found = True
            break
    if found:
        print("Paired");
        exit()

token = urllib.request.pathname2url(sys.argv[1]);
res = api.pair(token); 

responseData = res.get_data()
responseError = res.get_error()

if responseData != "":
    accountId = responseData["accountId"] 
    if os.path.isfile("/etc/pam.d/latch_accounts"):
        # add latch account
        f = open ("/etc/pam.d/latch_accounts", "a")
        f.write(user + ": " + accountId)
        f.close();
    else:
        # add latch account  
        fd = os.open ("/etc/pam.d/latch_accounts", os.O_WRONLY | os.O_CREAT, int("0600",8))
        f = os.fdopen(fd)
        f.write(user + ": " + accountId + "\n");
        f.close();    
    print("Paired");
elif responseError != "":
    print (responseError);
