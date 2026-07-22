#！/usr/bin/env python3
import time

def measure_time(function):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        print(f"[{function.__name__ }] executed in {end-start:.4f} seconds")
        return result
    return wrapper

@measure_time
def dummy_test_case():
    time.sleep(1)
    print("test case running...")

dummy_test_case()