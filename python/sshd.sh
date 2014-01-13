#!/bin/bash
sudo /usr/sbin/sshd.py

if test "$?" = 0
then
  if test -z "$SSH_ORIGINAL_COMMAND"
      then
        exec `grep "^$(whoami)" /etc/passwd | cut -d ":" -f 7`
      else
        exec "$SSH_ORIGINAL_COMMAND"
      fi
else
  echo "disconnect"
fi
