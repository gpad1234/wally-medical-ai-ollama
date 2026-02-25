#include <stdio.h>
#include <stdlib.h>
#include "doubly_linked_list.h"

void printHeader() {
    printf("\n╔════════════════════════════════════════════╗\n");
    printf("║  Doubly Linked List Manager v1.0          ║\n");
    printf("╚════════════════════════════════════════════╝\n\n");
}

void printMenu() {
    printf("============================================\n");
    printf("   Doubly Linked List Interactive Driver   \n");
    printf("============================================\n");
    printf("1.  Insert at End\n");
    printf("2.  Insert at Beginning\n");
    printf("3.  Insert After Value\n");
    printf("4.  Insert Before Value\n");
    printf("5.  Delete Node\n");
    printf("6.  Display List (Forward)\n");
    printf("7.  Display List (Backward)\n");
    printf("8.  Search Element\n");
    printf("9.  Get List Length\n");
    printf("10. Sort (Bubble Sort)\n");
    printf("11. Sort (Merge Sort)\n");
    printf("12. Reverse List\n");
    printf("13. Insert Array of Numbers\n");
    printf("14. Clear List\n");
    printf("0.  Exit\n");
    printf("============================================\n");
}

int main() {
    DNode* head = NULL;
    int choice, value, afterValue, beforeValue;
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
                head = insertDEnd(head, value);
                printf("✓ Value %d inserted at end.\n", value);
                displayDForward(head, "Updated List: ");
                break;
                
            case 2: // Insert at Beginning
                printf("Enter value to insert: ");
                scanf("%d", &value);
                head = insertDBegin(head, value);
                printf("✓ Value %d inserted at beginning.\n", value);
                displayDForward(head, "Updated List: ");
                break;
                
            case 3: // Insert After Value
                printf("Enter value after which to insert: ");
                scanf("%d", &afterValue);
                printf("Enter value to insert: ");
                scanf("%d", &value);
                head = insertDAfter(head, afterValue, value);
                displayDForward(head, "Updated List: ");
                break;
                
            case 4: // Insert Before Value
                printf("Enter value before which to insert: ");
                scanf("%d", &beforeValue);
                printf("Enter value to insert: ");
                scanf("%d", &value);
                head = insertDBefore(head, beforeValue, value);
                displayDForward(head, "Updated List: ");
                break;
                
            case 5: // Delete Node
                if (head == NULL) {
                    printf("✗ List is empty. Nothing to delete.\n");
                } else {
                    printf("Enter value to delete: ");
                    scanf("%d", &value);
                    head = deleteDNode(head, value);
                    printf("✓ Element %d deleted successfully.\n", value);
                    displayDForward(head, "Updated List: ");
                }
                break;
                
            case 6: // Display Forward
                displayDForward(head, "List (Forward): ");
                break;
                
            case 7: // Display Backward
                displayDBackward(head, "List (Backward): ");
                break;
                
            case 8: // Search Element
                if (head == NULL) {
                    printf("✗ List is empty.\n");
                } else {
                    printf("Enter value to search: ");
                    scanf("%d", &value);
                    position = searchD(head, value);
                    if (position != -1) {
                        printf("✓ Element %d found at position %d (0-indexed).\n", value, position);
                    } else {
                        printf("✗ Element %d not found in the list.\n", value);
                    }
                }
                break;
                
            case 9: // Get List Length
                printf("List Length: %d\n", getDListLength(head));
                break;
                
            case 10: // Bubble Sort
                if (head == NULL) {
                    printf("✗ List is empty. Nothing to sort.\n");
                } else {
                    displayDForward(head, "Before sorting: ");
                    head = bubbleSortD(head);
                    printf("✓ List sorted using Bubble Sort.\n");
                    displayDForward(head, "After sorting: ");
                }
                break;
                
            case 11: // Merge Sort
                if (head == NULL) {
                    printf("✗ List is empty. Nothing to sort.\n");
                } else {
                    displayDForward(head, "Before sorting: ");
                    head = mergeSortD(head);
                    printf("✓ List sorted using Merge Sort.\n");
                    displayDForward(head, "After sorting: ");
                }
                break;
                
            case 12: // Reverse List
                if (head == NULL) {
                    printf("✗ List is empty. Nothing to reverse.\n");
                } else {
                    displayDForward(head, "Before reversing: ");
                    head = reverseDList(head);
                    printf("✓ List reversed successfully.\n");
                    displayDForward(head, "After reversing: ");
                }
                break;
                
            case 13: // Insert Array
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
                    
                    head = insertDArray(head, arr, n);
                    printf("✓ Inserted %d elements from array.\n", n);
                    displayDForward(head, "Updated List: ");
                    
                    free(arr);
                }
                break;
                
            case 14: // Clear List
                if (head == NULL) {
                    printf("✗ List is already empty.\n");
                } else {
                    freeDList(head);
                    head = NULL;
                    printf("✓ List cleared successfully.\n");
                }
                break;
                
            case 0: // Exit
                printf("\nCleaning up and exiting...\n");
                freeDList(head);
                printf("✓ Goodbye!\n");
                return 0;
                
            default:
                printf("✗ Invalid choice. Please try again.\n");
        }
    }
    
    return 0;
}
