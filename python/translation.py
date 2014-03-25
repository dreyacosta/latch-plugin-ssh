'''
 This script helps to translate plugin
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



PLUGIN_TITLE = "SSH - latch"
CONFIG_TITLE = "SSH - latch settings"

PAIR_TITLE = "Pair"
UNPAIR_TITLE = "Unpair"
EXIT_TITLE = "Exit"
ERROR_TITLE = "Error"

SECRET_KEY = "Secret key"
APP_ID = "Application ID"

PAIR_MSG = "Your account is unprotected"
UNPAIR_MSG = "Your account is protected with Latch"

INSERT_PAIRING_CODE_MSG = "Insert your pairing code"
CONFIG_MSG = "Identify your application"

REQUIRED_FIELD_MSG = "is a required field."

PAIRED_SUCCESSFULLY_MSG = "Account paired successfully"
UNPAIRED_SUCCESSFULLY_MSG = "Account unpaired successfully"

CANT_READ_CONFIG_FILE_MSG = "Can't read config file"
CANT_READ_ACCOUNTS_FILE_MSG = "Can't read latch_accounts file"
EMPTY_PAIRING_CODE_MSG = "You didn't put a token"
BAD_PAIRING_CODE_LENGTH_MSG = "Token not found"
SOME_EXCEPTION_MSG = "Some exception happened"
INVALID_APP_SIGN_MSG = "Settings error: Bad secret key or application id"

CANT_OPEN_SSHD_PAM_MSG = "Can't open sshd pam config file"
CANT_OPEN_SSHD_CONFIG_MSG = "Can't open sshd_config file"

PAIRED_USER_MSG_PART_1 = "User '"
PAIRED_USER_MSG_PART_2 = "' is already paired"
# "User '"+ user + "' is already paired."

UNPAIRED_USER_MSG_PART_1 = "User '"
UNPAIRED_USER_MSG_PART_2 = "' not paired"
# "User '" + user + "' not paired."

INCORRECT_PAIR_USE_MSG = "use 'pair.py <TOKEN> [ -f <file.conf> ]'"
INCORRECT_UNPAIR_USE_MSG = "use 'unpair.py [ -f <file.conf> ]'"
INCORRECT_SETUP_USE_MSG = "use 'setup.py -f <file.conf>'"
INCORRECT_SETTINGS_USE_MSG = "use 'settings.py -f <file.conf>'"

INSTALLING_MSG = "latch plugin installing..."
UNINSTALLED_MSG = "Uninstall completed"