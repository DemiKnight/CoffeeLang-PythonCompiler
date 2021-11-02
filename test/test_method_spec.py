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
        assert len(visitor_fixture.trail.values()) == 20
        assert visitor_fixture.errors == [
            SemanticsError(2, "foo", ErrorType.EXPRESSION_USING_VOID_METHOD)
        ]

    @pytest.mark.skip
    def test_handle_function_missing_return(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        int foo() {}
        """)

    @pytest.mark.skip
    def test_handle_void_returning_value(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        void foo() {
            return 12;
        }
        """)

    @pytest.mark.skip
    def test_handle_main_return_type_mismatch_float(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        return 1.2;
        """)

    @pytest.mark.skip
    def test_handle_main_return_type_mismatch_bool(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        return true;
        """)

    @pytest.mark.skip
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

    @pytest.mark.skip
    def test_import_duplicate(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        import printf, printf;
        """)

    @pytest.mark.skip
    def test_import_usage(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        import printf;
        printf("hello")
        """)

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
        assert len(visitor_fixture.errors) == 0

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
