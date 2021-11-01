import pytest

from test.VisitorSpec import createTree


class TestArraysSemanticSpec:

    @pytest.mark.skip()
    def test_thing(self, visitor_fixture):
        prog_test = createTree("""""")