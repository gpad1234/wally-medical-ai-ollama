#include <stdio.h>
#include <stdlib.h>

// Function to print section headers
void printSection(const char* title) {
    printf("\n╔════════════════════════════════════════════════════════╗\n");
    printf("║  %-52s  ║\n", title);
    printf("╚════════════════════════════════════════════════════════╝\n\n");
}

// Demonstrate basic array access
void arrayBasics() {
    printSection("1. ARRAY BASICS - Declaration and Access");
    
    int arr[5] = {10, 20, 30, 40, 50};
    
    printf("Array declaration: int arr[5] = {10, 20, 30, 40, 50};\n\n");
    
    printf("Array Access Methods:\n");
    printf("┌─────────┬────────────────┬────────────────┬─────────┐\n");
    printf("│ Index   │ Array Notation │ Pointer Notion │ Value   │\n");
    printf("├─────────┼────────────────┼────────────────┼─────────┤\n");
    
    for (int i = 0; i < 5; i++) {
        printf("│ arr[%d]  │ arr[%d]         │ *(arr + %d)     │ %d      │\n", 
               i, i, i, arr[i]);
    }
    printf("└─────────┴────────────────┴────────────────┴─────────┘\n");
    
    printf("\nKey Insight: arr[i] is syntactic sugar for *(arr + i)\n");
}

// Demonstrate pointer arithmetic
void pointerArithmetic() {
    printSection("2. POINTER ARITHMETIC - How Pointers Move");
    
    int arr[5] = {10, 20, 30, 40, 50};
    int *ptr = arr;  // ptr points to arr[0]
    
    printf("Array: {10, 20, 30, 40, 50}\n");
    printf("int *ptr = arr;  // ptr points to first element\n\n");
    
    printf("Pointer Movement:\n");
    printf("┌──────────────┬──────────────────┬─────────────┬────────┐\n");
    printf("│ Expression   │ Address          │ Offset      │ Value  │\n");
    printf("├──────────────┼──────────────────┼─────────────┼────────┤\n");
    
    printf("│ ptr          │ %p │ +0 bytes    │ %d    │\n", (void*)ptr, *ptr);
    printf("│ ptr + 1      │ %p │ +4 bytes    │ %d    │\n", (void*)(ptr + 1), *(ptr + 1));
    printf("│ ptr + 2      │ %p │ +8 bytes    │ %d    │\n", (void*)(ptr + 2), *(ptr + 2));
    printf("│ ptr + 3      │ %p │ +12 bytes   │ %d    │\n", (void*)(ptr + 3), *(ptr + 3));
    printf("│ ptr + 4      │ %p │ +16 bytes   │ %d    │\n", (void*)(ptr + 4), *(ptr + 4));
    printf("└──────────────┴──────────────────┴─────────────┴────────┘\n");
    
    printf("\nKey Insight: ptr + 1 moves by sizeof(int) = %zu bytes\n", sizeof(int));
    printf("             NOT by 1 byte!\n");
}

// Demonstrate equivalence
void arrayPointerEquivalence() {
    printSection("3. ARRAY-POINTER EQUIVALENCE");
    
    int arr[4] = {100, 200, 300, 400};
    
    printf("Array: {100, 200, 300, 400}\n\n");
    
    printf("Equivalent Expressions:\n");
    printf("┌──────────────┬──────────────┬────────┬───────────────────┐\n");
    printf("│ Array        │ Pointer      │ Value  │ Explanation       │\n");
    printf("├──────────────┼──────────────┼────────┼───────────────────┤\n");
    printf("│ arr[0]       │ *(arr + 0)   │ %d   │ First element     │\n", arr[0]);
    printf("│ arr[1]       │ *(arr + 1)   │ %d   │ Second element    │\n", arr[1]);
    printf("│ arr[2]       │ *(arr + 2)   │ %d   │ Third element     │\n", arr[2]);
    printf("│ arr[3]       │ *(arr + 3)   │ %d   │ Fourth element    │\n", arr[3]);
    printf("│ &arr[0]      │ arr          │ Same   │ Address of first  │\n");
    printf("│ &arr[1]      │ arr + 1      │ Same   │ Address of second │\n");
    printf("│ &arr[i]      │ arr + i      │ Same   │ General pattern   │\n");
    printf("└──────────────┴──────────────┴────────┴───────────────────┘\n");
}

// Demonstrate iteration comparison
void iterationComparison() {
    printSection("4. ARRAY vs POINTER ITERATION");
    
    int arr[5] = {5, 15, 25, 35, 45};
    
    printf("Array: {5, 15, 25, 35, 45}\n\n");
    
    // Method 1: Array indexing
    printf("Method 1 - Array Indexing:\n");
    printf("for (int i = 0; i < 5; i++) { printf(\"%%d \", arr[i]); }\n");
    printf("Output: ");
    for (int i = 0; i < 5; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n\n");
    
    // Method 2: Pointer arithmetic
    printf("Method 2 - Pointer Arithmetic:\n");
    printf("int *p; for (p = arr; p < arr + 5; p++) { printf(\"%%d \", *p); }\n");
    printf("Output: ");
    int *p;
    for (p = arr; p < arr + 5; p++) {
        printf("%d ", *p);
    }
    printf("\n\n");
    
    // Method 3: Hybrid
    printf("Method 3 - Hybrid (pointer with offset):\n");
    printf("int *ptr = arr; for (int i = 0; i < 5; i++) { printf(\"%%d \", *(ptr + i)); }\n");
    printf("Output: ");
    int *ptr = arr;
    for (int i = 0; i < 5; i++) {
        printf("%d ", *(ptr + i));
    }
    printf("\n");
}

// Demonstrate pointer subtraction
void pointerSubtraction() {
    printSection("5. POINTER SUBTRACTION - Distance Between Elements");
    
    int arr[6] = {11, 22, 33, 44, 55, 66};
    int *start = &arr[0];
    int *end = &arr[5];
    int *middle = &arr[3];
    
    printf("Array: {11, 22, 33, 44, 55, 66}\n\n");
    
    printf("Pointer Distances:\n");
    printf("┌──────────────────────┬──────────┬────────────────────┐\n");
    printf("│ Expression           │ Result   │ Meaning            │\n");
    printf("├──────────────────────┼──────────┼────────────────────┤\n");
    printf("│ end - start          │ %ld       │ Elements between   │\n", end - start);
    printf("│ middle - start       │ %ld       │ Elements from start│\n", middle - start);
    printf("│ end - middle         │ %ld       │ Elements to end    │\n", end - middle);
    printf("└──────────────────────┴──────────┴────────────────────┘\n");
    
    printf("\nKey Insight: Pointer subtraction gives number of elements,\n");
    printf("             not number of bytes!\n");
}

// Demonstrate array decay
void arrayDecay() {
    printSection("6. ARRAY DECAY - When Arrays Become Pointers");
    
    int arr[4] = {7, 14, 21, 28};
    
    printf("Array: {7, 14, 21, 28}\n\n");
    
    printf("sizeof() Behavior:\n");
    printf("┌─────────────────────┬──────────┬────────────────────┐\n");
    printf("│ Expression          │ Size     │ What It Measures   │\n");
    printf("├─────────────────────┼──────────┼────────────────────┤\n");
    printf("│ sizeof(arr)         │ %zu bytes │ Entire array       │\n", sizeof(arr));
    printf("│ sizeof(arr[0])      │ %zu bytes │ One int element    │\n", sizeof(arr[0]));
    printf("│ sizeof(int*)        │ %zu bytes │ Pointer size       │\n", sizeof(int*));
    printf("└─────────────────────┴──────────┴────────────────────┘\n");
    
    printf("\nArray length calculation:\n");
    printf("Length = sizeof(arr) / sizeof(arr[0]) = %zu / %zu = %zu\n",
           sizeof(arr), sizeof(arr[0]), sizeof(arr) / sizeof(arr[0]));
    
    printf("\nKey Insight: Arrays know their size, pointers don't!\n");
}

// Demonstrate pointer increment/decrement
void pointerIncrementDecrement() {
    printSection("7. POINTER INCREMENT/DECREMENT");
    
    int arr[5] = {1, 2, 3, 4, 5};
    int *ptr = arr + 2;  // Start at middle element (3)
    
    printf("Array: {1, 2, 3, 4, 5}\n");
    printf("int *ptr = arr + 2;  // Points to arr[2] (value 3)\n\n");
    
    printf("Operations:\n");
    printf("┌──────────────┬─────────────┬─────────┬────────────────┐\n");
    printf("│ Operation    │ Expression  │ Value   │ New Position   │\n");
    printf("├──────────────┼─────────────┼─────────┼────────────────┤\n");
    
    printf("│ Initial      │ *ptr        │ %d       │ arr[2]         │\n", *ptr);
    ptr++;
    printf("│ Increment    │ *(ptr++)    │ %d       │ arr[3]         │\n", *ptr);
    ptr++;
    printf("│ Increment    │ *(ptr++)    │ %d       │ arr[4]         │\n", *ptr);
    ptr--;
    printf("│ Decrement    │ *(ptr--)    │ %d       │ arr[3]         │\n", *ptr);
    ptr--;
    printf("│ Decrement    │ *(ptr--)    │ %d       │ arr[2]         │\n", *ptr);
    ptr--;
    printf("│ Decrement    │ *(ptr--)    │ %d       │ arr[1]         │\n", *ptr);
    printf("└──────────────┴─────────────┴─────────┴────────────────┘\n");
}

// Demonstrate multidimensional arrays
void multidimensionalArrays() {
    printSection("8. MULTIDIMENSIONAL ARRAYS - 2D Array Pointers");
    
    int matrix[3][4] = {
        {1, 2, 3, 4},
        {5, 6, 7, 8},
        {9, 10, 11, 12}
    };
    
    printf("Matrix (3x4):\n");
    for (int i = 0; i < 3; i++) {
        printf("  [");
        for (int j = 0; j < 4; j++) {
            printf("%3d", matrix[i][j]);
        }
        printf(" ]\n");
    }
    
    printf("\nAccess Methods:\n");
    printf("┌─────────────┬──────────────────────┬────────┐\n");
    printf("│ Element     │ Pointer Notation     │ Value  │\n");
    printf("├─────────────┼──────────────────────┼────────┤\n");
    printf("│ matrix[0][0]│ *(*(matrix + 0) + 0) │ %d     │\n", matrix[0][0]);
    printf("│ matrix[0][2]│ *(*(matrix + 0) + 2) │ %d     │\n", matrix[0][2]);
    printf("│ matrix[1][1]│ *(*(matrix + 1) + 1) │ %d     │\n", matrix[1][1]);
    printf("│ matrix[2][3]│ *(*(matrix + 2) + 3) │ %d    │\n", matrix[2][3]);
    printf("└─────────────┴──────────────────────┴────────┘\n");
    
    printf("\nKey Insight: matrix[i][j] == *(*(matrix + i) + j)\n");
}

// Demonstrate array vs pointer differences
void arrayPointerDifferences() {
    printSection("9. KEY DIFFERENCES - Array vs Pointer");
    
    int arr[5] = {10, 20, 30, 40, 50};
    int *ptr = arr;
    
    printf("┌──────────────────────────┬─────────────┬─────────────┐\n");
    printf("│ Aspect                   │ Array       │ Pointer     │\n");
    printf("├──────────────────────────┼─────────────┼─────────────┤\n");
    printf("│ Declaration              │ int arr[5]  │ int *ptr    │\n");
    printf("│ Memory Allocation        │ Automatic   │ Manual      │\n");
    printf("│ Size Known at Compile    │ Yes         │ No          │\n");
    printf("│ sizeof() Result          │ %zu bytes   │ %zu bytes   │\n", sizeof(arr), sizeof(ptr));
    printf("│ Can be Reassigned        │ No          │ Yes         │\n");
    printf("│ Holds                    │ Data        │ Address     │\n");
    printf("│ Increment (arr++/ptr++)  │ Invalid     │ Valid       │\n");
    printf("│ Access Syntax            │ arr[i]      │ *(ptr + i)  │\n");
    printf("└──────────────────────────┴─────────────┴─────────────┘\n");
    
    printf("\nDemonstration:\n");
    printf("arr = arr + 1;   // ❌ INVALID - array is not modifiable\n");
    printf("ptr = ptr + 1;   // ✓ VALID   - pointer can be modified\n");
    ptr = ptr + 1;
    printf("After ptr++: *ptr = %d (now points to second element)\n", *ptr);
}

// Demonstrate practical examples
void practicalExamples() {
    printSection("10. PRACTICAL EXAMPLES");
    
    printf("Example 1: String Traversal\n");
    printf("────────────────────────────\n");
    char str[] = "Hello";
    
    printf("Array method: ");
    for (int i = 0; str[i] != '\0'; i++) {
        printf("%c ", str[i]);
    }
    printf("\n");
    
    printf("Pointer method: ");
    for (char *p = str; *p != '\0'; p++) {
        printf("%c ", *p);
    }
    printf("\n\n");
    
    printf("Example 2: Sum of Array\n");
    printf("────────────────────────\n");
    int numbers[] = {5, 10, 15, 20, 25};
    int sum = 0;
    
    // Using pointers
    int *end = numbers + 5;
    for (int *p = numbers; p < end; p++) {
        sum += *p;
    }
    printf("Sum using pointer arithmetic: %d\n", sum);
    
    // Reset sum
    sum = 0;
    for (int i = 0; i < 5; i++) {
        sum += numbers[i];
    }
    printf("Sum using array indexing:     %d\n", sum);
}

int main() {
    printf("\n╔════════════════════════════════════════════════════════╗\n");
    printf("║                                                        ║\n");
    printf("║     ARRAY vs POINTER ARITHMETIC DEMONSTRATION          ║\n");
    printf("║            Comprehensive C Programming Guide           ║\n");
    printf("║                                                        ║\n");
    printf("╚════════════════════════════════════════════════════════╝\n");
    
    arrayBasics();
    pointerArithmetic();
    arrayPointerEquivalence();
    iterationComparison();
    pointerSubtraction();
    arrayDecay();
    pointerIncrementDecrement();
    multidimensionalArrays();
    arrayPointerDifferences();
    practicalExamples();
    
    printf("\n╔════════════════════════════════════════════════════════╗\n");
    printf("║                    KEY TAKEAWAYS                       ║\n");
    printf("╚════════════════════════════════════════════════════════╝\n\n");
    
    printf("1. arr[i] is equivalent to *(arr + i)\n");
    printf("2. Pointer arithmetic moves by sizeof(type), not 1 byte\n");
    printf("3. Arrays decay to pointers in most contexts\n");
    printf("4. Arrays have fixed size; pointers can be reassigned\n");
    printf("5. Pointer subtraction gives element count, not bytes\n");
    printf("6. Arrays are not modifiable lvalues; pointers are\n");
    printf("7. sizeof(array) gives total size; sizeof(pointer) gives pointer size\n");
    printf("8. Both can use [] notation, but they're fundamentally different\n");
    
    printf("\n✓ Demonstration complete!\n\n");
    
    return 0;
}
