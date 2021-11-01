from Utils import SemanticsError, ErrorType
from VisitorSpec import *


class TestMethodSpec:
    @pytest.mark.skip
    def test_declare_empty_function(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        void foo() {
            
        }
        foo();
        """)

        expected_calls = defaultCalls + [
            TreeVisit("visitMethod_decl", None),
            TreeVisit("visitReturn_type", None),
            TreeVisit("visitBlock", None),
            TreeVisit("visitBlock", None),
            # TreeVisit("visitEval", None),
            TreeVisit("visitMethod_call", None)
        ]

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert list(visitor_fixture.trail.values()) == expected_calls
        assert len(visitor_fixture.errors) == 0

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

    @pytest.mark.skip
    def test_handle_clashing_function_ids(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        void foo() {}
        void foo() {}
        """)

        expected_calls = defaultCalls + []

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert list(visitor_fixture.trail.values()) == expected_calls
        assert visitor_fixture.errors == [
            SemanticsError(2, "foo", ErrorType.METHOD_ALREADY_DEFINED)
        ]
