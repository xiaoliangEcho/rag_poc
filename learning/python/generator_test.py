#!/usr/bin/env python3
import os

def read_large_file(filename=""):
    if filename and os.path.exists(filename):
        with open(filename, "+r") as file_handle:
            for line in file_handle:
                yield line.strip()
    else:
        print(f"file {filename} not found")

for line in read_large_file('/home/zoe/AI/rag_poc/learning/python/decorator_test.py'):
    print(line)