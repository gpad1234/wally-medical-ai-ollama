#include <stdio.h>
#include <stdlib.h>
#include "circular_linked_list.h"

void printHeader() {
    printf("\n╔════════════════════════════════════════════╗\n");
    printf("║  Circular Linked List Manager v1.0        ║\n");
    printf("╚════════════════════════════════════════════╝\n\n");
}

void printMenu() {
    printf("============================================\n");
    printf("  Circular Linked List Interactive Driver  \n");
    printf("============================================\n");
    printf("1.  Insert at End\n");
    printf("2.  Insert at Beginning\n");
    printf("3.  Insert After Value\n");
    printf("4.  Delete Node\n");
    printf("5.  Display List\n");
    printf("6.  Search Element\n");
    printf("7.  Get List Length\n");
    printf("8.  Sort (Bubble Sort)\n");
    printf("9.  Sort (Merge Sort)\n");
    printf("10. Reverse List\n");
    printf("11. Insert Array of Numbers\n");
    printf("12. Check if Circular\n");
    printf("13. Clear List\n");
    printf("0.  Exit\n");
    printf("============================================\n");
}

int main() {
    CNode* head = NULL;
    int choice, value, afterValue;
    int position;
    
    printHeader();
    
    while (1) {
        printMenu();
        printf("Enter your choice: ");
        
        if (scanf("%d", &choice) != 1) {
            printf("✗ Invalid input. Please enter a number.\n");
            while (getchar() != '\n'); // Clear input buffer
            continue;
        }
        
        switch (choice) {
            case 1: // Insert at End
                printf("Enter value to insert: ");
                scanf("%d", &value);
                head = insertCEnd(head, value);
                printf("✓ Value %d inserted at end.\n", value);
                displayCircular(head, "Updated List: ");
                break;
                
            case 2: // Insert at Beginning
                printf("Enter value to insert: ");
                scanf("%d", &value);
                head = insertCBegin(head, value);
                printf("✓ Value %d inserted at beginning.\n", value);
                displayCircular(head, "Updated List: ");
                break;
                
            case 3: // Insert After Value
                printf("Enter value after which to insert: ");
                scanf("%d", &afterValue);
                printf("Enter value to insert: ");
                scanf("%d", &value);
                head = insertCAfter(head, afterValue, value);
                displayCircular(head, "Updated List: ");
                break;
                
            case 4: // Delete Node
                if (head == NULL) {
                    printf("✗ List is empty. Nothing to delete.\n");
                } else {
                    printf("Enter value to delete: ");
                    scanf("%d", &value);
                    head = deleteCNode(head, value);
                    if (head != NULL || value == 0) { // Check if deletion was successful
                        printf("✓ Element %d deleted successfully.\n", value);
                    }
                    displayCircular(head, "Updated List: ");
                }
                break;
                
            case 5: // Display List
                displayCircular(head, "Circular List: ");
                if (head != NULL) {
                    printf("(List loops back: tail->next points to head %d)\n", head->data);
                }
                break;
                
            case 6: // Search Element
                if (head == NULL) {
                    printf("✗ List is empty.\n");
                } else {
                    printf("Enter value to search: ");
                    scanf("%d", &value);
                    position = searchC(head, value);
                    if (position != -1) {
                        printf("✓ Element %d found at position %d (0-indexed).\n", value, position);
                    } else {
                        printf("✗ Element %d not found in the list.\n", value);
                    }
                }
                break;
                
            case 7: // Get List Length
                printf("List Length: %d\n", getCListLength(head));
                break;
                
            case 8: // Bubble Sort
                if (head == NULL) {
                    printf("✗ List is empty. Nothing to sort.\n");
                } else {
                    displayCircular(head, "Before sorting: ");
                    head = bubbleSortC(head);
                    printf("✓ List sorted using Bubble Sort.\n");
                    displayCircular(head, "After sorting: ");
                }
                break;
                
            case 9: // Merge Sort
                if (head == NULL) {
                    printf("✗ List is empty. Nothing to sort.\n");
                } else {
                    displayCircular(head, "Before sorting: ");
                    head = mergeSortC(head);
                    printf("✓ List sorted using Merge Sort.\n");
                    displayCircular(head, "After sorting: ");
                }
                break;
                
            case 10: // Reverse List
                if (head == NULL) {
                    printf("✗ List is empty. Nothing to reverse.\n");
                } else {
                    displayCircular(head, "Before reversing: ");
                    head = reverseCList(head);
                    printf("✓ List reversed successfully.\n");
                    displayCircular(head, "After reversing: ");
                }
                break;
                
            case 11: // Insert Array
                {
                    int n;
                    printf("Enter number of elements: ");
                    scanf("%d", &n);
                    
                    if (n <= 0) {
                        printf("✗ Invalid number of elements.\n");
                        break;
                    }
                    
                    int* arr = (int*)malloc(n * sizeof(int));
                    if (arr == NULL) {
                        printf("✗ Memory allocation failed.\n");
                        break;
                    }
                    
                    printf("Enter %d numbers (separated by spaces or newlines):\n", n);
                    for (int i = 0; i < n; i++) {
                        printf("  Element %d: ", i + 1);
                        scanf("%d", &arr[i]);
                    }
                    
                    head = insertCArray(head, arr, n);
                    printf("✓ Inserted %d elements from array.\n", n);
                    displayCircular(head, "Updated List: ");
                    
                    free(arr);
                }
                break;
                
            case 12: // Check if Circular
                if (head == NULL) {
                    printf("List is empty.\n");
                } else {
                    if (isCircular(head)) {
                        printf("✓ List is CIRCULAR (tail->next points to head).\n");
                        CNode* tail = getTailC(head);
                        printf("  Head: %d, Tail: %d, Tail->next: %d\n", 
                               head->data, tail->data, tail->next->data);
                    } else {
                        printf("✗ List is NOT circular (broken structure).\n");
                    }
                }
                break;
                
            case 13: // Clear List
                if (head == NULL) {
                    printf("✗ List is already empty.\n");
                } else {
                    freeCList(head);
                    head = NULL;
                    printf("✓ List cleared successfully.\n");
                }
                break;
                
            case 0: // Exit
                printf("\nCleaning up and exiting...\n");
                freeCList(head);
                printf("✓ Goodbye!\n");
                return 0;
                
            default:
                printf("✗ Invalid choice. Please try again.\n");
        }
    }
    
    return 0;
}
