import pytest

from test.VisitorSpec import VisitorSpec, createTree

class TestExpressionsSemanticSpec(VisitorSpec):

    @pytest.mark.skip(reason="TODO")
    def test_expressions(self):
        test_prog = createTree("""""")