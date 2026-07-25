#!/usr/bin/env python3
import os
import subprocess
from concurrent.futures import ProcessPoolExecutor

# run bash cmd
# os.system('ls -l')

# subprocess.run
# out = subprocess.run(['ls', '-l'], shell=True, text=True, capture_output=True)
# print(type(out))

# subprocess.Popen
# p = subprocess.Popen(['ls', '-l'], shell=True, text=True, stdout=subprocess.PIPE)
# for line in p.stdout:
#     print(line.strip())
# p.communicate()

# def heavy_task(x):
#     return x * x

# # try concurrent
# with ProcessPoolExecutor(max_workers=5) as executor:
#     futures = [executor.submit(heavy_task, i) for i in range(10)]
#     for future in futures:
#         print(future.result())

# read from specified location
test_file = '/home/zoe/AI/rag_poc/learning/python/decorator_test.py'
with open(test_file, "+r") as file:
    file.seek(10)
    file.readline()
    file_size = os.path.getsize(test_file)
    while file.tell() < file_size:
        print(file.readline().strip())