import unittest


# If, loops & function calls checking.
from coursework.semantics import CoffeeTreeVisitor


class AdvancedSemantics(unittest.TestCase):
    def setUp(self) -> None:
        self.testSubject = CoffeeTreeVisitor()
        super().setUp()

    def tearDown(self) -> None:
        self.testSubject = None
        super().tearDown()


    def test_something(self):
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()

# import printf, printf; void foo(int x, int y) { return 0; } int a = food(1, -2.0, 5);