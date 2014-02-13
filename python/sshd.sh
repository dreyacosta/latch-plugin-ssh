#!/bin/bash

if test -z "$SSH_ORIGINAL_COMMAND"
    then
      exec `grep "^$(whoami)" /etc/passwd | cut -d ":" -f 7`
    else
      exec "$SSH_ORIGINAL_COMMAND"
fi
