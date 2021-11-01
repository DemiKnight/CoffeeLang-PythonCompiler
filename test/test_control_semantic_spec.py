import pytest

from test.VisitorSpec import VisitorSpec, createTree


class TestControlSemanticSpec(VisitorSpec):

    @pytest.mark.skip()
    def test_control(self):
        test_prog = createTree("""""")