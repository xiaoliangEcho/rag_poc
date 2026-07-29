#!/usr/bin/env python3
import os
import os
import pytest

@pytest.fixture(scope="class")
def files_in_current_dir():
    print("\n\nfiles_in_current_dir fixture started!")
    yield os.walk('./')
    print("\nfiles_in_current_dir fixture cleanup!")

