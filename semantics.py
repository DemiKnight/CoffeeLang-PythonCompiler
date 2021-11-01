import antlr4 as antlr
from enum import Enum

from typing import List, Any

from CoffeeLang.CoffeeLexer import CoffeeLexer
from CoffeeLang.CoffeeVisitor import CoffeeVisitor
from CoffeeLang.CoffeeParser import CoffeeParser

from CoffeeLang.CoffeeUtil import Var, Method, Import, Loop, SymbolTable, Var
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

    def declareVar(self, scope_context: int, line_number: int, var_type: str, context: CoffeeParser.Var_assignContext):
        variable_id = context.var().ID().getText()
        variable_size = 8
        variable_array = False
        variable_def = Var(variable_id, var_type, variable_size, scope_context, variable_array, line_number)
        if self.stbl.peek(variable_id) is not None:
            self.errors.append(SemanticsError(line_number, variable_id, ErrorType.VAR_ALREADY_DEFINED))
        else:
            self.stbl.pushVar(variable_def)

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
            self.declareVar(Var.GLOBAL, line_number, variable_type, ctx.var_decl().var_assign(index))

        return None

    def visitVar_decl(self, ctx: CoffeeParser.Var_declContext):
        line_number = ctx.start.line
        variable_type = ctx.data_type().getText()
        for index in range(len(ctx.var_assign())):
            self.declareVar(Var.LOCAL, line_number, variable_type, ctx.var_assign(index))
        return None

    def _method_impl(self, line_number: int, method_id: str, ctx: CoffeeParser.Method_declContext):
        method_type = ctx.return_type().getText()

        method_def = Method(method_id, method_type, line_number)
        self.stbl.pushMethod(method_def)
        self.stbl.pushFrame(method_def)

        for index in range(len(ctx.param())):
            param_id = ctx.param(index).ID().getText()
            param_type = ctx.param(index).data_type().getText()
            param_size = 8
            param_is_array = False

            if self.stbl.peek(param_id) is not None:
                self.errors.append(
                    SemanticsError(ctx.param(index).start.line, param_id, ErrorType.VAR_PARAM_ALREADY_DEFINED))
            else:
                method_def.pushParam(param_type)

                param_def = Var(param_id, param_type, param_size, Var.LOCAL, param_is_array, line_number)
                self.stbl.pushVar(param_def) # TODO Might be incorrect!

        self.visit(ctx.block())
        self.stbl.popFrame()

    def visitMethod_decl(self, ctx: CoffeeParser.Method_declContext):
        line_number = ctx.start.line
        method_id = ctx.ID().getText()

        if self.stbl.peek(method_id) is not None:
            self.errors.append(SemanticsError(line_number, method_id, ErrorType.METHOD_ALREADY_DEFINED))
        else:
            self._method_impl(line_number, method_id, ctx)


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
