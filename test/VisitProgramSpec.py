import unittest
from unittest.mock import MagicMock

from CoffeeLang.CoffeeUtil import SymbolTable
from semantics import CoffeeTreeVisitor
from test.TestUtil import strToProgram


class ProgramStructSpec(unittest.TestCase):
    def setUp(self) -> None:
        self.testSubject = CoffeeTreeVisitor()
        print(f"@@ {self._testMethodName} @@")
        super().setUp()

    def tearDown(self) -> None:
        self.testSubject = None
        print("-" * 20)
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
        self.testSubject.visit(prog)

        self.assertEqual(len(self.testSubject.errors), 2)

    def test_default_success(self):
        # given
        prog = strToProgram("""
        float a = 1;
        {
          int b = 2;
        }
        a = a + 2;
        """)

        # when
        self.testSubject.visit(prog)

        self.assertEqual(len(self.testSubject.errors), 0)

    def test_default_duplicate(self):
        # given
        prog = strToProgram("""
        float a = 1;
        float a = 2;
        {
          int b = 2, b;
          int a;
        }
        a = a + b;
        """)

        # when
        self.testSubject.visit(prog)

        self.assertEqual(len(self.testSubject.errors), 3)

    def test_method_basic(self):
        # given
        prog = strToProgram("""
        void foo(int a, float a, float b) {
            int b;
        }
        """)

        # when
        self.testSubject.visit(prog)

        # then
        self.assertEqual(len(self.testSubject.errors), 1)

    def test_method_basic_success(self):
        # given
        prog = strToProgram("""
        void foo(int a, int b) {
            int z = a + b;
        }
        """)

        # when
        self.testSubject.visit(prog)

        # then
        self.assertEqual(len(self.testSubject.errors), 0)

    def test_method_basic_duplicate(self):
        # given
        prog = strToProgram("""
        void foo(int a, float b) {
            int b;
            return 0; 
        }
        void foo(int a, float b) {
            int b;
            return 0; 
        }
        """)

        # when
        self.testSubject.visit(prog)

        # then
        self.assertEqual(len(self.testSubject.errors), 1)

    def test_type_check_default(self):
        # given
        # TODO Implement strings and char testing
        prog = strToProgram("""
        float a = 2.1;
        int b = 2;
        bool d = false;
        return a + 2;
        """)

        # when
        self.testSubject.visit(prog)

        # then
        self.assertEqual(len(self.testSubject.errors), 0)

    def test_type_missing_variable(self):
        # given
        prog = strToProgram("""
        int a = 2;
        return a + z; 
        """)

        # when
        self.testSubject.visit(prog)

        # then
        self.assertEqual(len(self.testSubject.errors), 1)

    def test_expression_basic(self):
        # given
        prog = strToProgram("""
        int a = 2 + 3;
        """)

        # when
        self.testSubject.visit(prog)

        # then
        self.assertEqual(len(self.testSubject.errors), 0)

    def test_array_zero(self):
        # given
        prog = strToProgram("""
        int a[0];
        int b[2];
        """)

        # when
        self.testSubject.visit(prog)

        # then
        self.assertEqual(len(self.testSubject.errors), 1)

    def test_coursework_1(self):
        # 4, 5, 6, 7, 26
        # given
        prog = strToProgram("""
        import printf, printf;
        void foo(int x, int y) {
            return 0;
        }

        int a = food(1, -2.0, 5);""")

        # when
        self.testSubject.visit(prog)

        # then
        self.assertEqual(len(self.testSubject.errors), 4)


if __name__ == '__main__':
    unittest.main()
