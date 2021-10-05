import antlr4 as antlr
from CoffeeLang.CoffeeLexer import CoffeeLexer
from CoffeeLang.CoffeeParser import CoffeeParser


def strToProgram(sourceCode: str) -> CoffeeParser.ProgramContext:
    lexer = CoffeeLexer(antlr.InputStream(sourceCode.strip()))
    stream = antlr.CommonTokenStream(lexer)
    # parse token stream
    parser = CoffeeParser(stream)
    return parser.program()
