#!/usr/bin/env bash

read -r  -d '' -a array << EOF
8
127.0.0.1
128.1.2.3
127.0.0.4
2.3.4.5
5.6.7.8
127.0.*.*
EOF


ip_filter() {
	num_ip=$1
	shift
	all_parametrs_left=($@)
	filter=${all_parametrs_left[-1]}
	unset 'all_parametrs_left[-1]'
	
	# set regular expression
	reg_filter=$(echo $filter|sed 's/\./\\./g; s/\*/[0-9]+/g')

	for ip in "${all_parametrs_left[@]:0:$num_ip}"
	do
		if [[ $ip =~ $reg_filter ]]
		then
			echo $ip
		fi
	done
}

ip_filter "${array[@]}"
