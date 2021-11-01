import pytest

def method():
    return 12

def test_thingy():
    assert method() == 12
