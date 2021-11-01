import antlr4 as antlr
from enum import Enum

from typing import List, Any

from CoffeeLang.CoffeeLexer import CoffeeLexer
from CoffeeLang.CoffeeVisitor import CoffeeVisitor
from CoffeeLang.CoffeeParser import CoffeeParser

from CoffeeLang.CoffeeUtil import Var, Method, Import, Loop, SymbolTable, Var
from Utils import SemanticsError, ErrorType, print_semantic_errors


class TypePrecedence(Enum):
    FLOAT = 0
    INT = 1
    BOOL = 2
    NOTHING = 99


class CoffeeTreeVisitor(CoffeeVisitor):
    errors: List[SemanticsError]
    entranceFlag: bool

    def __init__(self):
        self.stbl = SymbolTable()
        self.entranceFlag = False
        self.errors = list()

    def declareVar(self, scope_context: int, line_number: int, var_type: str, context: CoffeeParser.Var_assignContext):
        variable_id = context.var().ID().getText()
        if self.stbl.peek(variable_id) is not None:
            self.errors.append(SemanticsError(line_number, variable_id, ErrorType.VAR_ALREADY_DEFINED))
        else:
            variable_size = 8
            variable_array = False
            variable_def = Var(variable_id, var_type, variable_size, scope_context, variable_array, line_number)

            variable_value_type = self.visit(context.expr())

            if variable_value_type != var_type:
                self.errors.append(
                    SemanticsError(line_number,
                                   variable_id,
                                   ErrorType.VAR_ASSIGN_TYPE_MISMATCH,
                                   variable_value_type,
                                   var_type))
            else:
                self.stbl.pushVar(variable_def)

    def visit(self, tree):
        if self.entranceFlag:
            return super().visit(tree)
        else:
            self.entranceFlag = True
            value = super().visit(tree)
            print_semantic_errors(self.errors)
            return value


    def visitProgram(self, ctx: CoffeeParser.ProgramContext):
        method = Method("main", "int", ctx.start.line)
        self.stbl.pushFrame(method)
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
                self.stbl.pushVar(param_def)  # TODO Might be incorrect!

        self.visit(ctx.block())
        self.stbl.popFrame()

    def visitMethod_decl(self, ctx: CoffeeParser.Method_declContext):
        line_number = ctx.start.line
        method_id = ctx.ID().getText()

        if self.stbl.peek(method_id) is not None:
            self.errors.append(SemanticsError(line_number, method_id, ErrorType.METHOD_ALREADY_DEFINED))
        else:
            self._method_impl(line_number, method_id, ctx)

    def visitExpr(self, ctx: CoffeeParser.ExprContext):
        if ctx.literal() is not None:
            return self.visit(ctx.literal())
        elif ctx.location() is not None:
            return self.visit(ctx.location())
        elif len(ctx.expr()) == 2:
            # If location, could return missing variable type.
            lhsType: str = self.visit(ctx.expr(0))
            rhsType: str = self.visit(ctx.expr(1))

            lhs = TypePrecedence[lhsType.upper()] if lhsType is not None else TypePrecedence.NOTHING
            rhs = TypePrecedence[rhsType.upper()] if rhsType is not None else TypePrecedence.NOTHING

            return lhsType if lhs.value < rhs.value else rhsType
        elif ctx.data_type() is not None:
            return ctx.data_type()
        else:
            return self.visitChildren(ctx)

    def visitLiteral(self, ctx: CoffeeParser.LiteralContext):
        if ctx.INT_LIT() is not None:
            return "int"
        elif ctx.bool_lit() is not None:
            return "bool"
        elif ctx.FLOAT_LIT() is not None:
            return "float"
        elif ctx.CHAR_LIT() is not None:
            return "char"
        elif ctx.STRING_LIT() is not None:
            return "string"
        else:
            # Should be impossible to get here
            self.errors.append(SemanticsError(ctx.start.line, ctx.getText(), ErrorType.UNKNOWN_LITERAL_TYPE))

    def visitLocation(self, ctx: CoffeeParser.LocationContext):
        location_id: str = ctx.ID().getText()

        if self.stbl.peek(location_id) is not None:
            return self.stbl.find(location_id).data_type
        else:
            self.errors.append(SemanticsError(ctx.start.line, location_id, ErrorType.VAR_NOT_FOUND))


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
