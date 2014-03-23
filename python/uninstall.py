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


if os.path.isfile(SSHD_PAM_CONFIG_FILE):
    # read PAM config file
    f = open(SSHD_PAM_CONFIG_FILE,"r");
    lines = f.readlines();
    f.close();

    shutil.copy(SSHD_PAM_CONFIG_FILE, SSHD_PAM_CONFIG_FILE + "~")

    # delete latch PAM 
    f = open(SSHD_PAM_CONFIG_FILE,"w");
    for line in lines:
        if equalSplit(line, AUTH_INCLUDE_PASSWD_AUTH_SSHD):
            # centos version
            f.write(AUTH_INCLUDE_PASSWORD_AUTH + "\n")
        elif not equalSplit(line, AUTH_REQUIRED_LATCH_PAM):
            # ubuntu version
            f.write(line)
    f.close()
else:
    print("Can't open sshd pam config file")


if os.path.isfile(SSHD_CONFIG):
    # read sshd_config file
    f = open(SSHD_CONFIG,"r")
    lines = f.readlines()
    f.close()

    shutil.copy(SSHD_CONFIG, SSHD_CONFIG + "~")

    # delete latch
    f = open(SSHD_CONFIG,"w")
    for line in lines:
        if "ChallengeResponseAuthentication" in line and "#" not in line:
            f.write("ChallengeResponseAuthentication no\n")
        elif "PasswordAuthentication" in line and "#" not in line:
            f.write("PasswordAuthentication yes\n")
        elif not equalSplit(line, "ForceCommand " + WRAPPER_EXE):
            f.write(line);
    f.close();
else:
    print("Can't open sshd_config file")

# uninstall files
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
if os.path.isfile(PASSWORD_AUTH_SSHD_PAM_CONFIG_FILE):
    os.remove(PASSWORD_AUTH_SSHD_PAM_CONFIG_FILE)
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
