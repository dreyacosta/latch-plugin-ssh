CFLAGS +=  -Wall
all: /lib/security/pam_latch_otp.so

clean:
	$(RM) /lib/security/pam_latch_otp.so *.o
	
/lib/security/pam_latch_otp.so: pam_latch_otp.c ../latch.h
	$(CC) $(CFLAGS) -fPIC -shared -Xlinker -x -o $@ ../latch.c $< -lcurl -lcrypto -lpam
