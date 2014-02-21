#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>


int main(int argc, char **argv)
{
	if(argc == 1){
		execl("/usr/lib/latch/openssh/settingsGUI.py", "settingsGUI.py", NULL);
	}else if(argc == 3 && strncmp("-f", argv[1], 2) == 0){
		execl("/usr/lib/latch/openssh/settings.py", "settings.py", "-f", argv[2], NULL);
	}else{
		printf("use 'sudo config_latchSSH [-f latch.conf]'\n");
	}
	

	return 0;
}
