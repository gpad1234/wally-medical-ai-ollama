# Makefile for Linked List Project
# Compiler and flags
CC = gcc
CFLAGS = -Wall -Wextra -g -O2
LDFLAGS = -lm

# Detect OS
UNAME_S := $(shell uname -s)

# Directories
SRC_DIR = .
BIN_DIR = bin
OBJ_DIR = obj

# Source files
LIBRARY_SRC = linked_list.c
DRIVER_SRC = driver.c
TEST_SRC = test.c
ANIMATION_SRC = animation.c
ANIMATED_DEMO_SRC = animated_demo.c
DOUBLY_LIBRARY_SRC = doubly_linked_list.c
DOUBLY_DRIVER_SRC = doubly_driver.c
CIRCULAR_LIBRARY_SRC = circular_linked_list.c
CIRCULAR_DRIVER_SRC = circular_driver.c
ARRAY_POINTER_DEMO_SRC = array_pointer_demo.c
STRUCT_MEMORY_DEMO_SRC = struct_memory_demo.c
SIMPLE_DB_SRC = simple_db.c

# Object files
LIBRARY_OBJ = $(OBJ_DIR)/linked_list.o
DRIVER_OBJ = $(OBJ_DIR)/driver.o
TEST_OBJ = $(OBJ_DIR)/test.o
ANIMATION_OBJ = $(OBJ_DIR)/animation.o
ANIMATED_DEMO_OBJ = $(OBJ_DIR)/animated_demo.o
DOUBLY_LIBRARY_OBJ = $(OBJ_DIR)/doubly_linked_list.o
DOUBLY_DRIVER_OBJ = $(OBJ_DIR)/doubly_driver.o
CIRCULAR_LIBRARY_OBJ = $(OBJ_DIR)/circular_linked_list.o
CIRCULAR_DRIVER_OBJ = $(OBJ_DIR)/circular_driver.o
ARRAY_POINTER_DEMO_OBJ = $(OBJ_DIR)/array_pointer_demo.o
STRUCT_MEMORY_DEMO_OBJ = $(OBJ_DIR)/struct_memory_demo.o

# Header files
HEADERS = linked_list.h animation.h doubly_linked_list.h circular_linked_list.h

# Executables
DRIVER_BIN = $(BIN_DIR)/linked_list_driver
TEST_BIN = $(BIN_DIR)/test
ANIMATED_DEMO_BIN = $(BIN_DIR)/animated_demo
DOUBLY_DRIVER_BIN = $(BIN_DIR)/doubly_linked_list_driver
CIRCULAR_DRIVER_BIN = $(BIN_DIR)/circular_linked_list_driver
ARRAY_POINTER_DEMO_BIN = $(BIN_DIR)/array_pointer_demo
STRUCT_MEMORY_DEMO_BIN = $(BIN_DIR)/struct_memory_demo
SIMPLE_DB_TEST_BIN = $(BIN_DIR)/simple_db_test

# Shared libraries
ifeq ($(UNAME_S),Darwin)
    SIMPLE_DB_LIB = $(BIN_DIR)/libsimpledb.dylib
else
    SIMPLE_DB_LIB = $(BIN_DIR)/libsimpledb.so
endif

# Phony targets
.PHONY: all clean run run-test run-demo run-doubly run-circular run-array-demo run-struct-demo run-db-test build-db help install rebuild verbose build-all run-graph-db run-graph-examples test-graph run-web-ui

# Default target
all: prepare $(DRIVER_BIN)

prepare:
	@mkdir -p $(BIN_DIR) $(OBJ_DIR)

# Compile library object file
$(LIBRARY_OBJ): $(LIBRARY_SRC) $(HEADERS) | $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $(LIBRARY_SRC) -o $@

# Compile driver object file
$(DRIVER_OBJ): $(DRIVER_SRC) $(HEADERS) | $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $(DRIVER_SRC) -o $@

# Compile test object file
$(TEST_OBJ): $(TEST_SRC) $(HEADERS) | $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $(TEST_SRC) -o $@

# Compile animation object file
$(ANIMATION_OBJ): $(ANIMATION_SRC) $(HEADERS) | $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $(ANIMATION_SRC) -o $@

# Compile animated demo object file
$(ANIMATED_DEMO_OBJ): $(ANIMATED_DEMO_SRC) $(HEADERS) | $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $(ANIMATED_DEMO_SRC) -o $@

# Compile doubly linked list library object file
$(DOUBLY_LIBRARY_OBJ): $(DOUBLY_LIBRARY_SRC) doubly_linked_list.h | $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $(DOUBLY_LIBRARY_SRC) -o $@

# Compile doubly driver object file
$(DOUBLY_DRIVER_OBJ): $(DOUBLY_DRIVER_SRC) doubly_linked_list.h | $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $(DOUBLY_DRIVER_SRC) -o $@

# Compile circular linked list library object file
$(CIRCULAR_LIBRARY_OBJ): $(CIRCULAR_LIBRARY_SRC) circular_linked_list.h | $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $(CIRCULAR_LIBRARY_SRC) -o $@

# Compile circular driver object file
$(CIRCULAR_DRIVER_OBJ): $(CIRCULAR_DRIVER_SRC) circular_linked_list.h | $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $(CIRCULAR_DRIVER_SRC) -o $@

# Compile array pointer demo object file
$(ARRAY_POINTER_DEMO_OBJ): $(ARRAY_POINTER_DEMO_SRC) | $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $(ARRAY_POINTER_DEMO_SRC) -o $@

# Compile struct memory demo object file
$(STRUCT_MEMORY_DEMO_OBJ): $(STRUCT_MEMORY_DEMO_SRC) | $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $(STRUCT_MEMORY_DEMO_SRC) -o $@

# Link driver executable
$(DRIVER_BIN): $(DRIVER_OBJ) $(LIBRARY_OBJ) | $(BIN_DIR)
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)
	@echo "✓ Driver executable created: $@"

# Link test executable
$(TEST_BIN): $(TEST_OBJ) $(LIBRARY_OBJ) | $(BIN_DIR)
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)
	@echo "✓ Test executable created: $@"

# Link animated demo executable
$(ANIMATED_DEMO_BIN): $(ANIMATED_DEMO_OBJ) $(LIBRARY_OBJ) $(ANIMATION_OBJ) | $(BIN_DIR)
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)
	@echo "✓ Animated demo executable created: $@"

# Link doubly linked list driver executable
$(DOUBLY_DRIVER_BIN): $(DOUBLY_DRIVER_OBJ) $(DOUBLY_LIBRARY_OBJ) | $(BIN_DIR)
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)
	@echo "✓ Doubly linked list driver executable created: $@"

# Link circular linked list driver executable
$(CIRCULAR_DRIVER_BIN): $(CIRCULAR_DRIVER_OBJ) $(CIRCULAR_LIBRARY_OBJ) | $(BIN_DIR)
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)
	@echo "✓ Circular linked list driver executable created: $@"

# Link array pointer demo executable
$(ARRAY_POINTER_DEMO_BIN): $(ARRAY_POINTER_DEMO_OBJ) | $(BIN_DIR)
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)
	@echo "✓ Array pointer demo executable created: $@"

# Link struct memory demo executable
$(STRUCT_MEMORY_DEMO_BIN): $(STRUCT_MEMORY_DEMO_OBJ) | $(BIN_DIR)
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)
	@echo "✓ Struct memory demo executable created: $@"

# Build everything including test and animated demo
build-all: prepare $(DRIVER_BIN) $(TEST_BIN) $(ANIMATED_DEMO_BIN) $(DOUBLY_DRIVER_BIN) $(CIRCULAR_DRIVER_BIN) $(ARRAY_POINTER_DEMO_BIN) $(STRUCT_MEMORY_DEMO_BIN) $(SIMPLE_DB_LIB)

# Build only the simple database shared library
libsimpledb.dylib: $(SIMPLE_DB_LIB)
	@echo "✓ Simple database shared library built: $(SIMPLE_DB_LIB)"

	@echo "✓ All executables built successfully!"

# Run the driver
run: $(DRIVER_BIN)
	@echo "Starting interactive driver..."
	@$(DRIVER_BIN)

# Run tests
run-test: $(TEST_BIN)
	@echo "Running tests..."
	@$(TEST_BIN)

# Run animated demo
run-demo: $(ANIMATED_DEMO_BIN)
	@echo "Starting animated linked list demo..."
	@$(ANIMATED_DEMO_BIN)

# Run doubly linked list driver
run-doubly: $(DOUBLY_DRIVER_BIN)
	@echo "Starting doubly linked list interactive driver..."
	@$(DOUBLY_DRIVER_BIN)

# Run circular linked list driver
run-circular: $(CIRCULAR_DRIVER_BIN)
	@echo "Starting circular linked list interactive driver..."
	@$(CIRCULAR_DRIVER_BIN)

# Run array pointer demo
run-array-demo: $(ARRAY_POINTER_DEMO_BIN)
	@echo "Starting array vs pointer arithmetic demo..."
	@$(ARRAY_POINTER_DEMO_BIN)

# Run struct memory demo
run-struct-demo: $(STRUCT_MEMORY_DEMO_BIN)
	@echo "Starting struct memory layout demo..."
	@$(STRUCT_MEMORY_DEMO_BIN)

# Build simple database library and test
build-db: prepare $(SIMPLE_DB_LIB) $(SIMPLE_DB_TEST_BIN)
	@echo "✓ Simple database library and test built"

# Run simple database test
run-db-test: $(SIMPLE_DB_TEST_BIN)
	@echo "Starting simple database test..."
	@$(SIMPLE_DB_TEST_BIN)

# Build simple database shared library
$(SIMPLE_DB_LIB): $(SIMPLE_DB_SRC) | $(BIN_DIR)
	$(CC) -shared -fPIC $(CFLAGS) $< -o $@
	@echo "✓ Simple database library created: $@"

# Build simple database standalone test
$(SIMPLE_DB_TEST_BIN): $(SIMPLE_DB_SRC) | $(BIN_DIR)
	$(CC) $(CFLAGS) -DBUILD_STANDALONE $< -o $@
	@echo "✓ Simple database test executable created: $@"

# Clean build artifacts
clean:
	@echo "Cleaning up..."
	@rm -rf $(OBJ_DIR) $(BIN_DIR)
	@echo "✓ Clean complete!"

# Show help
help:
	@echo "Linked List Project - Makefile Commands"
	@echo "========================================"
	@echo "make              - Build the driver executable"
	@echo "make build-all    - Build all executables"
	@echo "make run          - Run the interactive driver"
	@echo "make run-test     - Run the test program"
	@echo "make libsimpledb.dylib - Build the simple database shared library"
	@echo "make run-demo     - Run animated demo"
	@echo "make run-doubly   - Run doubly linked list driver"
	@echo "make run-circular - Run circular linked list driver"
	@echo "make run-graph-db - Run graph database demo"
	@echo "make run-graph-examples - Run graph examples"
	@echo "make test-graph   - Run all graph tests"
	@echo "make run-web-ui   - Start Graph Database Web UI (port 5000)"
	@echo "make clean        - Remove build artifacts"
	@echo "make help         - Show this help message"
	@echo "========================================"

# Python graph database targets
run-graph-db:
	@echo "Running graph database demo..."
	@python3 graph_db.py

run-graph-examples:
	@echo "Running graph database examples..."
	@python3 graph_examples.py

test-graph: run-graph-db run-graph-examples
	@echo "Graph tests completed"

# Run web UI
run-web-ui:
	@echo "Starting Graph Database Web UI..."
	@echo "Open http://127.0.0.1:5000 in your browser"
	python3 graph_web_ui.py

# Rebuild everything
rebuild: clean all

# Verbose build
verbose: CFLAGS += -v
verbose: clean all
	@echo "✓ Verbose build complete!"
