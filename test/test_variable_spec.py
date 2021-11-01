import unittest
import pytest
from VisitorSpec import VisitorSpec, createTree
from TestUtilities import TreeVisit


class TestVariableSpec(VisitorSpec):

    @pytest.mark.skip(reason="TODO")
    def test_something2(self):
        # self.ignoreTest(VariableSpec.test_something2)
        # Given
        test_prog = createTree("""
        int prog = 12;
        """)

        expected_calls = self.defaultCalls + [
            # TreeVisit("visitMe", None)
        ]
        # when
        self.target.visit(test_prog)

        # then
        self.assertListEqual(self.defaultCalls, expected_calls)


if __name__ == '__main__':
    unittest.main()
