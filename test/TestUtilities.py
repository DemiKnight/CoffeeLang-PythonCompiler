from dataclasses import dataclass
from typing import List, Any

from CoffeeLang.CoffeeParser import CoffeeParser
from semantics import CoffeeTreeVisitor

@dataclass
class TreeVisit:
    method: str
    returnValue: Any


class StubbedCoffeeTreeVisitor(CoffeeTreeVisitor):
    places: List[TreeVisit]

    def __init__(self):
        self.places = list()
        super().__init__()

    def visit(self, tree):
        return_value = super().visit(tree)
        self.places.append(TreeVisit("visit", return_value))
        return return_value

    def visitProgram(self, ctx: CoffeeParser.ProgramContext):
        return_value = super().visitProgram(ctx)
        self.places.append(TreeVisit("visitProgram", return_value))
        return return_value

    def visitImport_stmt(self, ctx: CoffeeParser.Import_stmtContext):
        return_value = super().visitImport_stmt(ctx)
        self.places.append(TreeVisit("visitImport_stmt", return_value))
        return return_value

    def visitGlobal_decl(self, ctx: CoffeeParser.Global_declContext):
        return_value = super().visitGlobal_decl(ctx)
        self.places.append(TreeVisit("visitGlobal_decl", return_value))
        return return_value

    def visitVar_decl(self, ctx: CoffeeParser.Var_declContext):
        return_value = super().visitVar_decl(ctx)
        self.places.append(TreeVisit("visitVar_decl", return_value))
        return return_value

    def visitVar_assign(self, ctx: CoffeeParser.Var_assignContext):
        return_value = super().visitVar_assign(ctx)
        self.places.append(TreeVisit("visitVar_assign", return_value))
        return return_value

    def visitVar(self, ctx: CoffeeParser.VarContext):
        return_value = super().visitVar(ctx)
        self.places.append(TreeVisit("visitVar", return_value))
        return return_value

    def visitData_type(self, ctx: CoffeeParser.Data_typeContext):
        return_value = super().visitData_type(ctx)
        self.places.append(TreeVisit("visitData_type", return_value))
        return return_value

    def visitMethod_decl(self, ctx: CoffeeParser.Method_declContext):
        return_value = super().visitMethod_decl(ctx)
        self.places.append(TreeVisit("visitMethod_decl", return_value))
        return return_value

    def visitReturn_type(self, ctx: CoffeeParser.Return_typeContext):
        return_value = super().visitReturn_type(ctx)
        self.places.append(TreeVisit("visitReturn_type", return_value))
        return return_value

    def visitParam(self, ctx: CoffeeParser.ParamContext):
        return_value = super().visitParam(ctx)
        self.places.append(TreeVisit("visitParam", return_value))
        return return_value

    def visitBlock(self, ctx: CoffeeParser.BlockContext):
        return_value = super().visitBlock(ctx)
        self.places.append(TreeVisit("visitBlock", return_value))
        return return_value

    def visitEval(self, ctx: CoffeeParser.EvalContext):
        return_value = super().visitEval(ctx)
        self.places.append(TreeVisit("visitEval", return_value))
        return return_value

    def visitAssign(self, ctx: CoffeeParser.AssignContext):
        return_value = super().visitAssign(ctx)
        self.places.append(TreeVisit("visitAssign", return_value))
        return return_value

    def visitIf(self, ctx: CoffeeParser.IfContext):
        return_value = super().visitIf(ctx)
        self.places.append(TreeVisit("visitIf", return_value))
        return return_value

    def visitFor(self, ctx: CoffeeParser.ForContext):
        return_value = super().visitFor(ctx)
        self.places.append(TreeVisit("visitFor", return_value))
        return return_value

    def visitWhile(self, ctx: CoffeeParser.WhileContext):
        return_value = super().visitWhile(ctx)
        self.places.append(TreeVisit("visitWhile", return_value))
        return return_value

    def visitReturn(self, ctx: CoffeeParser.ReturnContext):
        return_value = super().visitReturn(ctx)
        self.places.append(TreeVisit("visitReturn", return_value))
        return return_value

    def visitBreak(self, ctx: CoffeeParser.BreakContext):
        return_value = super().visitBreak(ctx)
        self.places.append(TreeVisit("visitBreak", return_value))
        return return_value

    def visitContinue(self, ctx: CoffeeParser.ContinueContext):
        return_value = super().visitContinue(ctx)
        self.places.append(TreeVisit("visitContinue", return_value))
        return return_value

    def visitPass(self, ctx: CoffeeParser.PassContext):
        return_value = super().visitPass(ctx)
        self.places.append(TreeVisit("visitPass", return_value))
        return return_value

    def visitLoop_var(self, ctx: CoffeeParser.Loop_varContext):
        return_value = super().visitLoop_var(ctx)
        self.places.append(TreeVisit("visitLoop_var", return_value))
        return return_value

    def visitMethod_call(self, ctx: CoffeeParser.Method_callContext):
        return_value = super().visitMethod_call(ctx)
        self.places.append(TreeVisit("visitMethod_call", return_value))
        return return_value

    def visitExpr(self, ctx: CoffeeParser.ExprContext):
        return_value = super().visitExpr(ctx)
        self.places.append(TreeVisit("visitExpr", return_value))
        return return_value

    def visitAssign_op(self, ctx: CoffeeParser.Assign_opContext):
        return_value = super().visitAssign_op(ctx)
        self.places.append(TreeVisit("visitAssign_op", return_value))
        return return_value

    def visitLiteral(self, ctx: CoffeeParser.LiteralContext):
        return_value = super().visitLiteral(ctx)
        self.places.append(TreeVisit("visitLiteral", return_value))
        return return_value

    def visitBool_lit(self, ctx: CoffeeParser.Bool_litContext):
        return_value = super().visitBool_lit(ctx)
        self.places.append(TreeVisit("visitBool_lit", return_value))
        return return_value

    def visitLocation(self, ctx: CoffeeParser.LocationContext):
        return_value = super().visitLocation(ctx)
        self.places.append(TreeVisit("visitLocation", return_value))
        return return_value

    def visitLimit(self, ctx: CoffeeParser.LimitContext):
        return_value = super().visitLimit(ctx)
        self.places.append(TreeVisit("visitLimit", return_value))
        return return_value

    def visitLow(self, ctx: CoffeeParser.LowContext):
        return_value = super().visitLow(ctx)
        self.places.append(TreeVisit("visitLow", return_value))
        return return_value

    def visitHigh(self, ctx: CoffeeParser.HighContext):
        return_value = super().visitHigh(ctx)
        self.places.append(TreeVisit("visitHigh", return_value))
        return return_value

    def visitStep(self, ctx: CoffeeParser.StepContext):
        return_value = super().visitStep(ctx)
        self.places.append(TreeVisit("visitStep", return_value))
        return return_value
