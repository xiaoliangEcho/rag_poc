#!/usr/bin/env python3

input_list = [5, 2, 8, 4, 7, 1, 9, 3, 10, 6]

def quick_sort(left=0, right=0):
    initial_left  = left
    initial_right = right

    # finish condition
    if initial_left >= initial_right:
        print("sorting done")
        return
    
    # set pivot
    pivot = input_list[left]

    # main loop
    while left < right:
        # find the one which is smaller than piovt from right to left
        while left < right and input_list[right] > pivot:
            right-=1
        # either a bigger one found or left==right
        if left < right:
            input_list[left] = input_list[right]
            left+=1
        
        # find the one which is bigger than piovt from left to right
        while left < right and input_list[left] < pivot:
            left+=1
        # either a smaller one found or left==right
        if left < right:
            input_list[right] = input_list[left]
            right-=1
        
    # put the pivot to the correct location
    input_list[left] = pivot

    
    # recursive
    # sort the left part
    quick_sort(initial_left, left-1)
    # sort the right part
    quick_sort(left+1, initial_right)

print("The original list:")
print(input_list)

quick_sort(0, len(input_list)-1)

print("\nThe sorted list:")
print(input_list)

    
