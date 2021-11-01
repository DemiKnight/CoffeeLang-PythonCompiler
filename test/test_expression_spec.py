from Utils import SemanticsError, ErrorType
from VisitorSpec import *


class TestExpressionSpec:

    # @pytest.mark.skip
    def test_literal_int(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        return 2 + 2;
        """)

        expected_calls = defaultCalls + [
            TreeVisit("visitBlock", None),
            TreeVisit("visitReturn", None),
            TreeVisit("visitExpr", "int"),
            TreeVisit('visit', 'int'),
            TreeVisit("visitExpr", "int"),
            TreeVisit("visit", "int"),
            TreeVisit("visitLiteral", "int"),
            TreeVisit('visit', 'int'),
            TreeVisit("visitExpr", "int"),
            TreeVisit("visit", "int"),
            TreeVisit("visitLiteral", "int"),
        ]

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert list(visitor_fixture.trail.values()) == expected_calls
        assert len(visitor_fixture.errors) == 0

    def test_literal_float(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        {
            return 2.2 + 2.2;
        }
        """)

        expected_calls = defaultCalls + [
            TreeVisit("visitBlock", None),
            TreeVisit("visitBlock", None),
            TreeVisit("visitReturn", None),
            TreeVisit("visitExpr", "float"),
            TreeVisit("visit", "float"),
            TreeVisit("visitExpr", "float"),
            TreeVisit("visit", "float"),
            TreeVisit("visitLiteral", "float"),
            TreeVisit("visit", "float"),
            TreeVisit("visitExpr", "float"),
            TreeVisit("visit", "float"),
            TreeVisit("visitLiteral", "float"),
        ]

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert list(visitor_fixture.trail.values()) == expected_calls
        assert len(visitor_fixture.errors) == 0

    @pytest.mark.skip("Need to implement boolean logic.")
    def test_literal_bool(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        {
            return True && False;
        }
        """)

        expected_calls = defaultCalls + [
            TreeVisit("visitBlock", None),
            TreeVisit("visitBlock", None),
            TreeVisit("visitReturn", None),
            TreeVisit("visitExpr", "float"),
            TreeVisit("visitExpr", "float"),
            TreeVisit("visit", "float"),
            TreeVisit("visitLiteral", "float"),
            TreeVisit("visitExpr", "float"),
            TreeVisit("visit", "float"),
            TreeVisit("visitLiteral", "float"),
        ]

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert list(visitor_fixture.trail.values()) == expected_calls
        assert len(visitor_fixture.errors) == 0

    def test_location(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        int a = 2;
        return a + 2;
        """)

        expected_calls = defaultCalls + [
            TreeVisit("visitGlobal_decl", None),
            TreeVisit("visit", "int"),
            TreeVisit("visitExpr", "int"),
            TreeVisit("visit", "int"),
            TreeVisit("visitLiteral", "int"),
            TreeVisit("visitBlock", None),
            TreeVisit("visitReturn", None),
            TreeVisit("visitExpr", "int"),
            TreeVisit("visit", "int"),
            TreeVisit("visitExpr", "int"),
            TreeVisit("visit", "int"),
            TreeVisit("visitLocation", "int"),
            TreeVisit("visit", "int"),
            TreeVisit("visitExpr", "int"),
            TreeVisit("visit", "int"),
            TreeVisit("visitLiteral", "int"),
        ]

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert list(visitor_fixture.trail.values()) == expected_calls
        assert len(visitor_fixture.errors) == 0

    def test_location_undefined_var(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        return a + 2;
        """)
        expected_calls = defaultCalls + [
            TreeVisit("visitBlock", None),
            TreeVisit('visitReturn', None),
            TreeVisit("visitExpr", "int"),
            TreeVisit("visit", None),
            TreeVisit("visitExpr", None),
            TreeVisit("visit", None),
            TreeVisit("visitLocation", None),
            TreeVisit("visit", "int"),
            TreeVisit("visitExpr", "int"),
            TreeVisit("visit", "int"),
            TreeVisit("visitLiteral", "int"),
        ]

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert list(visitor_fixture.trail.values()) == expected_calls
        assert visitor_fixture.errors == [
            SemanticsError(1, "a", ErrorType.VAR_NOT_FOUND)
        ]

    def test_order_precedence_float_int(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        {
            return 2 + 3.3;
        }
        """)

        expected_calls = defaultCalls + [
            TreeVisit("visitBlock", None),
            TreeVisit("visitBlock", None),
            TreeVisit("visitReturn", None),
            TreeVisit("visitExpr", "float"),
            TreeVisit("visit", "int"),
            TreeVisit("visitExpr", "int"),
            TreeVisit("visit", "int"),
            TreeVisit("visitLiteral", "int"),
            TreeVisit("visit", "float"),
            TreeVisit("visitExpr", "float"),
            TreeVisit("visit", "float"),
            TreeVisit("visitLiteral", "float"),
        ]

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert list(visitor_fixture.trail.values()) == expected_calls
        assert len(visitor_fixture.errors) == 0

    def test_order_precedence_bool_int(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        {
            return 2 + true;
        }
        """)

        # TODO Print error
        expected_calls = defaultCalls + [
            TreeVisit("visitBlock", None),
            TreeVisit("visitBlock", None),
            TreeVisit("visitReturn", None),
            TreeVisit("visitExpr", "int"),
            TreeVisit("visit", "int"),
            TreeVisit("visitExpr", "int"),
            TreeVisit("visit", "int"),
            TreeVisit("visitLiteral", "int"),
            TreeVisit("visit", "bool"),
            TreeVisit("visitExpr", "bool"),
            TreeVisit("visit", "bool"),
            TreeVisit("visitLiteral", "bool"),
        ]

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert list(visitor_fixture.trail.values()) == expected_calls
        assert len(visitor_fixture.errors) == 0

    def test_order_precedence_bool_float(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        {
            return 2.2 + true;
        }
        """)

        # TODO Print error
        expected_calls = defaultCalls + [
            TreeVisit("visitBlock", None),
            TreeVisit("visitBlock", None),
            TreeVisit("visitReturn", None),
            TreeVisit("visitExpr", "float"),
            TreeVisit("visit", "float"),
            TreeVisit("visitExpr", "float"),
            TreeVisit("visit", "float"),
            TreeVisit("visitLiteral", "float"),
            TreeVisit("visit", "bool"),
            TreeVisit("visitExpr", "bool"),
            TreeVisit("visit", "bool"),
            TreeVisit("visitLiteral", "bool"),
        ]

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert list(visitor_fixture.trail.values()) == expected_calls
        assert len(visitor_fixture.errors) == 0

    @pytest.mark.skip
    def test_data_type_returned(self, visitor_fixture):
        print()
