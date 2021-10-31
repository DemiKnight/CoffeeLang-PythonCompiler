import antlr4 as antlr
from enum import Enum

from typing import List, Any

from CoffeeLang.CoffeeLexer import CoffeeLexer
from CoffeeLang.CoffeeVisitor import CoffeeVisitor
from CoffeeLang.CoffeeParser import CoffeeParser

from CoffeeLang.CoffeeUtil import Var, Method, Import, Loop, SymbolTable
from Utils import SemanticsError


class TypePrecedence(Enum):
    FLOAT = 0
    INT = 1
    BOOL = 2


class CoffeeTreeVisitor(CoffeeVisitor):
    errors: List[SemanticsError]

    def __init__(self):
        self.stbl = SymbolTable()
        self.errors = list()

    def visit(self, tree):
        return super().visit(tree)

    def visitProgram(self, ctx: CoffeeParser.ProgramContext):
        self.stbl.pushFrame(ctx)
        self.visitChildren(ctx)
        self.stbl.popFrame()

if __name__ == "__main__":
    # load source code
    filein = open('./test.coffee', 'r')
    source_code = filein.read()
    filein.close()

    # create a token stream from source code
    lexer = CoffeeLexer(antlr.InputStream(source_code))
    stream = antlr.CommonTokenStream(lexer)

    # parse token stream
    parser = CoffeeParser(stream)
    tree = parser.program()

    # create Coffee Visitor object
    visitor = CoffeeTreeVisitor()

    # visit nodes from tree root
    visitor.visit(tree)
