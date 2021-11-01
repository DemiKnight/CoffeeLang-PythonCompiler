import pytest

from test.VisitorSpec import createTree


class TestControlSemanticSpec:

    @pytest.mark.skip()
    def test_control(self, visitor_fixture):
        test_prog = createTree("""""")