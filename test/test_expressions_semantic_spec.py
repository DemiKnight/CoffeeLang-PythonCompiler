import pytest

from test.VisitorSpec import createTree


class TestExpressionsSemanticSpec:

    @pytest.mark.skip()
    def test_expressions(self, visitor_fixture):
        test_prog = createTree("""""")
