import pytest

from Utils import SemanticsError, ErrorType
from VisitorSpec import *


class TestMethodSpec:
    def test_handle_missing_declaration(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        void foo(int a) {}
        food(2);
        """)

        expected_calls = defaultCalls + [
            TreeVisit("visitMethod_decl", None),
            TreeVisit("visitMethod_call", None)
        ]

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert len(visitor_fixture.trail.values()) == 8
        assert visitor_fixture.errors == [
            SemanticsError(2, "food", ErrorType.METHOD_NOT_FOUND)
        ]

    # @pytest.mark.skip
    def test_call_function(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        void foo(int a) {}
        foo(2);
        """)

        expected_calls = defaultCalls + [

        ]

        # When
        visitor_fixture.visit(test_prog)

        # Then

    def test_declare_empty_function(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        void foo(int a) {}
        """)

        expected_calls = defaultCalls + [
            TreeVisit("visitMethod_decl", None),
            TreeVisit("visit", None),
            TreeVisit("visitBlock", None),
        ]

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert list(visitor_fixture.trail.values()) == expected_calls
        assert len(visitor_fixture.errors) == 0

    def test_handle_too_many_parameters_at_call(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        void foo(int a) {}
        foo(12, 22);
        """)
        expected_calls = defaultCalls + []

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert len(visitor_fixture.trail.values()) == 16
        assert visitor_fixture.errors == [
            SemanticsError(2, "foo", ErrorType.METHOD_SIGNATURE_ARGUMENT_COUNT)
        ]

    def test_handle_too_few_many_parameters_call(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        void foo(int a, int b) {}
        foo(112);
        """)
        expected_calls = defaultCalls + []

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert len(visitor_fixture.trail.values()) == 12
        assert visitor_fixture.errors == [
            SemanticsError(2, "foo", ErrorType.METHOD_SIGNATURE_ARGUMENT_COUNT)
        ]

    def test_handle_parameters_type_mismatch(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        void foo(int a, int b) {}
        foo(112, true);
        """)
        expected_calls = defaultCalls + []

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert len(visitor_fixture.trail.values()) == 16
        assert visitor_fixture.errors == [
            SemanticsError(2, "foo", ErrorType.METHOD_SIGNATURE_TYPE_MISMATCH_PARAMETERS)
        ]

    def test_handle_void_func_in_expression(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        void foo(int a) {}
        return 2 + foo(12);
        """)
        expected_calls = defaultCalls + []

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert len(visitor_fixture.trail.values()) == 21
        assert visitor_fixture.errors == [
            SemanticsError(2, "foo", ErrorType.EXPRESSION_USING_VOID_METHOD)
        ]

    def test_method_call_in_expression(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        int foo() {return 2;}
        return 2 + foo();
        """)
        expected_calls = defaultCalls + []

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert len(visitor_fixture.trail.values()) == 23
        assert visitor_fixture.errors == []

    def test_function_with_return(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        int foo() {return 2;}
        """)

        # WHen
        visitor_fixture.visit(test_prog)

        # Then
        assert len(visitor_fixture.trail.values()) == 11
        assert len(visitor_fixture.errors) == 0

    def test_handle_function_missing_return(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        int foo() {}
        """)
        expected_calls = defaultCalls + []

        # When
        visitor_fixture.visit(test_prog)

        # Then
        print(visitor_fixture.trail.values())
        assert len(visitor_fixture.trail.values()) == 5
        assert visitor_fixture.errors == [
            SemanticsError(1, "foo", ErrorType.METHOD_MISSING_RETURN)
        ]

    def test_handle_void_returning_value(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        void foo() {
            return 12;
        }
        """)
        expected_calls = defaultCalls + []

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert len(visitor_fixture.trail.values()) == 11
        assert visitor_fixture.errors == [
            SemanticsError(2, "foo", ErrorType.METHOD_VOID_RETURNING_VALUE)
        ]

    def test_handle_main_return_type_mismatch_float(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        return 1.2;
        """)
        expected_calls = defaultCalls + []

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert len(visitor_fixture.trail.values()) == 8
        assert visitor_fixture.errors == [
            SemanticsError(1, "main", ErrorType.MAIN_METHOD_RETURN_TYPE_MISMATCH)
        ]

    def test_handle_main_return_type_mismatch_bool(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        return true;
        """)

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert len(visitor_fixture.trail.values()) == 8
        assert visitor_fixture.errors == [
            SemanticsError(1, "main", ErrorType.MAIN_METHOD_RETURN_TYPE_MISMATCH)
        ]

    def test_parameter_usage(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        int foo(int a) {
            return 2 + a;
        }
        """)

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert len(visitor_fixture.trail.values()) == 17
        assert visitor_fixture.errors == []

    def test_non_exhaustive_return(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        int foo(bool value) {
            if(value) {
                return 12;
            } else {
            
            }
        }
        """)

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert len(visitor_fixture.trail.values()) == 22
        assert visitor_fixture.errors == [
            SemanticsError(1, "foo", ErrorType.METHOD_MISSING_RETURN_NON_EXHAUSTIVE)
        ]

    def test_import_duplicate(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        import printf, printf;
        """)
        expected_calls = defaultCalls + []

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert len(visitor_fixture.trail.values()) == 3
        assert visitor_fixture.errors == [
            SemanticsError(1, "printf", ErrorType.IMPORT_DUPLICATE)
        ]

    def test_import_usage(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        import printf;
        printf("hello");
        """)
        expected_calls = defaultCalls + []

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert len(visitor_fixture.trail.values()) == 6
        assert visitor_fixture.errors == []

    @pytest.mark.skip
    def test_declare_basic_func(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        int foo(int a) {
            return a + a;
        }
        """)

        expected_calls = defaultCalls + [

        ]

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert list(visitor_fixture.trail.values()) == expected_calls
        assert visitor_fixture.errors == []

    @pytest.mark.skip
    def test_handle_clashing_parameter_ids(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        int foo(int a, int a) {
            return a + a;
        }
        """)

        expected_calls = defaultCalls + [

        ]

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert list(visitor_fixture.trail.values()) == expected_calls
        assert visitor_fixture.errors == [
            SemanticsError(1, "a", ErrorType.VAR_PARAM_ALREADY_DEFINED)
        ]

    @pytest.mark.skip
    def test_handle_clashing_parameter_ids_types(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        int foo(int a, float a) {
            return a + a;
        }
        """)

        expected_calls = defaultCalls + [

        ]

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert list(visitor_fixture.trail.values()) == expected_calls
        assert visitor_fixture.errors == [
            SemanticsError(1, "a", ErrorType.VAR_PARAM_ALREADY_DEFINED)
        ]

    def test_handle_clashing_function_ids(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        void foo() {}
        void foo() {}
        """)

        expected_calls = defaultCalls + [
            TreeVisit("visitMethod_decl", None),
            TreeVisit("visit", None),
            TreeVisit("visitBlock", None),
            TreeVisit("visitMethod_decl", None)
        ]

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert list(visitor_fixture.trail.values()) == expected_calls
        assert visitor_fixture.errors == [
            SemanticsError(2, "foo", ErrorType.METHOD_ALREADY_DEFINED)
        ]
