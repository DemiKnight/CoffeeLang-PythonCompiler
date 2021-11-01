import pytest
from VisitorSpec import VisitorSpec, createTree
from TestUtilities import TreeVisit


class TestVariableSpec(VisitorSpec):

    @pytest.mark.skip()
    def test_declaration(self):
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

    @pytest.mark.skip()
    def test_block_declaration(self):
        test_prog = createTree("""
        int op = 55;
        {
            int xx = 22;
        }
        """)

    @pytest.mark.skip()
    def test_usage(self):
        # Given
        test_prog = createTree("""
        int x = 12;
        int z = x;
        """)

    @pytest.mark.skip()
    def test_handle_existing_variable_name(self):
        test_prog = createTree("""
        int x = 12;
        int x = 25;
        """)

    def test_block_scope_declaration(self):
        # Given
        test_prog = createTree("""
        int x = 22;
        {
            int x = 5;
        }
        """)

        expected_calls = self.defaultCalls + [
            TreeVisit("visitBlock", None),
            TreeVisit("visitGlobal_decl", None),
            TreeVisit("visitVar_decl", None),
            TreeVisit("visitData_type", "float"),
            TreeVisit("visitVar_assign", None),
            TreeVisit("visitVar", None),
            TreeVisit("visitExpr", None),
        ]

        # when
        self.target.visit(test_prog)

        print(self.target.places)

        # then
        assert expected_calls == self.target.places


