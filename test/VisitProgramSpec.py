import unittest
from unittest.mock import MagicMock

from CoffeeLang.CoffeeUtil import SymbolTable


class ProgramStructSpec(unittest.TestCase):
    def __init__(self):
        super().__init__()
        self.testSubject = SymbolTable()


    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
