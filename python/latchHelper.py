'''
 This script helps to integrate latch into system
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


PLUGIN_NAME = "SSH - latch"

LATCH_PATH = "/usr/lib/latch/"
LATCH_OPENSSH_PATH = LATCH_PATH + "openssh/"
# LATCH_CONFIG_PATH = "/etc/latch/"

LATCH_ACCOUNTS = LATCH_OPENSSH_PATH + ".latch_accounts"
LATCH_CONFIG =  "/etc/ssh-latch.conf"
LATCH_HOST = "https://latch.elevenpaths.com"

SSHD_PAM_CONFIG_FILE = "/etc/pam.d/sshd"
PASSWORD_AUTH_PAM_CONFIG_FILE = "/etc/pam.d/password-auth"
PASSWORD_AUTH_SSHD_PAM_CONFIG_FILE = "/etc/pam.d/passwd-auth-sshd"
LATCH_PAM_SO = "/lib/security/pam_latch.so"

AUTH_INCLUDE_PASSWORD_AUTH = "auth       include      password-auth"
AUTH_INCLUDE_PASSWD_AUTH_SSHD = "auth	   include	passwd-auth-sshd"
AUTH_SUFFICIENT_PAM_UNIX = "auth        sufficient     pam_unix.so nullok try_first_pass"
AUTH_REQUISITE_PAM_UNIX = "auth        requisite     pam_unix.so nullok try_first_pass"
AUTH_SUFFICIENT_LATCH_PAM = "auth        sufficient     " + LATCH_PAM_SO + "  accounts=" + LATCH_ACCOUNTS + "  config=" + LATCH_CONFIG + "  otp=yes"
AUTH_REQUIRED_LATCH_PAM = "auth       required     " + LATCH_PAM_SO + "  accounts=" + LATCH_ACCOUNTS + "  config=" + LATCH_CONFIG + "  otp=yes"
#auth       required     /lib/security/pam_latch.so  accounts=/usr/lib/latch/openssh/.latch_accounts  config=/etc/ssh-latch.conf  otp=yes

SSHD_CONFIG = "/etc/ssh/sshd_config"

WRAPPER_SH = "/usr/sbin/sshd.sh"
WRAPPER_PY = "/usr/sbin/sshd.py"
WRAPPER_EXE = "/usr/sbin/wp_sshd"


PAIR_BIN = "/usr/bin/pairSSH"
UNPAIR_BIN = "/usr/bin/unpairSSH"
PLUGIN_BIN = "/usr/bin/latchSSH"
SETTINGS_BIN = "/usr/sbin/config_latchSSH"

LATCH_PLUGIN_GUI = LATCH_OPENSSH_PATH + "latchPluginGUI.py"
SETTINGS_PLUGIN_GUI = LATCH_OPENSSH_PATH + "settingsGUI.py"
PAIR_PLUGIN = LATCH_OPENSSH_PATH + "pair.py"
UNPAIR_PLUGIN = LATCH_OPENSSH_PATH + "unpair.py"
SETTINGS_PLUGIN = LATCH_OPENSSH_PATH + "settings.py"
LATCH_HELPER_PLUGIN = LATCH_OPENSSH_PATH + "latchHelper.py"
TRANSLATION_PLUGIN = LATCH_OPENSSH_PATH + "translation.py"

LATCH_API = LATCH_OPENSSH_PATH + "latch.py"




def equalSplit(string1, string2):
    return string1.split() == string2.split()

def getConfigParameter(name, configFile=LATCH_CONFIG):
    # read latch config file
    try:
        f = open(configFile,"r")
    except IOError as e:
        return None

    lines = f.readlines()
    f.close()

    # find parameter
    for line in lines:
        if line.find(name) != -1:
            break;

    words = line.split()
    if len(words) == 3:
        return words[2]
    return None

def replaceConfigParameters(newAppId, newSecret):
    # write config file
    fd = os.open (LATCH_CONFIG, os.O_WRONLY | os.O_CREAT, int("0600",8))
    f = os.fdopen(fd,"w")
    f.write("#\n")
    f.write("# Configuration file for " + PLUGIN_NAME + "\n")
    f.write("#\n")
    f.write("\n")
    f.write("# Identify your Application\n")
    f.write("# Secret key value\n")
    f.write("#\n")
    f.write("app_id = " + newAppId + "\n")
    f.write("\n")
    f.write("# Application ID value\n")
    f.write("#\n")
    f.write("secret_key = " + newSecret + "\n")
    f.close()

def getAccountId(user):
    if os.path.isfile(LATCH_ACCOUNTS):
        # read latch_accounts file
        f = open(LATCH_ACCOUNTS,"r");
        lines = f.readlines();
        f.close();

        for line in lines:
            words = line.split();
            if words[0] == user + ':':
                words = line.split();
                if len(words) == 2:
                    return words[1];
                break;
        return None;
    '''
    else:
        print("Error: latch_accounts file doesn't exist")
        exit()
    '''

def isPair(user):
    if os.path.isfile(LATCH_ACCOUNTS):
        # read latch_accounts file
        f = open(LATCH_ACCOUNTS,"r")
        lines = f.readlines()
        f.close()
        # find user
        found = False
        for line in lines:
            words = line.split();
            if words[0] == user + ':':
                found = True
                break
        if found:
            return True
        return False
    '''
    else:
        print("Error: latch_accounts file doesn't exist")
        exit()
    '''

def deleteAccount(accountId):
    # read latch_accounts file
    f = open(LATCH_ACCOUNTS,"r")
    lines = f.readlines()
    f.close()
    # delete latch account
    f = open(LATCH_ACCOUNTS,"w")
    for line in lines:
        if line.find(accountId) == -1 :
            f.write(line);
    f.close();

def addAccount(user, accountId):
    if os.path.isfile(LATCH_ACCOUNTS):
        # add latch account
        f = open (LATCH_ACCOUNTS, "a")
        f.write(user + ": " + accountId + "\n")
        f.close();
    else:
        # add latch account
        fd = os.open (LATCH_ACCOUNTS, os.O_WRONLY | os.O_CREAT, int("0600",8))
        f = os.fdopen(fd)
        f.write(user + ": " + accountId + "\n");
        f.close();
