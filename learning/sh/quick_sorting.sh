#!/usr/bin/env bash

# 在 Bash 中，函数参数是按值传递（Pass by Value）的，而不是按引用传递。
# 这意味着当你调用 quick_sorting "${numbers[@]}" ... 时，
# Bash 会把当前 numbers 数组的所有元素复制一份传给函数内部的 all_parameters。
# 因此，你在函数内部对 numbers 数组进行的任何修改（比如 numbers[$left]=${numbers[$right]}），
# 都只作用于全局的那个 numbers 数组，而函数内部用来做逻辑判断的 left 和 right 索引，
# 以及递归调用时传入的数组快照，并没有同步更新。这会导致递归的边界条件永远无法正确收敛，从而陷入死循环。

# 另外，每次递归的left是可变的，不是一直是第一个，right也是可变的，不是一直是最后一个
# 所以要保留本次调用时的left和right，而移动临时的left和right

quick_sorting() {
    
    local left=$1
    local right=$2
    local old_left=$left
    local old_right=$right


    # array update value
    # all_parameters[-1]=10
    
    # finish condition
    if [ $left -ge $right ]
    then
        echo "sorting done"
        return
    fi
    pivot="${numbers[$left]}"
    while [[ $left -lt $right ]]
    do
        while [[ $left -lt $right ]] && [[ ${numbers[$right]} -gt $pivot ]]
        do
            right=$((right-1))
        done
        numbers[$left]=${numbers[$right]}
        if [[ $left -lt $right ]]
        then
            left=$((left+1))
        fi

        while [[ $left -lt $right ]] && [[ ${numbers[$left]} -lt $pivot ]]
        do
            left=$((left+1))
        done
        numbers[$right]=${numbers[$left]}
        if [[ $left -lt $right ]]
        then
            right=$((right-1))
        fi
    done

    numbers[$left]=$pivot
    # echo "after: left $left and rignt $right"

    quick_sorting  $old_left $((left-1))
    quick_sorting  $((left+1)) $old_right
}

numbers=(
    5
    2
    8
    4
    7
    1
    9
    3
    10
    6
    )
# array append value
# numbers+=(7)
len=${#numbers[@]}
echo "original:"
for num in "${numbers[@]}"
do
    echo -n "$num "
done
echo
quick_sorting 0 $((len-1))
echo
echo "after sort:"
for num in "${numbers[@]}"
do
    echo -n "$num "
done
echo