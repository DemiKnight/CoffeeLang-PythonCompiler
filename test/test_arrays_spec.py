from Utils import SemanticsError, ErrorType
from VisitorSpec import *

class TestArraySpec:

    @pytest.mark.skip("Sort variable test.")
    def test_handle_empty_arrays(self, visitor_fixture):
        # Given
        test_prog = createTree("""
        int myArray[0];
        """)

        expected_calls = defaultCalls + [

        ]

        # When
        visitor_fixture.visit(test_prog)

        # Then
        assert list(visitor_fixture.trail.values()) == expected_calls
        assert visitor_fixture.errors == [
            SemanticsError(1, "myArray", ErrorType.ARRAY_SIZE_ZERO_OR_LESS)
        ]