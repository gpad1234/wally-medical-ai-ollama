#include <stdio.h>
#include <stdlib.h>

int main() {
    printf("Hello from C!\n");
    printf("Environment test successful.\n");
    
    int x = 42;
    int y = 8;
    
    printf("Simple calculation: %d + %d = %d\n", x, y, x + y);
    printf("Simple calculation: %d * %d = %d\n", x, y, x * y);
    
    return EXIT_SUCCESS;
}
