import pytest

from test.VisitorSpec import VisitorSpec, createTree


class TestMethodSpec(VisitorSpec):

    @pytest.mark.skip()
    def test_method_decl(self):
        test_prog = createTree("""""")

    @pytest.mark.skip()
    def test_method_import(self):
        test_prog = createTree("""""")

    @pytest.mark.skip()
    def test_handle_existing_method_name(self):
        test_prog = createTree("""
        """)