import pytest

from Utils import ErrorType, SemanticsError
from VisitorSpec import *


class TestControlSemanticSpec:

    def test_control(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        import printf, printf; 
        void foo(int x, int y) { 
            return 0; 
        } 
        int a = food(1, -2.0, 5);
        """)

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert len(visitor_fixture.trail.values()) == 17
        assert visitor_fixture.errors == [
            SemanticsError(1,"printf",ErrorType.IMPORT_DUPLICATE),
            SemanticsError(3,"foo", ErrorType.METHOD_VOID_RETURNING_VALUE),
            SemanticsError(5,"food",ErrorType.METHOD_NOT_FOUND),
        ]

    def test_expression(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        if (true && !1) { 
            return true; 
        }
        """)

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert len(visitor_fixture.trail.values()) == 23
        assert visitor_fixture.errors == [
            SemanticsError(1,"", ErrorType.EXPRESSION_CONDITION_TYPE_MISMATCH_NOT,type_mismatched="int", type_required="bool"),
            SemanticsError(1,"main",ErrorType.EXPRESSION_CONDITION_TYPE_MISMATCH),
            SemanticsError(2,"main", ErrorType.MAIN_METHOD_RETURN_TYPE_MISMATCH, type_mismatched="bool")
        ]
