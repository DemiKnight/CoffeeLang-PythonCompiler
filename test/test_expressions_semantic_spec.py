import pytest

from test.VisitorSpec import VisitorSpec, createTree

class TestExpressionsSemanticSpec(VisitorSpec):

    @pytest.mark.skip()
    def test_expressions(self):
        test_prog = createTree("""""")