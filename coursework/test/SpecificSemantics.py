import unittest
from unittest.mock import Mock

from CoffeeLang.CoffeeUtil import SymbolTable
from coursework.semantics import CoffeeTreeVisitor
from test.TestUtil import strToProgram


# 1 to 27 `Semantic Rules` from Coffee Lang Spec
class SpecificSemanticsSpec(unittest.TestCase):
    def setUp(self) -> None:
        self.testSubject = CoffeeTreeVisitor()
        self.testSubject.stbl = Mock(spec=SymbolTable(), wraps=SymbolTable())

        print(f"@@ {self._testMethodName} @@")
        super().setUp()

    def tearDown(self) -> None:
        self.testSubject = None
        print("-" * 20)
        super().tearDown()

    def test_1_declare_before_usage_expr(self):
        # given
        prog = strToProgram("""
        int b = a + 3;
        """)

        # when
        self.testSubject.visit(prog)

        # print(self.testSubject.stbl.peek())
        # then
        # self.assertEqual(len(self.testSubject.errors), 1)
        print(self.testSubject.stbl.called)

    def test_2_variable_unique_identifier(self):
        # given
        prog = strToProgram("""
        int a = 0;
        int a = a + 3;
        {
          int a = 2;
        }
        """)

        # when
        self.testSubject.visit(prog)

        # then
        # self.assertEqual(len(self.testSubject.errors), 1)

    def test_2_variable_unique_identifier_method(self):
        # given
        prog = strToProgram("""
        void foo(int a, float b) {
            int a;
        }
        """)

        # when
        self.testSubject.visit(prog)

        # then
        # self.assertEqual(len(self.testSubject.errors), 1)


if __name__ == '__main__':
    unittest.main()
# 1. Variables must be declared before use
# 2. Variable declarations must have unique identifiers in a scope
# 3. Method declarations (including imported methods) must have unique identifiers in a scope
# 4. Method calls must refer to a declared method with an identical signature (return type, and number and type of parameters)
# 5. Method calls referring to imported methods must produce a warning to check the argument and return types match that of the imported method
# 6. Void methods cannot return an expression
# 7. Non-void methods must return an expression
# 8. The main method does not require a return statement, but if it has one, it must be of type int
# 9. Branch statements (if-else) containing return statements do not qualify a method as having a return statement and a warning must be issued unless they appear in both the main branch and the else branch
# 10. Loops containing return statements do not qualify a method as having a return statement and a warning must be issued
# 11. The expression in a branch statement must have type bool
# 12. The expression in a while loop must have type bool
# 13. The low and high expressions in a limit must have type int
# 14. Arrays must be declared with size greater than 0
# 15. The id in a for-loop must reference a declared array variable
# 16. Arrays cannot be assigned during declaration
# 17. Char expressions must be coerced to int
# 18. The expression in an assignment must have type bool, int or float
# 19. Locations of the from <id> [ <expr> ] must refer to a declared array variable
# 20. In a location, array indices must have type 'int'
# 21. The expression in unary minus operation must have type int or float
# 22. The expression in logical not operation must have type bool
# 23. The expression(s) in an arithmetic operation must have type int or float
# 24. The expression(s) in a logical operation must have type bool
# 25. The singular expression in a block (expr) provides a valid return value for a method without requiring the return keyword
# 26. Methods returning void cannot be used in an expression
# 27. Break and continue statements must be contained within the body of a loop.
