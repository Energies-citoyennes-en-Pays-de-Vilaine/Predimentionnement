cmodules/libsim.so:cmodules/libsim.h cmodules/sim_flex.c cmodules/obj
	make -C cmodules/ libsim.so
cmodules/obj:
	mkdir -p cmodules/obj