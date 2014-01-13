'''
 This script allows to unpair our ssh Server in some UNIX systems (like Linux)
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

def getAccountId(user, lines):

    for line in lines:
        if line.find(user) != -1:
            words = line.split();
            if len(words) == 2:
                return words[1];
            break; 
    return None;


if len(sys.argv) == 3 and sys.argv[1] == "-f":
    # read config file
    f = open(sys.argv[2],"r");
    lines = f.readlines();
    f.close();
    # write config file
    f = open("/etc/pam.d/latch.conf","w");
    f.writelines(lines);
    f.close();
elif len(sys.argv) != 1:
    print("use 'unpair.py [ -f <file.conf> ]'");
    exit();

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
    print("User not paired");
    exit();

api = latch.Latch(app_id, secret_key);

latch.Latch.set_host("https://latch.elevenpaths.com");

accountIdUrl = urllib.request.pathname2url(accountId);
res = api.unpair(accountIdUrl); 

responseError = res.get_error();

if responseError != "":
    print (responseError);
else:
    # delete latch account
    f = open("/etc/pam.d/latch_accounts","w");
    for line in lines:
        if line.find(accountId) == -1 :
            f.write(line);
    f.close();

    print("Unpaired");
