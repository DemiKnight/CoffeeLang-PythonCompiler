import antlr4 as antlr
from enum import Enum

from typing import List, Any

from CoffeeLang.CoffeeLexer import CoffeeLexer
from CoffeeLang.CoffeeVisitor import CoffeeVisitor
from CoffeeLang.CoffeeParser import CoffeeParser

from CoffeeLang.CoffeeUtil import Var, Method, Import, Loop, SymbolTable, Var
from Utils import SemanticsError, ErrorType, print_semantic_errors


# Type precendence for coffee
class TypePrecedence(Enum):
    FLOAT = 0
    INT = 1
    BOOL = 2
    NOTHING = 99


class CoffeeTreeVisitor(CoffeeVisitor):
    # List of all errors
    errors: List[SemanticsError]
    _entranceFlag: bool

    def __init__(self):
        self.stbl = SymbolTable()
        self._entranceFlag = False
        self.errors = list()

    # For global & local scopes
    def declare_var(self, scope_context: int, line_number: int, var_type: str, context: CoffeeParser.Var_assignContext):
        variable_id = context.var().ID().getText()
        # Duplicate variable ID in scope.
        if self.stbl.peek(variable_id) is not None:
            self.errors.append(SemanticsError(line_number, variable_id, ErrorType.VAR_ALREADY_DEFINED))
        else:
            variable_is_array = context.var().INT_LIT() is not None
            variable_size = int(context.var().INT_LIT().getText()) * 64 if variable_is_array else 8

            # Check specified array size
            if variable_is_array and int(context.var().INT_LIT().getText()) <= 0:
                self.errors.append(SemanticsError(line_number, variable_id, ErrorType.ARRAY_SIZE_ZERO_OR_LESS))

            variable_def = Var(variable_id, var_type, variable_size, scope_context, variable_is_array, line_number)

            # Should be a type string unless an error has occurred.
            variable_value_type = self.visit(context.expr()) if context.expr() is not None else None

            if variable_value_type is not None and variable_value_type != var_type:
                self.errors.append(
                    SemanticsError(line_number,
                                   variable_id,
                                   ErrorType.VAR_ASSIGN_TYPE_MISMATCH,
                                   variable_value_type,
                                   var_type))
            else:
                self.stbl.pushVar(variable_def)

    def visitProgram(self, ctx: CoffeeParser.ProgramContext):
        # Should only be called once, but just in case, use a flag to not duplicate errors in console.
        if self._entranceFlag:
            return super().visit(tree)
        else:
            self._entranceFlag = True
            main = Method("main", "int", ctx.start.line)
            self.stbl.pushFrame(main)
            self.visitChildren(ctx)
            self.stbl.popFrame()
            print_semantic_errors(self.errors)

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
            self.declare_var(Var.GLOBAL, line_number, variable_type, ctx.var_decl().var_assign(index))

    def visitVar_decl(self, ctx: CoffeeParser.Var_declContext):
        line_number = ctx.start.line
        variable_type = ctx.data_type().getText()
        for index in range(len(ctx.var_assign())):
            self.declare_var(Var.LOCAL, line_number, variable_type, ctx.var_assign(index))

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

            # Check for duplicate parameters
            if self.stbl.peek(param_id) is not None:
                self.errors.append(
                    SemanticsError(ctx.param(index).start.line, param_id, ErrorType.VAR_PARAM_ALREADY_DEFINED))
            else:
                method_def.pushParam(param_type)
                param_def = Var(param_id, param_type, param_size, Var.GLOBAL, param_is_array, line_number)
                self.stbl.pushVar(param_def)

        self.visit(ctx.block())

        # See `visitReturn` & `visitIf` for details
        if not method_def.has_return and method_def.return_type != "void":
            self.errors.append(SemanticsError(line_number, method_id, ErrorType.METHOD_MISSING_RETURN))

        self.stbl.popFrame()

    def visitMethod_decl(self, ctx: CoffeeParser.Method_declContext):
        line_number = ctx.start.line
        method_id = ctx.ID().getText()

        # Check for duplicate method_id (in scope)
        if self.stbl.peek(method_id) is not None:
            self.errors.append(SemanticsError(line_number, method_id, ErrorType.METHOD_ALREADY_DEFINED))
        else:
            self._method_impl(line_number, method_id, ctx)

    def visitExpr(self, ctx: CoffeeParser.ExprContext):
        if ctx.literal() is not None:
            returnType = self.visit(ctx.literal())
        elif ctx.location() is not None:
            returnType = self.visit(ctx.location())
        elif ctx.method_call() is not None:
            methodC: Method = self.visit(ctx.method_call())
            # MethodC is None when an error has occurred
            if methodC is None:
                return None
            elif methodC.return_type == "void":
                self.errors.append(SemanticsError(ctx.start.line, methodC.id, ErrorType.EXPRESSION_USING_VOID_METHOD))
                returnType = None
            else:
                returnType = methodC.return_type
        elif len(ctx.expr()) == 2:
            # If location, could return missing variable type.
            lhsType: str = self.visit(ctx.expr(0))
            rhsType: str = self.visit(ctx.expr(1))

            # Use numeric enum to determine type precedence. See TypePrecedence
            lhs = TypePrecedence[lhsType.upper()] if lhsType is not None else TypePrecedence.NOTHING
            rhs = TypePrecedence[rhsType.upper()] if rhsType is not None else TypePrecedence.NOTHING

            returnType = lhsType if lhs.value < rhs.value else rhsType
        elif ctx.data_type() is not None:
            returnType = ctx.data_type()
        else:
            returnType = self.visitChildren(ctx)

        # Logical `Not` type check, we don't have variable name in scope,
        # but another `EXPRESSION_CONDITION_TYPE_MISMATCH` will be thrown later.
        if ctx.NOT() is not None and returnType != "bool":
            self.errors.append(SemanticsError(ctx.start.line, "", ErrorType.EXPRESSION_CONDITION_TYPE_MISMATCH_NOT,
                                              type_mismatched=returnType, type_required="bool"))

        return returnType

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

        if self.stbl.find(location_id) is not None:
            return self.stbl.find(location_id).data_type
        else:
            self.errors.append(SemanticsError(ctx.start.line, location_id, ErrorType.VAR_NOT_FOUND))

    def visitMethod_call(self, ctx: CoffeeParser.Method_callContext) -> Method:
        line_number = ctx.start.line
        method_id = ctx.ID().getText()

        if self.stbl.peek(method_id) is not None:

            method_def: Method = self.stbl.find(method_id)

            # See `visitImport_stmt` for details
            if method_def.return_type == "import":
                print("\nWARNING: Check signature on imported method...\n")
                return method_def

            params = list()

            for index in range(len(ctx.expr())):
                visitTest = self.visit(ctx.expr(index))
                params.append(visitTest)

            if len(params) != len(method_def.param):
                self.errors.append(SemanticsError(line_number, method_id, ErrorType.METHOD_SIGNATURE_ARGUMENT_COUNT))
            elif params != method_def.param:  # Parameter type check
                self.errors.append(
                    SemanticsError(line_number, method_id, ErrorType.METHOD_SIGNATURE_TYPE_MISMATCH_PARAMETERS))

            return method_def
        else:  # Duplicate import
            self.errors.append(SemanticsError(line_number, method_id, ErrorType.METHOD_NOT_FOUND))

    def visitReturn(self, ctx: CoffeeParser.ReturnContext):
        methodCxt: Method = self.stbl.getMethodContext()

        # methodCxt should always return a method, either user-defined or `main`
        methodCxt.has_return = True
        returnValue = self.visit(ctx.expr())

        # Return type checks
        if methodCxt.id != "main":
            if methodCxt.return_type == "void" and returnValue is not None:
                self.errors.append(SemanticsError(ctx.start.line, methodCxt.id, ErrorType.METHOD_VOID_RETURNING_VALUE))
            elif methodCxt.return_type != returnValue:
                self.errors.append(SemanticsError(ctx.start.line, methodCxt.id, ErrorType.METHOD_RETURN_TYPE_MISMATCH))

        elif methodCxt.id == "main" and returnValue != "int":
            self.errors.append(SemanticsError(ctx.start.line, "main", ErrorType.MAIN_METHOD_RETURN_TYPE_MISMATCH,
                                              type_mismatched=returnValue))

    def visitImport_stmt(self, ctx: CoffeeParser.Import_stmtContext):

        for index in range(len(ctx.ID())):
            import_method_id = ctx.ID(index).getText()

            existing_method = self.stbl.find(import_method_id)

            if existing_method is not None: # Duplicate import
                self.errors.append(SemanticsError(ctx.start.line, import_method_id, ErrorType.IMPORT_DUPLICATE))
            else:
                # We don't know the imported function type, so utilise it for a warning
                method = Method(import_method_id, "import", ctx.start.line)
                self.stbl.pushMethod(method)


    def visitIf(self, ctx: CoffeeParser.IfContext):
        method_context: Method = self.stbl.getMethodContext()

        condition_type = self.visit(ctx.expr())
        if condition_type != "bool":
            self.errors.append(
                SemanticsError(ctx.start.line, method_context.id, ErrorType.EXPRESSION_CONDITION_TYPE_MISMATCH))

        # Attempt deduce whether the if statement returns something
        if method_context.return_type != "void":
            passed_main_if = False
            passed_else_if = False
            method_context.has_return = False

            # If we always have one code block
            self.visit(ctx.block(0))

            # Check whether `visitReturn` has modified `method_context.has_return`
            passed_main_if = method_context.has_return

            if ctx.ELSE() is not None:
                # Reset `method_context.has_return` for the else block
                method_context.has_return = False
                self.visit(ctx.block(1))

                # Check for `visitReturn` again
                passed_else_if = method_context.has_return
            else:
                passed_else_if = True

            method_context.has_return = passed_else_if & passed_main_if


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
