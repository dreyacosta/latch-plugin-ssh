#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>



int latch()
{
    int i,f;
    f= fork();
    if (f==0){
        execl("/usr/sbin/sshd.py", "sshd.py", NULL);
    }

    int status;
    wait(&status);

    return status;
    
}


int main( void )
{
    int j;
    j= latch();

    if (j){
        printf("disconnect\n");
    }else{
        execl("/usr/sbin/sshd.sh", "sshd.sh", NULL);
    }

    return 0;
}
