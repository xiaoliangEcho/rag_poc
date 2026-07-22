#!/usr/bin/env bash

while true
do

IFS=' ' read -r -a numbers -p "input numbers: "
#numbers=(5 6 3)

# specify the left and right range of the array
quick_sort() {
	local original_left=$1
	local original_right=$2
	local left=$1
	local right=$2
	# exit conditio
	echo "debug left $left and right $right"
	if [ $left -ge $right ]
	then
		echo "sort completed!"
		return
	fi

	# set the first one as pivot
	pivot=${numbers[$left]}

	# main loop
	while [ $left -lt $right ]
	do
		# find the one which is smaller then pivot from right to left
		while [ $left -lt $right ] && [ ${numbers[$right]} -gt $pivot ]
		do
			right=$((right-1))
		done	
		if [ $left -lt $right ]
		then
			numbers[$left]=${numbers[$right]}
			left=$((left+1))
		fi
		# find the one which is larger then pivot from left to right
		while [ $left -lt $right ] && [ ${numbers[$left]} -lt $pivot ]
		do
			left=$((left+1))
		done	
		if [ $left -lt $right ]
		then
			numbers[$right]=${numbers[$left]}
			right=$((right-1))
		fi
	done
	# put the pivot to the correct location and recusive call
	numbers[$left]=$pivot	
	# do the left and right part recursively
	quick_sort $original_left  $((left-1))
	quick_sort $((left+1)) $original_right

}
num=${#numbers[@]}
echo "${numbers[@]}"
quick_sort 0 $((num-1))
echo "${numbers[@]}"

done
