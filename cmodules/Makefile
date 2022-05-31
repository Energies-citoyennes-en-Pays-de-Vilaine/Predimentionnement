CFLAGS=-fPIC
libsim.so: obj/sim_flex.o
	gcc ${CFLAGS} -shared  obj/*.o -o libsim.so
obj/sim_flex.o: sim_flex.c libsim.h
	gcc ${CFLAGS} -c sim_flex.c -o obj/sim_flex.o