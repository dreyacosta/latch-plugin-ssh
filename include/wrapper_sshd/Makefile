CFLAGS +=  -Wall

CC = gcc 
OBJECTS = latch.o

wp_sshd : wrapper_sshd.o $(OBJECTS)
	$(CC) $(CFLAGS) -o wp_sshd wrapper_sshd.o $(OBJECTS) -lcurl -lcrypto

wrapper_sshd.o: latch.h
latch.o: latch.h

.PHONY : clean
    clean :
	-rm wp_sshd $(objects) 
