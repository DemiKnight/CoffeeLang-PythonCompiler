from Utils import SemanticsError, ErrorType
from VisitorSpec import *


class TestArraySpec:

    def test_handle_empty_arrays(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        int myArray[0];
        """)

        expected_calls = defaultCalls + [
            TreeVisit("visitGlobal_decl", None)
        ]

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert list(visitor_fixture.trail.values()) == expected_calls
        assert visitor_fixture.errors == [
            SemanticsError(1, "myArray", ErrorType.ARRAY_SIZE_ZERO_OR_LESS)
        ]

    @pytest.mark.skip
    def test_basic_array(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        int myArray[1];
        myArray[0] = 22;
        """)

        expected_calls = defaultCalls + [
            TreeVisit("vistGlobal_decl", None),
            TreeVisit("vistBlock", None),

        ]

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert list(visitor_fixture.trail.values()) == expected_calls
        assert len(visitor_fixture.errors) == 0
