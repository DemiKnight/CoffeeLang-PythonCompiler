from __future__ import annotations

import antlr4 as antlr
from enum import Enum

from typing import List, Any

from CoffeeLang.CoffeeLexer import CoffeeLexer
from CoffeeLang.CoffeeVisitor import CoffeeVisitor
from CoffeeLang.CoffeeParser import CoffeeParser
from CoffeeLang.CoffeeUtil import SymbolTable

from CoffeeLang.CoffeeUtil import Var, Method, Import, Loop, SymbolTable
from SemanticsUtils import SemanticsError


class TypePrecedence(Enum):
    FLOAT = 0
    INT = 1
    BOOL = 2


class CoffeeTreeVisitor(CoffeeVisitor):
    errors: List[SemanticsError]

    def __init__(self):
        self.stbl = SymbolTable()
        self.errors = list()

    def visitProgram(self, ctx) -> None:
        self.stbl.pushFrame(ctx)
        self.visitChildren(ctx)
        self.stbl.popFrame()

        for error in self.errors:
            print(error.errorStr())
        return None

    def visitGlobal_decl(self, ctx: CoffeeParser.Global_declContext):
        self.stbl.pushScope()
        variable_type = ctx.var_decl().data_type().getText()
        line_number = ctx.start.line

        for index in range(len(ctx.var_decl().var_assign())):
            variable = ctx.var_decl().var_assign(index).var()
            variable_id = variable.ID().getText()
            variable_size = 8  # Implement arrays here

            if self.stbl.peek(variable_id) is not None:
                self.errors.append(SemanticsError(line_number, f"{variable_id} declared twice"))


            return_variable = None
            if variable.INT_LIT() is not None:
                print()
            else:
                print()
                # Var(variable_id, )


            # print(var.var().ID())

        self.stbl.popScope()
        return None

    def visitBlock(self, ctx: CoffeeParser.BlockContext):
        if ctx.LCURLY() is not None:
            self.stbl.pushScope()

        self.visitChildren(ctx)

        if ctx.RCURLY() is not None:
            self.stbl.popScope()

    def visitVar_decl(self, ctx: CoffeeParser.Var_declContext):
        return super().visitVar_decl(ctx)

    def visitMethod_decl(self, ctx: CoffeeParser.Method_declContext):
        return super().visitMethod_decl(ctx)

    def visitExpr(self, ctx: CoffeeParser.ExprContext):
        return super().visitExpr(ctx)

    def visitLiteral(self, ctx: CoffeeParser.LiteralContext):
        return super().visitLiteral(ctx)

    def visitLocation(self, ctx: CoffeeParser.LocationContext):
        return super().visitLocation(ctx)

    def visitImport_stmt(self, ctx: CoffeeParser.Import_stmtContext):
        return super().visitImport_stmt(ctx)

    def visitVar_assign(self, ctx: CoffeeParser.Var_assignContext):
        return super().visitVar_assign(ctx)

    def visitVar(self, ctx: CoffeeParser.VarContext):
        return super().visitVar(ctx)

    def visitData_type(self, ctx: CoffeeParser.Data_typeContext):
        return super().visitData_type(ctx)

    def visitReturn_type(self, ctx: CoffeeParser.Return_typeContext):
        return super().visitReturn_type(ctx)

    def visitParam(self, ctx: CoffeeParser.ParamContext):
        return super().visitParam(ctx)

    def visitEval(self, ctx: CoffeeParser.EvalContext):
        return super().visitEval(ctx)

    def visitAssign(self, ctx: CoffeeParser.AssignContext):
        return super().visitAssign(ctx)

    def visitIf(self, ctx: CoffeeParser.IfContext):
        return super().visitIf(ctx)

    def visitFor(self, ctx: CoffeeParser.ForContext):
        return super().visitFor(ctx)

    def visitWhile(self, ctx: CoffeeParser.WhileContext):
        return super().visitWhile(ctx)

    def visitReturn(self, ctx: CoffeeParser.ReturnContext):
        return super().visitReturn(ctx)

    def visitBreak(self, ctx: CoffeeParser.BreakContext):
        return super().visitBreak(ctx)

    def visitContinue(self, ctx: CoffeeParser.ContinueContext):
        return super().visitContinue(ctx)

    def visitPass(self, ctx: CoffeeParser.PassContext):
        return super().visitPass(ctx)

    def visitLoop_var(self, ctx: CoffeeParser.Loop_varContext):
        return super().visitLoop_var(ctx)

    def visitMethod_call(self, ctx: CoffeeParser.Method_callContext):
        return super().visitMethod_call(ctx)

    def visitAssign_op(self, ctx: CoffeeParser.Assign_opContext):
        return super().visitAssign_op(ctx)

    def visitBool_lit(self, ctx: CoffeeParser.Bool_litContext):
        return super().visitBool_lit(ctx)

    def visitLimit(self, ctx: CoffeeParser.LimitContext):
        return super().visitLimit(ctx)

    def visitLow(self, ctx: CoffeeParser.LowContext):
        return super().visitLow(ctx)

    def visitHigh(self, ctx: CoffeeParser.HighContext):
        return super().visitHigh(ctx)

    def visitStep(self, ctx: CoffeeParser.StepContext):
        return super().visitStep(ctx)


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
