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

    def visit(self, tree):
        return super().visit(tree)

    def visitProgram(self, ctx) -> None:
        self.stbl.pushFrame(ctx)
        self.visitChildren(ctx)
        self.stbl.popFrame()

        for error in self.errors:
            print(error.errorStr())


    def visitGlobal_decl(self, ctx: CoffeeParser.Global_declContext):
        lineNumber = ctx.start.line
        variableType = ctx.var_decl().data_type().getText()

        for index in range(len(ctx.var_decl().var_assign())):
            varTest = ctx.var_decl().var_assign(index).var()
            variableId = ctx.var_decl().var_assign(index).var().ID().getText()

            maybeArrayLiteral = varTest.INT_LIT()
            # print(f'array lit {type(maybeArrayLiteral)} {maybeArrayLiteral.getText() == 0}')

            if self.stbl.peek(variableId) is not None:
                self.errors.append(SemanticsError(lineNumber, f"var {variableId} already defined"))
                # print(f'error on line {lineNumber}: var {variableId} already defined')

            if maybeArrayLiteral is None:
                print(f"zz{lineNumber}")
                nonArrayVar = Var(variableId, variableType, 8, Var.GLOBAL, False, lineNumber)
                self.stbl.pushVar(nonArrayVar)
            elif maybeArrayLiteral.getText() == '0':
                print(f'error on line {lineNumber}: array {variableId} can\'t be 0')
            else:
                print(f"x{lineNumber} {maybeArrayLiteral.getText() == '0'}")
                arrayVar = Var(variableId, variableType, varTest.INT_LIT, Var.GLOBAL, True, lineNumber)
                self.stbl.pushVar(arrayVar)


    def visitMethod_decl(self, ctx: CoffeeParser.Method_declContext):
        lineNumber = ctx.start.line
        methodId = ctx.ID().getText()
        methodType = ctx.return_type().getText()

        if self.stbl.peek(methodId) is not None:
            self.errors.append(SemanticsError(lineNumber, f"Method {methodId} is already defined"))
            # print(f"error on line {lineNumber}: Method {methodId} is already defined")

        method = Method(methodId, methodType, lineNumber)
        self.stbl.pushMethod(method)
        self.stbl.pushFrame(method)

        for index in range(len(ctx.param())):
            paramId = ctx.param(index).ID().getText()
            print(paramId)
            paramType = ctx.param(index).data_type().getText()
            paramSize = 8
            paramArray = False

            if self.stbl.peek(paramId) is not None:
                self.errors.append(SemanticsError(lineNumber, f"Parameter {paramId} is already defined"))
                # print(f"error on line {lineNumber}: Parameter {paramId} is already defined")

            param = Var(paramId, paramType, paramSize, Var.LOCAL, paramArray, lineNumber)
            method.pushParam(paramType)
            self.stbl.pushVar(param)

        self.visit(ctx.block())

        print(f'{method.has_return} {methodType} {method.has_return is False and methodType != "void"}')

        if method.has_return is True and methodType == "void":
            print(f"error: {methodId} should have returned {methodType}")

        self.stbl.popFrame()

    def visitBlock(self, ctx: CoffeeParser.BlockContext):
        if ctx.RCURLY() is not None:
            self.stbl.pushScope()
        self.visitChildren(ctx)
        if ctx.LCURLY() is not None:
            self.stbl.popScope()

    def visitVar_decl(self, ctx: CoffeeParser.Var_declContext):
        lineNumber = ctx.start.line
        variableType = ctx.data_type().getText()

        print(f'{lineNumber}: {variableType}')

        for index in range(len(ctx.var_assign())):
            variableId = ctx.var_assign(index).var().ID().getText()
            if self.stbl.peek(variableId) is not None:
                self.errors.append(SemanticsError(lineNumber, f"var {variableId} already defined"))
                # print(f'error on line {lineNumber}: var {variableId} already defined')

            variableSize = 8
            isVariableArray = False
            var = Var(variableId, variableType, variableSize, Var.LOCAL, isVariableArray, lineNumber)
            self.stbl.pushVar(var)

    def visitExpr(self, ctx: CoffeeParser.ExprContext):
        if ctx.literal() is not None:
            return self.visit(ctx.literal())
        elif ctx.location() is not None:
            self.stbl.pushScope()
            result = self.visit(ctx.location())
            self.stbl.popScope()

            return result
        elif ctx.data_type() is not None:
            return ctx.data_type()
        elif len(ctx.expr()) == 2:
            print(ctx.expr(0).start.line)
            lhsExpressionType = self.visit(ctx.expr(0))
            rhsExpressionType = self.visit(ctx.expr(1))
            print(type(rhsExpressionType))
            print(type(lhsExpressionType))
            rhs = TypePrecedence[rhsExpressionType.upper()]
            lhs = TypePrecedence[lhsExpressionType.upper()]
            # print(f"{lhs} {rhs} {lhs.value > rhs.value} {lhsExpressionType if lhs.value < rhs.value else rhsExpressionType}")
            return lhsExpressionType if lhs.value < rhs.value else rhsExpressionType
        else:
            return self.visitChildren(ctx)

    # `define the visitLiteral method to return a string for each possible literal (bool, int, float, char,
    # string).`
    def visitLiteral(self, ctx: CoffeeParser.LiteralContext):
        # bool
        if ctx.bool_lit() is not None:
            return "bool"

        # int
        elif ctx.INT_LIT is not None:
            return "int"

        # char
        elif ctx.CHAR_LIT() is not None:
            return "char"

        # float
        elif ctx.FLOAT_LIT() is not None:
            return "float"

        # string
        else:
            return "string"

    def visitLocation(self, ctx: CoffeeParser.LocationContext):
        variableId = ctx.ID().getText()
        # print(f"test {variableId} {self.stbl.find(variableId).data_type}")

        if self.stbl.peek(variableId) is not None:
            print(f"line {ctx.start.line}: {variableId}")
            return self.stbl.find(variableId).data_type

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
