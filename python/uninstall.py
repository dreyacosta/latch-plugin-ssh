'''
 This script allows to uninstall latch plugin from ssh Server in some UNIX systems (like Linux)
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

import os
import shutil

# read PAM sshd file
f = open("/etc/pam.d/sshd","r");
lines = f.readlines();
f.close();
# delete latch PAM 
f = open("/etc/pam.d/sshd","w");
for line in lines:
    if line.find("/lib/security/pam_latch.so") == -1 :
        f.write(line);
f.close();

# read sshd_config file
f = open("/etc/ssh/sshd_config","r");
lines = f.readlines();
f.close();
# delete latch
f = open("/etc/ssh/sshd_config","w");
for line in lines:
    if line.find("ForceCommand /usr/sbin/sshd.sh") == -1 :
        f.write(line);
f.close();


if os.path.isfile("/etc/pam.d/latch_accounts"):
    os.remove("/etc/pam.d/latch_accounts")
if os.path.isfile("/etc/pam.d/latch.conf"):
    os.remove("/etc/pam.d/latch.conf")
if os.path.isfile("/lib/security/pam_latch.so"):
    os.remove("/lib/security/pam_latch.so")
if os.path.isfile("/usr/sbin/sshd.sh"):
    os.remove("/usr/sbin/sshd.sh")
if os.path.isfile("/usr/sbin/sshd.py"):
    os.remove("/usr/sbin/sshd.py")
if os.path.isfile("/etc/sudoers.d/latch_conf"):
    os.remove("/etc/sudoers.d/latch_conf")
if os.path.isdir("/etc/ssh/latch"):
    shutil.rmtree("/etc/ssh/latch")
print("Uninstall completed")
