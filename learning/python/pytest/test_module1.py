#!/usr/bin/env python3

import os

class TestClass1():

    def setup_method(self):
        print('\ntest setup\n')

    def test_case1(self, files_in_current_dir):
        for root, dir, files in files_in_current_dir:
            print(f"root {root}")
            print(f"dirs {dir}")
            print(f"files {files}")

    def teardown_method(self):
        print("\n\ntest teardown")

