import pytest

from test.VisitorSpec import VisitorSpec, createTree


class TestArraysSemanticSpec(VisitorSpec):

    @pytest.mark.skip(reason="TODO")
    def test_thing(self):
        prog_test = createTree("""""")