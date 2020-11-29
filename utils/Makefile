default: build

#LDFLAGS=`pkg-config --libs gtk+-3.0`
override CFLAGS += -march=native -O3 -pipe -flto -fuse-linker-plugin
CC=gcc

build: saveFileInspector.c
	$(CC) $(CFLAGS) $(LDFLAGS) -o saveFileInspector saveFileInspector.c
clean:
	$(RM) saveFileInspector
