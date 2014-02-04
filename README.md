### LATCH SSH PLUGIN -- INSTALLATION GUIDE ###


#### PREREQUISITES ####

 * OpenSSH version 5.9. (UNIX system)

 * Libraries: python3 python3-tk (apt-get install)

 * EasyGui (included in latch-plugin-ssh package)

* To get the "Application ID" and "Secret", (fundamental values for integrating Latch in any application), it’s necessary to register a developer account in Latch's website: https://latch.elevenpaths.com. On the upper right side, click on "Developer area".


#### INSTALLING THE PLUGIN IN SSH ####

1. Go to "python" directory in plugin package, open and edit "latch-model.conf" file. Add your settings and save it in the same directory as "latch.conf".

2. Open a terminal. Change to "python" directory, where you have saved the "latch.conf" file. Run "sudo python3 install.py -f latch.conf".

3. Linux Restart SSH "sudo /etc/init.d/ssh restart".
