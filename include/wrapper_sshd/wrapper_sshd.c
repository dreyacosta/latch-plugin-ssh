#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <syslog.h>
#include <pwd.h>

#include "latch.h"



static const char* getAccountId(const char* pUser, const char* pAccounts) {

	char * line = NULL;
	char * token = NULL;
	size_t len = 0;
	ssize_t read;
	const char delimiters[]= " \t\n";
	FILE *fp;

	fp = fopen(pAccounts,"r");
	if (fp == NULL) {
        	//perror("Failed to open file \"latch accounts\"");
        	return NULL;
    	}

	while((read = getline(&line,&len, fp)) != -1){
		token = strsep(&line,delimiters);
		if(token[strlen(token)-1] == ':'  &&  strncmp(token,pUser,strlen(token)-1) == 0){
			token = strsep(&line,delimiters);
			if(strlen(token) == 64){
				return token;
			}else{
				return NULL;
			}
		}
	}

	return NULL;
}

/*
 * Get config parameters of the form: parameter = value (from LATCH_CONFIG file)
 * 
 * @return Pointer to value
 * @return '\0' if value is not found ( parameter =  )
 * @return NULL other case
 */
static const char *getConfig(const char* pParameter, const char* pConfig) {

	char * line = NULL;
	char * token = NULL;
	size_t len = 0;
	ssize_t read;
	const char delimiters[]= " \t\n";

	FILE *fp = fopen(pConfig,"r");
	if (fp == NULL) {
        	//perror("Failed to open file \"latch.conf\"");
        	return NULL;
    	}

	while((read = getline(&line,&len, fp)) != -1){
		token = strsep(&line,delimiters);
		if(strcmp(pParameter,token) == 0  &&  strcmp("=", strsep(&line,delimiters)) == 0){
			return strsep(&line,delimiters);
		}
	}

	return NULL;
}

void send_syslog_alert(){  

	openlog ("Latch", LOG_PID, LOG_AUTH); 
	syslog (LOG_ALERT, "Latch-auth-pam warning: Someone tried to access. Latch locked");  
	closelog ();
}


const char *getUserName(){
	register struct passwd *pw;
	register uid_t uid;

	uid = getuid();
	pw = getpwuid(uid);
	if (pw){
		return pw->pw_name;
	}
	return NULL;
}


int latch()
{
	const char* pUsername = NULL;				
	const char* pAccountId = NULL;
	const char* pSecretKey = NULL;
	const char* pAppId = NULL;
	const char* pAccounts = "/usr/lib/latch/openssh/.latch_accounts";
	const char* pConfig = "/etc/ssh-latch.conf";
	char *buffer;

	pUsername = getUserName();

	pAccountId = getAccountId(pUsername, pAccounts);
	if (pAccountId == NULL) {
		return 0;
	}

	pAppId = getConfig("app_id", pConfig);
	pSecretKey = getConfig("secret_key", pConfig);
	
	if(pAppId == NULL || pSecretKey == NULL){
		//perror("Failed to read \"latch.conf\"");
		return 0;
	}

	if(strcmp(pAppId,"") == 0 || strcmp(pSecretKey,"") == 0){
		//perror("Failed to read \"latch.conf\"");
		return 0;
	}

	init(pAppId, pSecretKey);
	setHost("https://latch.elevenpaths.com");

	buffer = status(pAccountId);
	
	if(buffer == NULL || strcmp(buffer,"") == 0){
		return 0;
	}
	if (strstr(buffer, "\"status\":\"off\"") != NULL){
		//fprintf (stderr, "Latch locked\n");
                send_syslog_alert();
		return 1;
	}
	return 0;
}



int main( void )
{
	if (latch()){
		return 1;
	}else{
		execl("/usr/sbin/sshd.sh", "sshd.sh", NULL);
	}

	return 0;
}
