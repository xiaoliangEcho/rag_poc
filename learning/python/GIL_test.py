#!/usr/bin/env python3

import threading
import multiprocessing
import time

def cpu_bound():
    count=0
    for _ in range(100000000):
        count += 1

# CPU 密集型任务：多线程反而可能更慢（因为线程切换和 GIL 争抢）
def threading_test():
    time_now = time.time()
    # print(f"current time is {time_now}")
    threads = [threading.Thread(target=cpu_bound) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(f"time consumed for threading test is {time.time()-time_now:.2f}")

# CPU 密集型任务：多进程能利用多核，绕过 GIL
def multiprocess_test():
    time_now = time.time()
    # print(f"current time is {time_now}")
    threads = [multiprocessing.Process(target=cpu_bound) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(f"time consumed for threading test is {time.time()-time_now:.2f}")

print("start test")
threading_test()
multiprocess_test()