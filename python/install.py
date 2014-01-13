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


# run as root

import sys
import os
import shutil

if len(sys.argv) == 3 and sys.argv[1] == "-f":
    # read config file
    f = open(sys.argv[2],"r")
    lines = f.readlines()
    f.close()
    # write config file
    f = open("/etc/pam.d/latch.conf","w")
    f.writelines(lines)
    f.close()
else:
    print("use 'install.py -f <file.conf>'");
    exit();

# read sshd_config file
# f = open("/etc/pam.d/sshd","r")
f = open("/etc/ssh/sshd_config","r")
lines = f.readlines()
f.close()

# find latch 
found = False
for line in lines:
    # if line.find("auth       required	    /lib/security/pam_latch.so") != -1 :
    if line.find("ForceCommand /usr/sbin/sshd.sh") != -1 :
        found = True
        break

if not found:  
    '''
    # add latch PAM to ssh configuration
    f = open("/etc/pam.d/sshd","a")
    f.write("auth       required	    /lib/security/pam_latch.so")
    f.close()
    '''
    # add latch to ssh configuration
    f = open("/etc/ssh/sshd_config","a")
    f.write("ForceCommand /usr/sbin/sshd.sh")
    f.close()
    # install the two wrappers, sshd.sh and sshd.py in /usr/sbin 
    shutil.copy("sshd.sh", "/usr/sbin")
    shutil.copy("sshd.py", "/usr/sbin") 
    # install latch in /etc/ssh 
    shutil.copytree(".", "/etc/ssh/latch")
    # add sudo privileges for latch execution
    fd = os.open ("/etc/sudoers.d/latch_conf", os.O_CREAT, int("0440",8)) 
    f = open("/etc/sudoers.d/latch_conf","a")
    f.write("ALL ALL= NOPASSWD: /usr/sbin/sshd.py\n");
    f.write("ALL ALL= NOPASSWD: /etc/ssh/latch/gui/latchPlugin.py\n");
    f.close();
    # add latch_accounts file 
    fd = os.open ("/etc/pam.d/latch_accounts", os.O_CREAT, int("0600",8))
    print("Latch ssh plugin has been installed") 
else:
    print("Latch ssh plugin is already installed")
