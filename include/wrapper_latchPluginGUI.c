#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


int main( void )
{
   execl("/usr/lib/openssh/latch/latchPluginGUI.py", "latchPluginGUI.py", NULL);

   return 0;
}
