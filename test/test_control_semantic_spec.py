import pytest

from test.VisitorSpec import VisitorSpec, createTree


class TestControlSemanticSpec(VisitorSpec):

    @pytest.mark.skip(reason="TODO")
    def test_control(self):
        test_prog = createTree("""""")