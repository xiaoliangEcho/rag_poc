#include <iostream>
#include <vector>

// 在 C++ 中，可执行的语句（比如 std::cout << ...）必须放在函数内部，
// 不能直接写在文件的全局作用域里。你需要把它放进 main 函数中

void quick_sort(std::vector<int>& array, int left, int right) {
    // set finish condition
    if(left >= right) {
        std::cout << "sorting done: " << left << " " << right<< std::endl;
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

    // after mail loop
    // put the pivot to correct position
    array[left] = pivot;

    //recusive
    quick_sort(array, initial_left, left-1);
    quick_sort(array, left+1, initial_right);
}
int main() {
    std::vector<int> numbers = {5, 2, 8, 4, 7, 1, 9, 3, 10, 6};
    std::cout << "The original list:\n";
    for (int num : numbers) {
        std::cout << num << " ";
    }
    std::cout << std::endl;
    quick_sort(numbers, 0, numbers.size()-1);

    std::cout << "\nThe sorted list:\n";
    for (int num : numbers) {
        std::cout << num << " ";
    }
    std::cout << std::endl;
    return 0;   
}
