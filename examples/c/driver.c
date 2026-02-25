#include <stdio.h>
#include <stdlib.h>
#include "linked_list.h"

void printMenu() {
    printf("\n");
    printf("========================================\n");
    printf("     Linked List Interactive Driver     \n");
    printf("========================================\n");
    printf("1.  Insert at End\n");
    printf("2.  Insert at Beginning\n");
    printf("3.  Delete Node\n");
    printf("4.  Display List\n");
    printf("5.  Search Element\n");
    printf("6.  Get List Length\n");
    printf("7.  Sort (Bubble Sort)\n");
    printf("8.  Sort (Merge Sort)\n");
    printf("9.  Reverse List\n");
    printf("10. Insert Array of Numbers\n");
    printf("11. Clear List\n");
    printf("0.  Exit\n");
    printf("========================================\n");
    printf("Enter your choice: ");
}

int main() {
    Node* list = NULL;
    int choice, value, pos;
    
    // Set line buffering for stdout to ensure output appears immediately
    setvbuf(stdout, NULL, _IOLBF, 0);
    
    printf("\n");
    printf("╔════════════════════════════════════════╗\n");
    printf("║  Welcome to Linked List Manager v1.0  ║\n");
    printf("╚════════════════════════════════════════╝\n");
    
    while (1) {
        printMenu();
        scanf("%d", &choice);
        
        switch (choice) {
            case 1:
                printf("Enter value to insert at end: ");
                scanf("%d", &value);
                list = insertEnd(list, value);
                printf("✓ Element %d inserted at end.\n", value);
                display(list, "Current List");
                break;
                
            case 2:
                printf("Enter value to insert at beginning: ");
                scanf("%d", &value);
                list = insertBegin(list, value);
                printf("✓ Element %d inserted at beginning.\n", value);
                display(list, "Current List");
                break;
                
            case 3:
                printf("Enter value to delete: ");
                scanf("%d", &value);
                list = deleteNode(list, value);
                display(list, "Current List");
                break;
                
            case 4:
                display(list, "Current List");
                break;
                
            case 5:
                printf("Enter value to search: ");
                scanf("%d", &value);
                pos = search(list, value);
                if (pos != -1) {
                    printf("✓ Element %d found at position %d (0-indexed)\n", value, pos);
                } else {
                    printf("✗ Element %d not found in the list.\n", value);
                }
                break;
                
            case 6: {
                int len = getListLength(list);
                printf("List length: %d\n", len);
                break;
            }
                
            case 7: {
                if (list == NULL) {
                    printf("✗ Cannot sort empty list!\n");
                    break;
                }
                // Create a copy for sorting
                Node* sortCopy = NULL;
                Node* temp = list;
                while (temp != NULL) {
                    sortCopy = insertEnd(sortCopy, temp->data);
                    temp = temp->next;
                }
                sortCopy = bubbleSort(sortCopy);
                display(sortCopy, "Sorted List (Bubble Sort)");
                freeList(sortCopy);
                break;
            }
                
            case 8: {
                if (list == NULL) {
                    printf("✗ Cannot sort empty list!\n");
                    break;
                }
                // Create a copy for sorting
                Node* sortCopy = NULL;
                Node* temp = list;
                while (temp != NULL) {
                    sortCopy = insertEnd(sortCopy, temp->data);
                    temp = temp->next;
                }
                sortCopy = mergeSort(sortCopy);
                display(sortCopy, "Sorted List (Merge Sort)");
                freeList(sortCopy);
                break;
            }
                
            case 9: {
                if (list == NULL) {
                    printf("✗ Cannot reverse empty list!\n");
                    break;
                }
                // Create a copy for reversing
                Node* reverseCopy = NULL;
                Node* temp = list;
                while (temp != NULL) {
                    reverseCopy = insertEnd(reverseCopy, temp->data);
                    temp = temp->next;
                }
                reverseCopy = reverseList(reverseCopy);
                display(reverseCopy, "Reversed List");
                freeList(reverseCopy);
                break;
            }
                
            case 10: {
                printf("Enter number of elements: ");
                int arraySize;
                scanf("%d", &arraySize);
                
                if (arraySize <= 0) {
                    printf("✗ Array size must be greater than 0!\n");
                    break;
                }
                
                int* array = (int*)malloc(arraySize * sizeof(int));
                if (array == NULL) {
                    printf("✗ Memory allocation failed!\n");
                    break;
                }
                
                printf("Enter %d numbers (separated by spaces or newlines):\n", arraySize);
                for (int i = 0; i < arraySize; i++) {
                    printf("  Element %d: ", i + 1);
                    scanf("%d", &array[i]);
                }
                
                list = insertArray(list, array, arraySize);
                display(list, "Updated List");
                free(array);
                break;
            }
                
            case 11:
                freeList(list);
                list = NULL;
                printf("✓ List cleared successfully!\n");
                break;
                
            case 0:
                printf("\nCleaning up and exiting...\n");
                freeList(list);
                printf("✓ Goodbye!\n\n");
                return EXIT_SUCCESS;
                
            default:
                printf("✗ Invalid choice! Please try again.\n");
        }
    }
    
    return EXIT_SUCCESS;
}
