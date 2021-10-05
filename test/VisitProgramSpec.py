import unittest
from unittest.mock import MagicMock

from CoffeeLang.CoffeeUtil import SymbolTable
from semantics import CoffeeTreeVisitor
from test.TestUtil import strToProgram


class ProgramStructSpec(unittest.TestCase):
    def setUp(self) -> None:
        self.testSubject = CoffeeTreeVisitor()
        super().setUp()

    def tearDown(self) -> None:
        self.testSubject = None
        super().tearDown()

    def test_default(self):
        # given
        prog = strToProgram("""
        float a = 1;
        {
          int b = 2, b;
          int a;
        }
        a = a + b;
        """)

        # when
        test = self.testSubject.visit(prog)

        self.assertEqual(len(self.testSubject.errors), 0)

if __name__ == '__main__':
    unittest.main()
