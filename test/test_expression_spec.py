from Utils import SemanticsError, ErrorType
from VisitorSpec import *


class TestExpressionSpec:

    def test_literal_int(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        return 2 + 2;
        """)

        expected_calls = defaultCalls + [
            TreeVisit("visitBlock", None),
            TreeVisit("visitReturn", None),
            TreeVisit('visit', 'int'),
            TreeVisit('visitExpr', 'int'),
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
        return 2.2 + 2.2;
        """)

        expected_calls = defaultCalls + [
            TreeVisit("visitBlock", None),
            TreeVisit("visitReturn", None),
            TreeVisit("visit", "float"),
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
        assert visitor_fixture.errors == [
            SemanticsError(1,"main", ErrorType.MAIN_METHOD_RETURN_TYPE_MISMATCH, type_mismatched="float")
        ]

    @pytest.mark.skip("Need to implement boolean logic.")
    def test_literal_bool(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        return True && False;
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
            TreeVisit("visit", "int"),
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
            TreeVisit("visit", "int"),
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
        return 2 + 3.3;
        """)

        expected_calls = defaultCalls + [
            TreeVisit("visitBlock", None),
            TreeVisit("visitReturn", None),
            TreeVisit("visit", "float"),
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
        assert visitor_fixture.errors == [
            SemanticsError(1, "main", ErrorType.MAIN_METHOD_RETURN_TYPE_MISMATCH, type_mismatched="float")
        ]

    def test_order_precedence_bool_int(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        return 2 + true;
        """)

        expected_calls = defaultCalls + [
            TreeVisit("visitBlock", None),
            TreeVisit("visitReturn", None),
            TreeVisit("visit", "int"),
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
        assert visitor_fixture.errors == []

    def test_order_precedence_bool_float(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        return 2.2 + true;
        """)

        expected_calls = defaultCalls + [
            TreeVisit("visitBlock", None),
            TreeVisit("visitReturn", None),
            TreeVisit("visit", "float"),
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
        assert visitor_fixture.errors == [
            SemanticsError(1, "main", ErrorType.MAIN_METHOD_RETURN_TYPE_MISMATCH, type_mismatched="float")
        ]

    def test_logical_not(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        bool a = !true
        """)

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert len(visitor_fixture.trail.values()) == 8
        assert visitor_fixture.errors == []

    def test_handle_logical_not_type_mismatch(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        bool a = !-1;
        """)

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert len(visitor_fixture.trail.values()) == 9
        assert visitor_fixture.errors == [
            SemanticsError(1, "", ErrorType.EXPRESSION_CONDITION_TYPE_MISMATCH_NOT,type_mismatched="int", type_required="bool"),
            SemanticsError(1, "a", ErrorType.VAR_ASSIGN_TYPE_MISMATCH, "int", "bool")
        ]
