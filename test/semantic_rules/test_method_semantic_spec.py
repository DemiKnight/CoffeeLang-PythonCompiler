import pytest

from test.VisitorSpec import createTree


class TestMethodSpec:

    @pytest.mark.skip()
    def test_method_decl(self, visitor_fixture):
        test_prog = createTree("""""")

    @pytest.mark.skip()
    def test_method_import(self, visitor_fixture):
        test_prog = createTree("""""")

    @pytest.mark.skip()
    def test_handle_existing_method_name(self, visitor_fixture):
        test_prog = createTree("""
        """)