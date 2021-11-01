from dataclasses import dataclass
from typing import List, Any, Dict, Callable

from antlr4 import ParserRuleContext

from CoffeeLang.CoffeeParser import CoffeeParser
from semantics import CoffeeTreeVisitor
import uuid

@dataclass
class TreeVisit:
    method: str
    returnValue: Any


class StubbedCoffeeTreeVisitor(CoffeeTreeVisitor):
    places: List[TreeVisit]
    trail: Dict[str, TreeVisit]

    def _trail_add(self, visit: TreeVisit) -> str:
        setKey = str(uuid.uuid4())
        self.trail[setKey] = visit
        return setKey

    def _handle(self, func_name: str, func_context: ParserRuleContext, func: Callable[..., Any]):
        key = self._trail_add(TreeVisit(func_name, None))
        self.trail[key].returnValue = func(func_context)
        return self.trail[key].returnValue

    def places_order(self):
        return self.places.reverse()

    def __init__(self):
        self.places = list()
        self.trail = dict()
        super().__init__()

    def visit(self, tree):
        self.places.append(TreeVisit("visit", None))

        return self._handle("visit", tree, super().visit)

        # key = self._trail_add(TreeVisit("visit", None))
        # self.trail[key].returnValue = super().visit(tree)

    def visitProgram(self, ctx: CoffeeParser.ProgramContext):
        self.places.append(TreeVisit("visitProgram", None))

        return self._handle("visitProgram", ctx, super().visitProgram)
        # key = self._trail_add(TreeVisit("visitProgram", None))
        # self.trail[key].returnValue = super().visitProgram(ctx)

    def visitImport_stmt(self, ctx: CoffeeParser.Import_stmtContext):
        key = self._trail_add(TreeVisit("visitImport_stmt", None))

        return self._handle("visitImport_stmt", ctx, super().visitImport_stmt)
        # self.trail[key].returnValue = super().visitImport_stmt(ctx)
        # return self.trail[key].returnValue

    def visitGlobal_decl(self, ctx: CoffeeParser.Global_declContext):
        self.places.append(TreeVisit("visitGlobal_decl", None))

        return self._handle("visitGlobal_decl", ctx, super().visitGlobal_decl)

        # key = self._trail_add(TreeVisit("visitGlobal_decl", None))
        # self.trail[key].returnValue = super().visitGlobal_decl(ctx)
        # return self.trail[key].returnValue

    def visitVar_decl(self, ctx: CoffeeParser.Var_declContext):
        self.places.append(TreeVisit("visitVar_decl", None))
        return self._handle("visitVar_decl", ctx, super().visitVar_decl)
        # key = self._trail_add(TreeVisit("visitVar_decl", None))
        # self.trail[key].returnValue = super().visitVar_decl(ctx)
        # return self.trail[key].returnValue

    def visitBlock(self, ctx: CoffeeParser.BlockContext):
        self.places.append(TreeVisit("visitBlock", None))
        return self._handle("visitBlock", ctx, super().visitBlock)
        # super().visitBlock(ctx)

    def visitVar_assign(self, ctx: CoffeeParser.Var_assignContext):
        # return_value = super().visitVar_assign(ctx)
        return self._handle("visitVar_assign", ctx, super().visitVar_assign)
        # self.places.append(TreeVisit("visitVar_assign", return_value))
        # return return_value

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
