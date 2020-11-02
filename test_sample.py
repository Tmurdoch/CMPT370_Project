
import pytest
# CMPT 370
# Group 4, Fall 2020


def add_two(x):
    return x + 2


def equals(x, y):
    if x == y:
        return True
    else:
        return False


def test_fail():

    # fail the test
    assert equals(3, 4)


def test_pass():

    # pass the test
    assert add_two(1) == 3
    assert equals(2, 2)
