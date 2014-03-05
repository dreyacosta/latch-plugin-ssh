#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=utf-8
# Run as root

'''
 This script allows to uninstall latch plugin from openvpn Server in some UNIX systems (like Linux)
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


import os
import shutil

from latchHelper import *


# read sshd_config file
f = open(SSHD_CONFIG,"r");
lines = f.readlines();
f.close();
# delete latch
f = open(SSHD_CONFIG,"w");
for line in lines:
    if line.find("ForceCommand " + WRAPPER_EXE) == -1 :
        f.write(line);
f.close();

if os.path.isfile(LATCH_ACCOUNTS):
    os.remove(LATCH_ACCOUNTS)
if os.path.isfile(LATCH_CONFIG):
    os.remove(LATCH_CONFIG)
if os.path.isfile(WRAPPER_SH):
    os.remove(WRAPPER_SH)
if os.path.isfile(WRAPPER_PY):
    os.remove(WRAPPER_PY)
if os.path.isfile(WRAPPER_EXE):
    os.remove(WRAPPER_EXE)
if os.path.isdir(LATCH_OPENSSH_PATH):
    shutil.rmtree(LATCH_OPENSSH_PATH)
if os.path.isfile(PAIR_BIN):
    os.remove(PAIR_BIN)
if os.path.isfile(UNPAIR_BIN):
    os.remove(UNPAIR_BIN)
if os.path.isfile(PLUGIN_BIN):
    os.remove(PLUGIN_BIN)
if os.path.isfile(SETTINGS_BIN):
    os.remove(SETTINGS_BIN)

print("Uninstall completed")
