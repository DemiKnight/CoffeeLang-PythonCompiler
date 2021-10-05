import unittest
from semantics import CoffeeTreeVisitor
from test.TestUtil import strToProgram

# 1 to 27 `Semantic Rules` from Coffee Lang Spec
class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.testSubject = CoffeeTreeVisitor()
        super().setUp()

    def tearDown(self) -> None:
        self.testSubject = None
        super().tearDown()

    def test_declare_before_usage(self):
        # given
        prog = strToProgram("""
        int a = 2;
        {
          a = a + 2;
        }
        int b = a + 3;
        """)

        # when
        self.testSubject.visit(prog)

        # then
        self.assertEqual(len(self.testSubject.errors), 0)



if __name__ == '__main__':
    unittest.main()
# "1. Variables must be declared before use
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
# 22. The expression in logical not operation must have"

