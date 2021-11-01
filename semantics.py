import antlr4 as antlr
from enum import Enum

from typing import List, Any

from CoffeeLang.CoffeeLexer import CoffeeLexer
from CoffeeLang.CoffeeVisitor import CoffeeVisitor
from CoffeeLang.CoffeeParser import CoffeeParser

from CoffeeLang.CoffeeUtil import Var, Method, Import, Loop, SymbolTable
from Utils import SemanticsError, ErrorType, printSemanticErrors


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
        value = super().visit(tree)

        printSemanticErrors(self.errors)

        return value

    def visitProgram(self, ctx: CoffeeParser.ProgramContext):
        self.stbl.pushFrame(ctx)
        self.visitChildren(ctx)
        self.stbl.popFrame()
        return None

    def visitBlock(self, ctx: CoffeeParser.BlockContext):
        if ctx.LCURLY() is not None:
            self.stbl.pushScope()
        self.visitChildren(ctx)

        if ctx.RCURLY() is not None:
            self.stbl.popScope()
        return None

    def visitGlobal_decl(self, ctx: CoffeeParser.Global_declContext):
        line_number = ctx.start.line
        variable_type = ctx.var_decl().data_type().getText()
        for index in range(len(ctx.var_decl().var_assign())):
            variable_id = ctx.var_decl().var_assign(index).var().ID().getText()
            variable_size = 8
            variable_array = False
            variable_def = Var(variable_id, variable_type, variable_size, Var.GLOBAL, variable_array, line_number)
            if self.stbl.peek(variable_id) is not None:
                self.errors.append(SemanticsError(line_number, variable_id, ErrorType.VAR_ALREADY_DEFINED))
            else:
                self.stbl.pushVar(variable_def)
        return None

    def visitVar_decl(self, ctx: CoffeeParser.Var_declContext):
        line_number = ctx.start.line
        variable_type = ctx.data_type().getText()
        for index in range(len(ctx.var_assign())):
            variable_id = ctx.var_assign(index).var().ID().getText()
            variable_size = 8
            variable_array = False
            variable_def = Var(variable_id, variable_type, variable_size, Var.LOCAL, variable_array, line_number)
            if self.stbl.peek(variable_id) is not None:
                self.errors.append(SemanticsError(line_number, variable_id, ErrorType.VAR_ALREADY_DEFINED))
            else:
                self.stbl.pushVar(variable_def)
        return None

    def visitData_type(self, ctx: CoffeeParser.Data_typeContext):
        return super().visitData_type(ctx)

    def visitVar_assign(self, ctx: CoffeeParser.Var_assignContext):
        return super().visitVar_assign(ctx)

    def visitVar(self, ctx: CoffeeParser.VarContext):
        return super().visitVar(ctx)

    def visitExpr(self, ctx: CoffeeParser.ExprContext):
        return super().visitExpr(ctx)


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
