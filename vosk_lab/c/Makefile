CFLAGS=-I../src
# LDFLAGS=-L../src -lvosk -ldl -lpthread -Wl,-rpath,../src
# LDFLAGS=-L../src -lvosk -ldl -lpthread -Wl,-rpath,'$$ORIGIN/../src'
LDFLAGS=-L../src -lvosk -ldl -lpthread -Wl,--enable-new-dtags -Wl,-rpath,'$$ORIGIN/../src'




all: libvosk_recognizer.so

libvosk_recognizer.so: test_vosk.o
	gcc -shared -o libvosk_recognizer.so test_vosk.o $(LDFLAGS)

%.o: %.c
	gcc $(CFLAGS) -c -fPIC -o $@ $<

clean:
	rm -f *.o *.a libvosk_recognizer.so





# CFLAGS=-I../src
# LDFLAGS=-L../src -lvosk -ldl -lpthread -Wl,-rpath,../src

# all: test_vosk test_vosk_speaker

# test_vosk: test_vosk.o
# 	gcc $^ -o $@ $(LDFLAGS)

# test_vosk_speaker: test_vosk_speaker.o
# 	gcc $^ -o $@ $(LDFLAGS)

# %.o: %.c
# 	gcc $(CFLAGS) -c -o $@ $<

# clean:
# 	rm -f *.o *.a test_vosk test_vosk_speaker
