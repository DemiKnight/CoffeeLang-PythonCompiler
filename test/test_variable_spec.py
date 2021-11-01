from Utils import SemanticsError, ErrorType
from VisitorSpec import *
from TestUtilities import TreeVisit, trail_values
from semantics import CoffeeTreeVisitor


class TestVariableSpec:

    def test_declaration(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        int prog = 12;
        """)

        expected_calls = defaultCalls + [
            TreeVisit("visitGlobal_decl", None)
        ]

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert trail_values(visitor_fixture.trail) == expected_calls
        assert len(visitor_fixture.errors) == 0

    @pytest.mark.skip
    def test_usage(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        int x = 12;
        int z = x;
        """)

        expected_calls = defaultCalls + [
            TreeVisit("visitGlobal_decl", None),
            TreeVisit("visitExpr", None),
            TreeVisit("visitGlobal_decl", None),
            TreeVisit("visitExpr", None),
        ]

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert trail_values(visitor_fixture.trail) == expected_calls
        assert len(visitor_fixture.errors) == 0

    def test_handle_existing_variable_name_global(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        int x = 12;
        int x = 25;
        """)

        expected_calls = defaultCalls + [
            TreeVisit("visitGlobal_decl", None),
            TreeVisit("visitGlobal_decl", None)
        ]

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert trail_values(visitor_fixture.trail) == expected_calls
        assert visitor_fixture.errors == [
            SemanticsError(2, "x", ErrorType.VAR_ALREADY_DEFINED)
        ]

    def test_handle_existing_variable_name_local(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        {
            int x = 12;
            int x = 25;
        }
        """)

        expected_calls = defaultCalls + [
            TreeVisit("visitBlock", None),
            TreeVisit("visitVar_decl", None),
            TreeVisit("visitVar_decl", None)
        ]

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert trail_values(visitor_fixture.trail) == expected_calls
        assert visitor_fixture.errors == [
            SemanticsError(3, "x", ErrorType.VAR_ALREADY_DEFINED)
        ]

    def test_block_scope_declaration(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        int x = 22;
        {
            int x = 5;
        }
        """)

        expected_calls = defaultCalls + [
            TreeVisit("visitGlobal_decl", None),
            TreeVisit("visitBlock", None),
            TreeVisit("visitVar_decl", None)
        ]

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert trail_values(visitor_fixture.trail) == expected_calls
        assert len(visitor_fixture.errors) == 0
