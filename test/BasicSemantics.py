import unittest

# All kinds of variable declarations and type checking
from semantics import CoffeeTreeVisitor
from test.TestUtil import strToProgram


class BasicSemanticsSpec(unittest.TestCase):

    def setUp(self) -> None:
        self.testSubject = CoffeeTreeVisitor()
        super().setUp()

    def tearDown(self) -> None:
        self.testSubject = None
        super().tearDown()

    def test_variable_declaration(self):
        # given
        prog = strToProgram("""
        int a;
        """)

        # when
        test = self.testSubject.visit(prog)

        self.assertEqual(len(self.testSubject.errors), 0)

    def test_variable_declaration_with_literal(self):
        # given
        prog = strToProgram("""
        int a = 5;
        """)




if __name__ == '__main__':
    unittest.main()
