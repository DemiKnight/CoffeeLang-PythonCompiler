import unittest
import pytest

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


defaultCalls: List[TreeVisit] = [
    TreeVisit("visitProgram", None)
]


@pytest.fixture(autouse=True)
def visitor_fixture():
    return StubbedCoffeeTreeVisitor()
