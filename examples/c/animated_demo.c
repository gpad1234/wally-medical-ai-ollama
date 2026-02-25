#include <stdio.h>
#include <stdlib.h>
#include "linked_list.h"
#include "animation.h"

void clearScreen() {
    printf("\033[2J\033[H");
}

void printHeader() {
    printf("\n");
    printf("%s", BOLD);
    printf("╔════════════════════════════════════════════════════════╗\n");
    printf("║     Animated Linked List Visualization Demo           ║\n");
    printf("╚════════════════════════════════════════════════════════╝\n");
    printf("%s\n", RESET);
}

int main() {
    Node* list = NULL;
    
    // Set line buffering
    setvbuf(stdout, NULL, _IOLBF, 0);
    
    printHeader();
    
    printf("%sDemo: Building a linked list with animations%s\n\n", CYAN, RESET);
    sleep_ms(1000);
    
    // Step 1: Insert elements
    printf("%s━━━━━ STEP 1: Inserting Elements ━━━━━%s\n", BOLD, RESET);
    sleep_ms(800);
    
    animateInsert(list, 45, "end");
    list = insertEnd(list, 45);
    animateDisplay(list, "After insert 1");
    sleep_ms(500);
    
    animateInsert(list, 23, "end");
    list = insertEnd(list, 23);
    animateDisplay(list, "After insert 2");
    sleep_ms(500);
    
    animateInsert(list, 89, "end");
    list = insertEnd(list, 89);
    animateDisplay(list, "After insert 3");
    sleep_ms(500);
    
    animateInsert(list, 12, "end");
    list = insertEnd(list, 12);
    animateDisplay(list, "After insert 4");
    sleep_ms(500);
    
    animateInsert(list, 56, "end");
    list = insertEnd(list, 56);
    animateDisplay(list, "Current list");
    sleep_ms(1000);
    
    // Step 2: Search
    printf("\n%s━━━━━ STEP 2: Searching for Element ━━━━━%s\n", BOLD, RESET);
    sleep_ms(800);
    animateSearch(list, 89);
    sleep_ms(1000);
    
    // Step 3: Display with animation
    printf("\n%s━━━━━ STEP 3: Final List State ━━━━━%s\n", BOLD, RESET);
    sleep_ms(800);
    animateDisplay(list, "Final list");
    sleep_ms(1000);
    
    // Step 4: Bubble Sort
    printf("\n%s━━━━━ STEP 4: Sorting (Bubble Sort) ━━━━━%s\n", BOLD, RESET);
    sleep_ms(800);
    
    // Create copy for sorting
    Node* sortCopy = NULL;
    Node* temp = list;
    while (temp != NULL) {
        sortCopy = insertEnd(sortCopy, temp->data);
        temp = temp->next;
    }
    
    animateSort(sortCopy, "BUBBLE SORT");
    sortCopy = bubbleSort(sortCopy);
    animateDisplay(sortCopy, "Sorted result");
    sleep_ms(1000);
    freeList(sortCopy);
    
    // Step 5: Reverse
    printf("\n%s━━━━━ STEP 5: Reversing List ━━━━━%s\n", BOLD, RESET);
    sleep_ms(800);
    
    // Create copy for reversing
    Node* reverseCopy = NULL;
    temp = list;
    while (temp != NULL) {
        reverseCopy = insertEnd(reverseCopy, temp->data);
        temp = temp->next;
    }
    
    animateReverse(reverseCopy);
    reverseCopy = reverseList(reverseCopy);
    animateDisplay(reverseCopy, "Reversed result");
    sleep_ms(1000);
    freeList(reverseCopy);
    
    // Step 6: Delete
    printf("\n%s━━━━━ STEP 6: Deleting Element ━━━━━%s\n", BOLD, RESET);
    sleep_ms(800);
    animateDelete(list, 23);
    list = deleteNode(list, 23);
    animateDisplay(list, "After deletion");
    sleep_ms(1000);
    
    // Cleanup
    printf("\n%s━━━━━ DEMO COMPLETE ━━━━━%s\n", BOLD, RESET);
    printf("%s✓ All operations completed successfully!%s\n\n", GREEN, RESET);
    
    freeList(list);
    
    return EXIT_SUCCESS;
}
