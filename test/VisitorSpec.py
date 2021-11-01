import unittest
from typing import List

from antlr4 import InputStream, CommonTokenStream, ParserRuleContext

from CoffeeLang.CoffeeLexer import CoffeeLexer
from CoffeeLang.CoffeeParser import CoffeeParser
from TestUtilities import StubbedCoffeeTreeVisitor, TreeVisit


def createTree(source_str: str) -> ParserRuleContext:
    lexer = CoffeeLexer(InputStream(source_str))
    stream = CommonTokenStream(lexer)
    parser = CoffeeParser(stream)
    return parser.program()


class VisitorSpec(unittest.TestCase):
    target: StubbedCoffeeTreeVisitor
    defaultCalls: List[TreeVisit]

    @staticmethod
    def prepTestName(test_name: str):
        return test_name.replace("test_", "").replace("_", " ")

    def ignoreTest(self, func):
        self.skipTest(f"Ignoring test `{self.prepTestName(func.__name__)}`")

    def setUp(self) -> None:
        self.target = StubbedCoffeeTreeVisitor()
        self.defaultCalls = [
            TreeVisit("visitProgram", None)
        ]
        super().setUp()



if __name__ == '__main__':
    unittest.main()
