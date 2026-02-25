/*
 * Struct Memory Layout Demonstration
 * 
 * Educational program demonstrating:
 * - Struct declaration and initialization
 * - Memory layout and padding
 * - Structure alignment rules
 * - sizeof() operator behavior
 * - Bit fields
 * - Nested structures
 * - Structure packing
 * - Unions vs Structs
 * - Practical examples
 * 
 * Compile: gcc -Wall -Wextra -g -O2 struct_memory_demo.c -o bin/struct_memory_demo
 * Run: ./bin/struct_memory_demo
 */

#include <stdio.h>
#include <stddef.h>
#include <stdint.h>
#include <string.h>

// ============================================================================
// SECTION 1: Basic Struct Declaration
// ============================================================================

struct BasicStruct {
    int id;
    char grade;
    double score;
};

void demo_basic_struct(void) {
    printf("\n");
    printf("╔════════════════════════════════════════════════════════╗\n");
    printf("║  1. BASIC STRUCT - Declaration and Memory Layout      ║\n");
    printf("╚════════════════════════════════════════════════════════╝\n\n");
    
    struct BasicStruct student = {101, 'A', 95.5};
    
    printf("struct BasicStruct {\n");
    printf("    int id;        // 4 bytes\n");
    printf("    char grade;    // 1 byte\n");
    printf("    double score;  // 8 bytes\n");
    printf("};\n\n");
    
    printf("Values:\n");
    printf("  id    = %d\n", student.id);
    printf("  grade = %c\n", student.grade);
    printf("  score = %.1f\n\n", student.score);
    
    printf("sizeof(struct BasicStruct) = %zu bytes\n", sizeof(struct BasicStruct));
    printf("Expected without padding: 4 + 1 + 8 = 13 bytes\n");
    printf("Actual with padding: %zu bytes\n\n", sizeof(struct BasicStruct));
    
    printf("Key Insight: Compiler adds padding for alignment!\n");
}

// ============================================================================
// SECTION 2: Memory Padding and Alignment
// ============================================================================

struct PaddingDemo {
    char a;      // 1 byte
    int b;       // 4 bytes (requires 4-byte alignment)
    char c;      // 1 byte
    double d;    // 8 bytes (requires 8-byte alignment)
};

void demo_padding(void) {
    printf("\n");
    printf("╔════════════════════════════════════════════════════════╗\n");
    printf("║  2. MEMORY PADDING - Alignment Requirements           ║\n");
    printf("╚════════════════════════════════════════════════════════╝\n\n");
    
    struct PaddingDemo demo;
    
    printf("struct PaddingDemo {\n");
    printf("    char a;    // 1 byte\n");
    printf("    int b;     // 4 bytes\n");
    printf("    char c;    // 1 byte\n");
    printf("    double d;  // 8 bytes\n");
    printf("};\n\n");
    
    printf("Member Addresses and Offsets:\n");
    printf("┌─────────┬──────────┬────────────┬─────────────┐\n");
    printf("│ Member  │ Offset   │ Size       │ Padding     │\n");
    printf("├─────────┼──────────┼────────────┼─────────────┤\n");
    printf("│ char a  │ %8zu │ 1 byte     │ 3 bytes     │\n", offsetof(struct PaddingDemo, a));
    printf("│ int b   │ %8zu │ 4 bytes    │ 0 bytes     │\n", offsetof(struct PaddingDemo, b));
    printf("│ char c  │ %8zu │ 1 byte     │ 7 bytes     │\n", offsetof(struct PaddingDemo, c));
    printf("│ double d│ %8zu │ 8 bytes    │ 0 bytes     │\n", offsetof(struct PaddingDemo, d));
    printf("└─────────┴──────────┴────────────┴─────────────┘\n\n");
    
    printf("Total size: %zu bytes\n", sizeof(struct PaddingDemo));
    printf("Without padding: 1 + 4 + 1 + 8 = 14 bytes\n");
    printf("With padding: %zu bytes (10 bytes of padding!)\n\n", sizeof(struct PaddingDemo));
    
    printf("Memory Layout Visualization:\n");
    printf("[a][PPP][bbbb][c][PPPPPPP][dddddddd]\n");
    printf(" 1  3    4     1    7        8      = 24 bytes\n\n");
    
    printf("Key Insight: Padding ensures proper alignment for performance\n");
}

// ============================================================================
// SECTION 3: Optimized Struct Layout
// ============================================================================

struct UnoptimizedStruct {
    char a;
    int b;
    char c;
    int d;
};

struct OptimizedStruct {
    int b;
    int d;
    char a;
    char c;
};

void demo_optimization(void) {
    printf("\n");
    printf("╔════════════════════════════════════════════════════════╗\n");
    printf("║  3. STRUCT OPTIMIZATION - Order Matters!              ║\n");
    printf("╚════════════════════════════════════════════════════════╝\n\n");
    
    printf("Unoptimized Layout (poor ordering):\n");
    printf("struct UnoptimizedStruct {\n");
    printf("    char a; int b; char c; int d;\n");
    printf("};\n");
    printf("Size: %zu bytes\n\n", sizeof(struct UnoptimizedStruct));
    
    printf("Optimized Layout (better ordering):\n");
    printf("struct OptimizedStruct {\n");
    printf("    int b; int d; char a; char c;\n");
    printf("};\n");
    printf("Size: %zu bytes\n\n", sizeof(struct OptimizedStruct));
    
    printf("Comparison:\n");
    printf("┌─────────────────┬──────────┬──────────────┐\n");
    printf("│ Struct          │ Size     │ Savings      │\n");
    printf("├─────────────────┼──────────┼──────────────┤\n");
    printf("│ Unoptimized     │ %2zu bytes│ -            │\n", sizeof(struct UnoptimizedStruct));
    printf("│ Optimized       │ %2zu bytes│ %2zu bytes    │\n", 
           sizeof(struct OptimizedStruct),
           sizeof(struct UnoptimizedStruct) - sizeof(struct OptimizedStruct));
    printf("└─────────────────┴──────────┴──────────────┘\n\n");
    
    printf("Best Practice: Group members by size (largest first)\n");
}

// ============================================================================
// SECTION 4: Packed Structures
// ============================================================================

struct NormalStruct {
    char a;
    int b;
    char c;
} __attribute__((aligned(1)));

struct PackedStruct {
    char a;
    int b;
    char c;
} __attribute__((packed));

void demo_packing(void) {
    printf("\n");
    printf("╔════════════════════════════════════════════════════════╗\n");
    printf("║  4. PACKED STRUCTURES - Forcing No Padding            ║\n");
    printf("╚════════════════════════════════════════════════════════╝\n\n");
    
    printf("Normal struct (with padding):\n");
    printf("Size: %zu bytes\n\n", sizeof(struct NormalStruct));
    
    printf("Packed struct (no padding):\n");
    printf("Size: %zu bytes\n\n", sizeof(struct PackedStruct));
    
    printf("Comparison:\n");
    printf("┌─────────────┬──────────┬────────────────────┐\n");
    printf("│ Type        │ Size     │ Performance        │\n");
    printf("├─────────────┼──────────┼────────────────────┤\n");
    printf("│ Normal      │ %2zu bytes│ Fast (aligned)     │\n", sizeof(struct NormalStruct));
    printf("│ Packed      │ %2zu bytes│ Slow (unaligned)   │\n", sizeof(struct PackedStruct));
    printf("└─────────────┴──────────┴────────────────────┘\n\n");
    
    printf("Warning: Packed structs sacrifice performance for space!\n");
    printf("Use only when necessary (file formats, network protocols)\n");
}

// ============================================================================
// SECTION 5: Nested Structures
// ============================================================================

struct Address {
    char street[50];
    char city[30];
    int zipcode;
};

struct Person {
    char name[50];
    int age;
    struct Address addr;
};

void demo_nested_structs(void) {
    printf("\n");
    printf("╔════════════════════════════════════════════════════════╗\n");
    printf("║  5. NESTED STRUCTURES - Struct within Struct          ║\n");
    printf("╚════════════════════════════════════════════════════════╝\n\n");
    
    struct Person person = {
        "John Doe",
        30,
        {"123 Main St", "New York", 10001}
    };
    
    printf("struct Address {\n");
    printf("    char street[50]; char city[30]; int zipcode;\n");
    printf("};\n");
    printf("sizeof(Address) = %zu bytes\n\n", sizeof(struct Address));
    
    printf("struct Person {\n");
    printf("    char name[50]; int age; struct Address addr;\n");
    printf("};\n");
    printf("sizeof(Person) = %zu bytes\n\n", sizeof(struct Person));
    
    printf("Member Offsets:\n");
    printf("  name   at offset %zu\n", offsetof(struct Person, name));
    printf("  age    at offset %zu\n", offsetof(struct Person, age));
    printf("  addr   at offset %zu\n\n", offsetof(struct Person, addr));
    
    printf("Accessing nested members:\n");
    printf("  person.name = %s\n", person.name);
    printf("  person.age = %d\n", person.age);
    printf("  person.addr.city = %s\n", person.addr.city);
    printf("  person.addr.zipcode = %d\n", person.addr.zipcode);
}

// ============================================================================
// SECTION 6: Bit Fields
// ============================================================================

struct BitFields {
    unsigned int flag1 : 1;   // 1 bit
    unsigned int flag2 : 1;   // 1 bit
    unsigned int value : 6;   // 6 bits
    unsigned int type : 3;    // 3 bits
    unsigned int reserved : 21; // 21 bits
};

void demo_bit_fields(void) {
    printf("\n");
    printf("╔════════════════════════════════════════════════════════╗\n");
    printf("║  6. BIT FIELDS - Packing Data into Bits               ║\n");
    printf("╚════════════════════════════════════════════════════════╝\n\n");
    
    struct BitFields bf = {1, 0, 42, 5, 0};
    
    printf("struct BitFields {\n");
    printf("    unsigned int flag1 : 1;     // 1 bit\n");
    printf("    unsigned int flag2 : 1;     // 1 bit\n");
    printf("    unsigned int value : 6;     // 6 bits\n");
    printf("    unsigned int type : 3;      // 3 bits\n");
    printf("    unsigned int reserved : 21; // 21 bits\n");
    printf("};                              // Total: 32 bits = 4 bytes\n\n");
    
    printf("sizeof(BitFields) = %zu bytes\n\n", sizeof(struct BitFields));
    
    printf("Values:\n");
    printf("  flag1 = %u\n", bf.flag1);
    printf("  flag2 = %u\n", bf.flag2);
    printf("  value = %u\n", bf.value);
    printf("  type = %u\n\n", bf.type);
    
    printf("Use Cases:\n");
    printf("  - Hardware registers\n");
    printf("  - Flags and options\n");
    printf("  - Network packet headers\n");
    printf("  - Embedded systems programming\n");
}

// ============================================================================
// SECTION 7: Unions vs Structs
// ============================================================================

union DataUnion {
    int i;
    float f;
    char str[20];
};

struct DataStruct {
    int i;
    float f;
    char str[20];
};

void demo_union_vs_struct(void) {
    printf("\n");
    printf("╔════════════════════════════════════════════════════════╗\n");
    printf("║  7. UNIONS vs STRUCTS - Overlapping Memory            ║\n");
    printf("╚════════════════════════════════════════════════════════╝\n\n");
    
    union DataUnion u;
    struct DataStruct s;
    
    printf("Union (overlapping memory):\n");
    printf("union DataUnion {\n");
    printf("    int i;         // 4 bytes\n");
    printf("    float f;       // 4 bytes\n");
    printf("    char str[20];  // 20 bytes\n");
    printf("};\n");
    printf("sizeof(union) = %zu bytes\n\n", sizeof(union DataUnion));
    
    printf("Struct (separate memory):\n");
    printf("struct DataStruct {\n");
    printf("    int i;         // 4 bytes\n");
    printf("    float f;       // 4 bytes\n");
    printf("    char str[20];  // 20 bytes\n");
    printf("};\n");
    printf("sizeof(struct) = %zu bytes\n\n", sizeof(struct DataStruct));
    
    printf("Comparison:\n");
    printf("┌─────────┬──────────┬─────────────────────────┐\n");
    printf("│ Type    │ Size     │ Memory Model            │\n");
    printf("├─────────┼──────────┼─────────────────────────┤\n");
    printf("│ Union   │ %2zu bytes│ All members share space │\n", sizeof(union DataUnion));
    printf("│ Struct  │ %2zu bytes│ Each member has space   │\n", sizeof(struct DataStruct));
    printf("└─────────┴──────────┴─────────────────────────┘\n\n");
    
    u.i = 42;
    printf("Union demonstration:\n");
    printf("  u.i = 42\n");
    printf("  u.i value = %d\n", u.i);
    
    u.f = 3.14f;
    printf("  u.f = 3.14\n");
    printf("  u.f value = %.2f\n", u.f);
    printf("  u.i value = %d (corrupted!)\n\n", u.i);
    
    printf("Key Insight: Union members share the same memory!\n");
}

// ============================================================================
// SECTION 8: sizeof() Operator
// ============================================================================

void demo_sizeof(void) {
    printf("\n");
    printf("╔════════════════════════════════════════════════════════╗\n");
    printf("║  8. sizeof() OPERATOR - Size Calculations             ║\n");
    printf("╚════════════════════════════════════════════════════════╝\n\n");
    
    struct BasicStruct bs;
    struct BasicStruct arr[10];
    
    printf("Basic Types:\n");
    printf("┌──────────────┬──────────┐\n");
    printf("│ Type         │ Size     │\n");
    printf("├──────────────┼──────────┤\n");
    printf("│ char         │ %2zu bytes│\n", sizeof(char));
    printf("│ short        │ %2zu bytes│\n", sizeof(short));
    printf("│ int          │ %2zu bytes│\n", sizeof(int));
    printf("│ long         │ %2zu bytes│\n", sizeof(long));
    printf("│ long long    │ %2zu bytes│\n", sizeof(long long));
    printf("│ float        │ %2zu bytes│\n", sizeof(float));
    printf("│ double       │ %2zu bytes│\n", sizeof(double));
    printf("│ void*        │ %2zu bytes│\n", sizeof(void*));
    printf("└──────────────┴──────────┘\n\n");
    
    printf("Struct Sizes:\n");
    printf("  sizeof(struct BasicStruct) = %zu bytes\n", sizeof(struct BasicStruct));
    printf("  sizeof(bs) = %zu bytes\n", sizeof(bs));
    printf("  sizeof(arr) = %zu bytes\n", sizeof(arr));
    printf("  sizeof(arr[0]) = %zu bytes\n\n", sizeof(arr[0]));
    
    printf("Array Length Calculation:\n");
    printf("  length = sizeof(arr) / sizeof(arr[0])\n");
    printf("  length = %zu / %zu = %zu elements\n", 
           sizeof(arr), sizeof(arr[0]), sizeof(arr) / sizeof(arr[0]));
}

// ============================================================================
// SECTION 9: Practical Example - Network Packet
// ============================================================================

struct PacketHeader {
    uint8_t version : 4;
    uint8_t header_len : 4;
    uint8_t type_of_service;
    uint16_t total_length;
    uint16_t identification;
    uint16_t flags_fragment;
    uint8_t time_to_live;
    uint8_t protocol;
    uint16_t checksum;
    uint32_t source_ip;
    uint32_t dest_ip;
} __attribute__((packed));

void demo_practical_packet(void) {
    printf("\n");
    printf("╔════════════════════════════════════════════════════════╗\n");
    printf("║  9. PRACTICAL EXAMPLE - Network Packet Header         ║\n");
    printf("╚════════════════════════════════════════════════════════╝\n\n");
    
    struct PacketHeader packet = {
        .version = 4,
        .header_len = 5,
        .type_of_service = 0,
        .total_length = 60,
        .identification = 12345,
        .flags_fragment = 0,
        .time_to_live = 64,
        .protocol = 6,  // TCP
        .checksum = 0xABCD,
        .source_ip = 0xC0A80001,  // 192.168.0.1
        .dest_ip = 0xC0A80002     // 192.168.0.2
    };
    
    printf("IPv4 Packet Header Structure:\n\n");
    printf("struct PacketHeader {\n");
    printf("    uint8_t version : 4;\n");
    printf("    uint8_t header_len : 4;\n");
    printf("    uint8_t type_of_service;\n");
    printf("    uint16_t total_length;\n");
    printf("    uint16_t identification;\n");
    printf("    uint16_t flags_fragment;\n");
    printf("    uint8_t time_to_live;\n");
    printf("    uint8_t protocol;\n");
    printf("    uint16_t checksum;\n");
    printf("    uint32_t source_ip;\n");
    printf("    uint32_t dest_ip;\n");
    printf("} __attribute__((packed));\n\n");
    
    printf("sizeof(PacketHeader) = %zu bytes (20 bytes standard)\n\n", 
           sizeof(struct PacketHeader));
    
    printf("Packet Contents:\n");
    printf("  Version: %u\n", packet.version);
    printf("  Header Length: %u words\n", packet.header_len);
    printf("  Total Length: %u bytes\n", packet.total_length);
    printf("  TTL: %u\n", packet.time_to_live);
    printf("  Protocol: %u (TCP)\n", packet.protocol);
    printf("  Source IP: 0x%08X\n", packet.source_ip);
    printf("  Dest IP: 0x%08X\n\n", packet.dest_ip);
    
    printf("Use Case: Parsing network packets in low-level code\n");
}

// ============================================================================
// SECTION 10: Key Takeaways
// ============================================================================

void demo_key_takeaways(void) {
    printf("\n");
    printf("╔════════════════════════════════════════════════════════╗\n");
    printf("║                    KEY TAKEAWAYS                       ║\n");
    printf("╚════════════════════════════════════════════════════════╝\n\n");
    
    printf("1. Structs can have padding for alignment (performance)\n");
    printf("2. Member order affects struct size\n");
    printf("3. offsetof() shows member positions within struct\n");
    printf("4. Packed structs remove padding (use with caution)\n");
    printf("5. Unions share memory; only one member valid at a time\n");
    printf("6. Bit fields pack data into individual bits\n");
    printf("7. sizeof(struct) includes all padding\n");
    printf("8. Nested structs are laid out contiguously\n");
    printf("9. Alignment rules depend on the platform\n");
    printf("10. Understanding memory layout is crucial for:\n");
    printf("    - Performance optimization\n");
    printf("    - File I/O and serialization\n");
    printf("    - Network protocols\n");
    printf("    - Hardware interfacing\n\n");
    
    printf("✓ Demonstration complete!\n\n");
}

// ============================================================================
// MAIN FUNCTION
// ============================================================================

int main(void) {
    printf("\n");
    printf("╔════════════════════════════════════════════════════════╗\n");
    printf("║                                                        ║\n");
    printf("║        STRUCT MEMORY LAYOUT DEMONSTRATION             ║\n");
    printf("║         Comprehensive C Programming Guide             ║\n");
    printf("║                                                        ║\n");
    printf("╚════════════════════════════════════════════════════════╝\n");
    
    demo_basic_struct();
    demo_padding();
    demo_optimization();
    demo_packing();
    demo_nested_structs();
    demo_bit_fields();
    demo_union_vs_struct();
    demo_sizeof();
    demo_practical_packet();
    demo_key_takeaways();
    
    return 0;
}
