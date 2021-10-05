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

    def variableDeclUtil(self, type: str, line_number: int, indexes: range, thing):
        for index in indexes:
            variable: CoffeeParser.VarContext = thing(index).var()
            variable_id = variable.ID().getText()
            variable_size = 8  # Implement arrays here
            variable_is_array = False

            if self.stbl.peek(variable_id) is not None:
                self.errors.append(SemanticsError(line_number, f"{variable_id} declared twice"))

            if variable.INT_LIT() is not None:
                variable_size = variable.INT_LIT().getText()

                if variable_size == "0":
                    self.errors.append(SemanticsError(line_number, f"array {variable_id} must not be declared  empty!"))

                variable_is_array = True

            return_variable = Var(variable_id, type, variable_size, Var.GLOBAL, variable_is_array, line_number)
            self.stbl.pushVar(return_variable)

        return None

    def visitProgram(self, ctx) -> None:
        self.stbl.pushFrame(ctx)
        self.visitChildren(ctx)
        self.stbl.popFrame()

        for error in self.errors:
            print(error.errorStr())
        if len(self.errors) == 0:
            print("Success! No errors found...")

        return None

    def visitGlobal_decl(self, ctx: CoffeeParser.Global_declContext):
        variable_type = ctx.var_decl().data_type().getText()
        line_number = ctx.start.line

        self.variableDeclUtil(variable_type, line_number, range(len(ctx.var_decl().var_assign())),
                              ctx.var_decl().var_assign)

        return None

    def visitBlock(self, ctx: CoffeeParser.BlockContext):
        if ctx.LCURLY() is not None:
            self.stbl.pushScope()

        self.visitChildren(ctx)

        if ctx.RCURLY() is not None:
            self.stbl.popScope()

    def visitVar_decl(self, ctx: CoffeeParser.Var_declContext):
        line_number = ctx.start.line
        variable_type = ctx.data_type().getText()

        self.variableDeclUtil(variable_type, line_number, range(len(ctx.var_assign())),
                              ctx.var_assign)

    def visitMethod_decl(self, ctx: CoffeeParser.Method_declContext):
        line = ctx.start.line
        method_id = ctx.ID().getText()
        method_type = ctx.return_type().getText()

        if self.stbl.peek(method_id) is not None:
            self.errors.append(SemanticsError(line, f"method {method_id}->{method_type} declared twice!"))

        method = Method(method_id, method_type, line)
        self.stbl.pushMethod(method)
        self.stbl.pushFrame(method)

        # self.variableDeclUtil()
        for index in range(len(ctx.param())):
            param = ctx.param(index)
            variable_id = param.ID().getText()
            variable_type = param.data_type().getText()
            variable_size = 8  # Implement arrays here
            variable_is_array = False

            if self.stbl.peek(variable_id) is not None:
                self.errors.append(SemanticsError(line, f"Duplicate param {variable_id} for function {method_id}"))

            method.pushParam(variable_type)
            variable = Var(variable_id, variable_type, variable_size,Var.LOCAL,variable_is_array,line)
            self.stbl.pushVar(variable)

        self.visit(ctx.block())
        self.stbl.popFrame()

    def visitExpr(self, ctx: CoffeeParser.ExprContext):
        if ctx.literal() is not None:
            return self.visit(ctx.literal())
        elif ctx.location() is not None:
            return self.visit(ctx.location())
        elif len(ctx.expr()) == 2:
            expression_0 = self.visit(ctx.expr(0))
            expression_1 = self.visit(ctx.expr(1))
            expression_0_type = None
            expression_1_type = None

            if expression_0 is not None:
                expression_0_type = TypePrecedence[expression_0.upper()]

            if expression_1 is not None:
                expression_1_type = TypePrecedence[expression_1.upper()]

            if expression_1 is not None and expression_0 is not None:
                return expression_0 if expression_0_type.value < expression_1_type.value else expression_1
            else:
                return None
        elif ctx.data_type() is not None:
            return self.visit(ctx.data_type())
        else:
            return self.visitChildren(ctx)

    def visitLiteral(self, ctx: CoffeeParser.LiteralContext):
        if ctx.bool_lit() is not None:
            return "bool"
        elif ctx.INT_LIT() is not None:
            return "int"
        elif ctx.CHAR_LIT() is not None:
            return "char"
        elif ctx.FLOAT_LIT() is not None:
            return "float"
        else:  # should be string
            return "string"

    def visitLocation(self, ctx: CoffeeParser.LocationContext):
        variable_id = ctx.ID().getText()

        if self.stbl.peek(variable_id) is not None:
            return self.stbl.find(variable_id).data_type
        else:
            self.errors.append(SemanticsError(ctx.start.line, f"missing variable {variable_id} in expression"))

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
