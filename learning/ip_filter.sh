# 题目名称
# Bash: IP Address Filtering（IP 地址过滤）
# 问题描述
# 需编写 Bash 脚本，根据给定的 IP 掩码模式，从日志条目中筛选出匹配的 IPv4 地址并返回。
# 输入格式
# 第一行：整数 num_logs（表示日志条目的数量）。
# 接下来 num_logs 行：每行是一条日志条目，格式为 日志类型 IP地址（例如 ALERT 192.168.36.3）。
# 最后一行：字符串 mask（用于匹配 IP 地址的模式，例如 192.168.*.*）。
# 输出格式
# 返回所有与 mask 模式匹配的 IPv4 地址列表（每个 IP 占一行）。
# 约束条件
# 单条日志条目长度不超过 100 字符。
# IP 地址遵循标准 IPv4 格式（如 x.x.x.x，其中 x 为数字）。
# 日志条目数量最多为 1000 条。


# 样例输入（Sample Input 0）
# 4
# ALERT 192.168.36.3
# DEBUG 191.169.78.3
# CONNECTION 10.0.0.1
# PING 192.168.1.1
# 192.168.*.*

# 样例输出（Sample Output 0）
# 192.168.36.3
# 192.168.1.1

# 样例解释
# 掩码 192.168.*.* 表示“前两段为 192.168，后两段任意”的 IP 模式。程序遍历所有日志，提取 IP 并与掩码匹配，最终返回符合条件的 IP 列表。

#!/usr/bin/env bash

#
# Complete the 'filter_logs' function below.
#
# The function is expected to return a STRING_ARRAY.
# The function accepts following parameters:
# 1. INTEGER num_logs
# 2. STRING_ARRAY logs
# 3. STRING mask
#

filter_logs() { 
    local num_logs=$1
    shift
    local all_remaining=("$@")
    local mask="${all_remaining[-1]}"
    unset 'all_remaining[-1]'
    local logs=("${all_remaining[@]}")
    num_filtered=0

    local new_mask=$(echo "$mask"|sed 's/\./\\./g; s/\*/[0-9]\+/g')
    # echo "new mask is $new_mask"

    for log in "${logs[@]}"
    do
        if [[ $num_filtered -le $num_logs ]]
        then
            ip_address=$(echo "$log"|awk '{print $2}')
            # 
            # 失败场景： 假设掩码是 192.168.1.*。
            # 你的代码会把掩码变成 192.168.1。
            # IP 192.168.10.5 也会被判定为匹配（因为它确实以 192.168.1 开头），但这是错误的。
            # 同理，掩码 10.* 会匹配到 100.0.0.1，这也是错的。
            # new_mask=$(echo $mask|sed "s/\.\*//g")
            # if [[ "$ip_address" = "$new_mask"* ]]

            # 在 Bash 的 [[ ... =~ ... ]] 结构中：
            # 不加引号：右侧会被解析为正则表达式。
            # 加双引号：右侧会被视为普通字符串（字面量）。
            if [[ "$ip_address" =~ ^$new_mask$ ]]
            then
                echo $ip_address
            fi
            num_filtered=$((num_filtered + 1))
        fi
    done

}
num_logs=4
logs=(
'ALERT 192.168.36.3'
'DEBUG 191.169.78.3'
'CONNECTION 10.0.0.1'
'PING 192.168.1.1'
)
mask='192.168.*.*'

# get customized input
# read num_logs
filter_logs $num_logs "${logs[@]}" $mask