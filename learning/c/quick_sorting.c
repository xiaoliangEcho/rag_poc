#include <stdio.h>

void quick_sort(int array[], int left, int right) {
    // set finish condition
    if(left >= right) {
        printf("sorting done: %d %d \n", left, right);
        return;
    }
    int initial_left = left;
    int initial_right = right;

    //set pivot
    int pivot = array[left];

    //main loop
    while(left < right) {
        //find the fisrt one which is smaller than pivot from right
        while(left < right && array[right] > pivot) {
            right-=1;
        }
        if(left < right) {
            array[left] = array[right];
            left+=1;
        }

        //find the fisrt one which is larger than pivot from left
        while(left < right && array[left] < pivot) {
            left+=1;
        }
        if(left < right) {
            array[right] = array[left];
            right-=1;
        }
    } // main loop done

    // after main loop
    // put the pivot to correct position
    array[left] = pivot;

    //recusive
    quick_sort(array, initial_left, left-1);
    quick_sort(array, left+1, initial_right);
}

int main() {
    int numbers[] = {5, 2, 8, 4, 7, 1, 9, 3, 10, 6};
    printf("The original list:\n");
    int len = sizeof(numbers) / sizeof(numbers[0]);
    for (int i=0; i<len; i++) {
        printf("%d ", numbers[i]);
    }
    printf("\n");
    quick_sort(numbers, 0, len-1);

    printf("\nThe sorted list:\n");
    for (int i=0; i<len; i++) {
        printf("%d ", numbers[i]);
    }
    printf("\n");
    return 0;   
}
