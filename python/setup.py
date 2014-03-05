#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=utf-8
# Run as root

'''
 This script allows to install latch plugin in ssh Server in some UNIX systems (like Linux)
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
import shutil

from latchHelper import *



if len(sys.argv) == 3 and sys.argv[1] == "-f":
    secret_key = getConfigParameter("secret_key", sys.argv[2])
    app_id = getConfigParameter("app_id", sys.argv[2])
    if app_id == None or secret_key == None:
        print("Can't read config file");
        exit(1)

    replaceConfigParameters(app_id, secret_key)
else:
    print("use 'setup.py -f <file.conf>'");
    exit(1);

# read sshd_config file
f = open(SSHD_CONFIG,"r")
lines = f.readlines()
f.close()
# find latch
found = False
for line in lines:
    if line.find("ForceCommand " + WRAPPER_EXE) != -1 :
        found = True
        break
if not found:
    # add latch to ssh configuration
    f = open(SSHD_CONFIG,"a")
    f.write("ForceCommand " + WRAPPER_EXE)
    f.close()

# install the two wrappers, sshd.sh and sshd.py in /usr/sbin
if not os.path.isfile(WRAPPER_SH):
    os.open (WRAPPER_SH, os.O_CREAT, int("0554",8))
    shutil.copyfile('sshd.sh', WRAPPER_SH)
if not os.path.isfile(WRAPPER_PY):
    os.open (WRAPPER_PY, os.O_CREAT, int("0500",8))
    shutil.copyfile('sshd.py', WRAPPER_PY)

# install latch in /usr/lib/openssh
if not os.path.isdir(LATCH_PATH):
    os.mkdir(LATCH_PATH)
if not os.path.isdir(LATCH_OPENSSH_PATH):
    os.mkdir(LATCH_OPENSSH_PATH)
if not os.path.isfile(LATCH_PLUGIN_GUI):
    os.open (LATCH_PLUGIN_GUI, os.O_CREAT, int("0100",8))
    shutil.copyfile('latchPluginGUI.py', LATCH_PLUGIN_GUI)
if not os.path.isfile(SETTINGS_PLUGIN_GUI):
    os.open (SETTINGS_PLUGIN_GUI, os.O_CREAT, int("0100",8))
    shutil.copyfile('settingsGUI.py', SETTINGS_PLUGIN_GUI)
if not os.path.isfile(PAIR_PLUGIN):
    os.open (PAIR_PLUGIN, os.O_CREAT, int("0100",8))
    shutil.copyfile('pair.py', PAIR_PLUGIN)
if not os.path.isfile(UNPAIR_PLUGIN):
    os.open (UNPAIR_PLUGIN, os.O_CREAT, int("0100",8))
    shutil.copyfile('unpair.py', UNPAIR_PLUGIN)
if not os.path.isfile(SETTINGS_PLUGIN):
    os.open (SETTINGS_PLUGIN, os.O_CREAT, int("0100",8))
    shutil.copyfile('settings.py', SETTINGS_PLUGIN)
if not os.path.isfile(LATCH_HELPER_PLUGIN):
    os.open (LATCH_HELPER_PLUGIN, os.O_CREAT, int("0400",8))
    shutil.copyfile('latchHelper.py', LATCH_HELPER_PLUGIN)
if not os.path.isfile(LATCH_API):
    os.open (LATCH_API, os.O_CREAT, int("0400",8))
    shutil.copyfile('latch.py', LATCH_API)

# add latch_accounts file
if not os.path.isfile(LATCH_ACCOUNTS):   
    fd = os.open (LATCH_ACCOUNTS, os.O_CREAT, int("0600",8))

print("latch plugin installing...")
exit(0)