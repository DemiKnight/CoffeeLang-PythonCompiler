from typing import List

from CoffeeLang.CoffeeParser import CoffeeParser
from semantics import CoffeeTreeVisitor


class StubbedCoffeeTreeVisitor(CoffeeTreeVisitor):
    visitedPlaces: List[str]

    def __init__(self):
        self.visitedPlaces = list()
        super().__init__()

    def visit(self, tree):
        self.visitedPlaces += "visit"
        return super().visit(tree)

    def visitProgram(self, ctx: CoffeeParser.ProgramContext):
        self.visitedPlaces += "visitProgram"
        super().visitProgram(ctx)

    def visitImport_stmt(self, ctx: CoffeeParser.Import_stmtContext):
        self.visitedPlaces += "visitImport_stmt"
        return super().visitImport_stmt(ctx)

    def visitGlobal_decl(self, ctx: CoffeeParser.Global_declContext):
        self.visitedPlaces += "visitGlobal_decl"
        return super().visitGlobal_decl(ctx)

    def visitVar_decl(self, ctx: CoffeeParser.Var_declContext):
        self.visitedPlaces += "visitVar_decl"
        return super().visitVar_decl(ctx)

    def visitVar_assign(self, ctx: CoffeeParser.Var_assignContext):
        self.visitedPlaces += "visitVar_assign"
        return super().visitVar_assign(ctx)

    def visitVar(self, ctx: CoffeeParser.VarContext):
        self.visitedPlaces += "visitVar"
        return super().visitVar(ctx)

    def visitData_type(self, ctx: CoffeeParser.Data_typeContext):
        self.visitedPlaces += "visitData_type"
        return super().visitData_type(ctx)

    def visitMethod_decl(self, ctx: CoffeeParser.Method_declContext):
        self.visitedPlaces += "visitMethod_decl"
        return super().visitMethod_decl(ctx)

    def visitReturn_type(self, ctx: CoffeeParser.Return_typeContext):
        self.visitedPlaces += "visitReturn_type"
        return super().visitReturn_type(ctx)

    def visitParam(self, ctx: CoffeeParser.ParamContext):
        self.visitedPlaces += "visitParam"
        return super().visitParam(ctx)

    def visitBlock(self, ctx: CoffeeParser.BlockContext):
        self.visitedPlaces += "visitBlock"
        return super().visitBlock(ctx)

    def visitEval(self, ctx: CoffeeParser.EvalContext):
        self.visitedPlaces += "visitEval"
        return super().visitEval(ctx)

    def visitAssign(self, ctx: CoffeeParser.AssignContext):
        self.visitedPlaces += "visitAssign"
        return super().visitAssign(ctx)

    def visitIf(self, ctx: CoffeeParser.IfContext):
        self.visitedPlaces += "visitIf"
        return super().visitIf(ctx)

    def visitFor(self, ctx: CoffeeParser.ForContext):
        self.visitedPlaces += "visitFor"
        return super().visitFor(ctx)

    def visitWhile(self, ctx: CoffeeParser.WhileContext):
        self.visitedPlaces += "visitWhile"
        return super().visitWhile(ctx)

    def visitReturn(self, ctx: CoffeeParser.ReturnContext):
        self.visitedPlaces += "visitReturn"
        return super().visitReturn(ctx)

    def visitBreak(self, ctx: CoffeeParser.BreakContext):
        self.visitedPlaces += "visitBreak"
        return super().visitBreak(ctx)

    def visitContinue(self, ctx: CoffeeParser.ContinueContext):
        self.visitedPlaces += "visitContinue"
        return super().visitContinue(ctx)

    def visitPass(self, ctx: CoffeeParser.PassContext):
        self.visitedPlaces += "visitPass"
        return super().visitPass(ctx)

    def visitLoop_var(self, ctx: CoffeeParser.Loop_varContext):
        self.visitedPlaces += "visitLoop_var"
        return super().visitLoop_var(ctx)

    def visitMethod_call(self, ctx: CoffeeParser.Method_callContext):
        self.visitedPlaces += "visitMethod_call"
        return super().visitMethod_call(ctx)

    def visitExpr(self, ctx: CoffeeParser.ExprContext):
        self.visitedPlaces += "visitExpr"
        return super().visitExpr(ctx)

    def visitAssign_op(self, ctx: CoffeeParser.Assign_opContext):
        self.visitedPlaces += "visitAssign_op"
        return super().visitAssign_op(ctx)

    def visitLiteral(self, ctx: CoffeeParser.LiteralContext):
        self.visitedPlaces += "visitLiteral"
        return super().visitLiteral(ctx)

    def visitBool_lit(self, ctx: CoffeeParser.Bool_litContext):
        self.visitedPlaces += "visitBool_lit"
        return super().visitBool_lit(ctx)

    def visitLocation(self, ctx: CoffeeParser.LocationContext):
        self.visitedPlaces += "visitLocation"
        return super().visitLocation(ctx)

    def visitLimit(self, ctx: CoffeeParser.LimitContext):
        self.visitedPlaces += "visitLimit"
        return super().visitLimit(ctx)

    def visitLow(self, ctx: CoffeeParser.LowContext):
        self.visitedPlaces += "visitLow"
        return super().visitLow(ctx)

    def visitHigh(self, ctx: CoffeeParser.HighContext):
        self.visitedPlaces += "visitHigh"
        return super().visitHigh(ctx)

    def visitStep(self, ctx: CoffeeParser.StepContext):
        self.visitedPlaces += "visitStep"
        return super().visitStep(ctx)
