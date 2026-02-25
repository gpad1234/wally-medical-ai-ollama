# Makefile — build libsimpledb shared library
# Output: build/lib/libsimpledb.so  (Linux)
#          build/lib/libsimpledb.dylib (macOS)

CC      = gcc
CFLAGS  = -Wall -Wextra -O2 -fPIC -std=c11
SRC     = simple_db.c
HEADER  = simple_db.h
OUTDIR  = build/lib

# Platform detection
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    EXT     = .dylib
    LDFLAGS = -dynamiclib
else
    EXT     = .so
    LDFLAGS = -shared
endif

LIB = $(OUTDIR)/libsimpledb$(EXT)

.PHONY: all clean

all: $(LIB)

$(OUTDIR):
	mkdir -p $(OUTDIR)

$(LIB): $(SRC) $(HEADER) | $(OUTDIR)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $(SRC)
	@echo "Built: $@"

clean:
	rm -rf build
