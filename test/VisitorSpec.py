import pytest

from typing import List

from antlr4 import InputStream, CommonTokenStream, ParserRuleContext

from CoffeeLang.CoffeeLexer import CoffeeLexer
from CoffeeLang.CoffeeParser import CoffeeParser
from test.TestUtilities import StubbedCoffeeTreeVisitor, TreeVisit


def createTree(source_str: str) -> ParserRuleContext:
    lexer = CoffeeLexer(InputStream(source_str.strip()))
    stream = CommonTokenStream(lexer)
    parser = CoffeeParser(stream)
    return parser.program()


defaultCalls: List[TreeVisit] = [
    TreeVisit("visit", None),
    TreeVisit("visitProgram", None)
]

@pytest.fixture(autouse=True)
def visitor_fixture():
    yield StubbedCoffeeTreeVisitor()
