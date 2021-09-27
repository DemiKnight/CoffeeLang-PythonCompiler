import antlr4 as antlr
from CoffeeLang.CoffeeLexer import CoffeeLexer
from CoffeeLang.CoffeeVisitor import CoffeeVisitor
from CoffeeLang.CoffeeParser import CoffeeParser
from CoffeeLang.CoffeeUtil import SymbolTable

class CoffeeTreeVisitor(CoffeeVisitor):
    def __init__(self):
        self.stbl = SymbolTable()

    def visitProgram(self, ctx):
        self.visitChildren(ctx)

    def visitImport_stmt(self, ctx: CoffeeParser.Import_stmtContext):
        return super().visitImport_stmt(ctx)

    def visitGlobal_decl(self, ctx: CoffeeParser.Global_declContext):
        return super().visitGlobal_decl(ctx)

    def visitVar_decl(self, ctx: CoffeeParser.Var_declContext):
        return super().visitVar_decl(ctx)

    def visitVar_assign(self, ctx: CoffeeParser.Var_assignContext):
        return super().visitVar_assign(ctx)

    def visitVar(self, ctx: CoffeeParser.VarContext):
        return super().visitVar(ctx)

    def visitData_type(self, ctx: CoffeeParser.Data_typeContext):
        return super().visitData_type(ctx)

    def visitMethod_decl(self, ctx: CoffeeParser.Method_declContext):
        return super().visitMethod_decl(ctx)

    def visitReturn_type(self, ctx: CoffeeParser.Return_typeContext):
        return super().visitReturn_type(ctx)

    def visitParam(self, ctx: CoffeeParser.ParamContext):
        return super().visitParam(ctx)

    def visitBlock(self, ctx: CoffeeParser.BlockContext):
        return super().visitBlock(ctx)

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

    def visitExpr(self, ctx: CoffeeParser.ExprContext):
        return super().visitExpr(ctx)

    def visitAssign_op(self, ctx: CoffeeParser.Assign_opContext):
        return super().visitAssign_op(ctx)

    def visitLiteral(self, ctx: CoffeeParser.LiteralContext):
        return super().visitLiteral(ctx)

    def visitBool_lit(self, ctx: CoffeeParser.Bool_litContext):
        return super().visitBool_lit(ctx)

    def visitLocation(self, ctx: CoffeeParser.LocationContext):
        return super().visitLocation(ctx)

    def visitLimit(self, ctx: CoffeeParser.LimitContext):
        return super().visitLimit(ctx)

    def visitLow(self, ctx: CoffeeParser.LowContext):
        return super().visitLow(ctx)

    def visitHigh(self, ctx: CoffeeParser.HighContext):
        return super().visitHigh(ctx)

    def visitStep(self, ctx: CoffeeParser.StepContext):
        return super().visitStep(ctx)


#load source code
filein = open('./test.coffee', 'r')
source_code = filein.read();
filein.close()

#create a token stream from source code
lexer = CoffeeLexer(antlr.InputStream(source_code))
stream = antlr.CommonTokenStream(lexer)

#parse token stream
parser = CoffeeParser(stream)
tree = parser.program()

#create Coffee Visitor object
visitor = CoffeeTreeVisitor()

#visit nodes from tree root
visitor.visit(tree)
