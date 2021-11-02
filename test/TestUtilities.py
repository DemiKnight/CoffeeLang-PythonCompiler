from dataclasses import dataclass
from typing import List, Any, Dict, Callable

from antlr4 import ParserRuleContext

from CoffeeLang.CoffeeParser import CoffeeParser
from semantics import CoffeeTreeVisitor
import uuid

@dataclass
class TreeVisit:
    method: str
    returnValue: Any = None

def trail_values(values: Dict[str, TreeVisit]) -> List[TreeVisit]:
    return list(values.values())

class StubbedCoffeeTreeVisitor(CoffeeTreeVisitor):
    trail: Dict[str, TreeVisit]

    def _trail_add(self, visit: TreeVisit) -> str:
        setKey = str(uuid.uuid4())
        self.trail[setKey] = visit
        return setKey

    def _handle(self, func_name: str, func_context: ParserRuleContext, func: Callable[..., Any]):
        key = self._trail_add(TreeVisit(func_name, None))
        self.trail[key].returnValue = func(func_context)
        return self.trail[key].returnValue

    def __init__(self):
        self.trail = dict()
        super().__init__()

    def visit(self, tree):
        return self._handle("visit", tree, super().visit)

    def visitProgram(self, ctx: CoffeeParser.ProgramContext):
        return self._handle("visitProgram", ctx, super().visitProgram)

    def visitImport_stmt(self, ctx: CoffeeParser.Import_stmtContext):
        return self._handle("visitImport_stmt", ctx, super().visitImport_stmt)

    def visitGlobal_decl(self, ctx: CoffeeParser.Global_declContext):
        return self._handle("visitGlobal_decl", ctx, super().visitGlobal_decl)

    def visitVar_decl(self, ctx: CoffeeParser.Var_declContext):
        return self._handle("visitVar_decl", ctx, super().visitVar_decl)

    def visitBlock(self, ctx: CoffeeParser.BlockContext):
        return self._handle("visitBlock", ctx, super().visitBlock)

    def visitVar_assign(self, ctx: CoffeeParser.Var_assignContext):
        return self._handle("visitVar_assign", ctx, super().visitVar_assign)

    def visitVar(self, ctx: CoffeeParser.VarContext):
        return self._handle("visitVar", ctx, super().visitVar)

    def visitData_type(self, ctx: CoffeeParser.Data_typeContext):
        return self._handle("visitData_type", ctx, super().visitData_type)

    def visitMethod_decl(self, ctx: CoffeeParser.Method_declContext):
        return self._handle("visitMethod_decl", ctx, super().visitMethod_decl)

    def visitReturn_type(self, ctx: CoffeeParser.Return_typeContext):
        return self._handle("visitReturn_type", ctx, super().visitReturn_type)

    def visitParam(self, ctx: CoffeeParser.ParamContext):
        return self._handle("visitParam", ctx, super().visitParam)

    def visitEval(self, ctx: CoffeeParser.EvalContext):
        return self._handle("visitEval", ctx, super().visitEval)

    def visitAssign(self, ctx: CoffeeParser.AssignContext):
        return self._handle("visitAssign", ctx, super().visitAssign)

    def visitIf(self, ctx: CoffeeParser.IfContext):
        return self._handle("visitIf", ctx, super().visitIf)

    def visitFor(self, ctx: CoffeeParser.ForContext):
        return self._handle("visitFor", ctx, super().visitFor)

    def visitWhile(self, ctx: CoffeeParser.WhileContext):
        return self._handle("visitWhile", ctx, super().visitWhile)

    def visitReturn(self, ctx: CoffeeParser.ReturnContext):
        return self._handle("visitReturn", ctx, super().visitReturn)

    def visitBreak(self, ctx: CoffeeParser.BreakContext):
        return self._handle("visitBreak", ctx, super().visitBreak)

    def visitContinue(self, ctx: CoffeeParser.ContinueContext):
        return self._handle("visitContinue", ctx, super().visitContinue)

    def visitPass(self, ctx: CoffeeParser.PassContext):
        return self._handle("visitPass", ctx, super().visitPass)

    def visitLoop_var(self, ctx: CoffeeParser.Loop_varContext):
        return self._handle("visitLoop_var", ctx, super().visitLoop_var)

    def visitMethod_call(self, ctx: CoffeeParser.Method_callContext):
        return self._handle("visitMethod_call", ctx, super().visitMethod_call)

    def visitExpr(self, ctx: CoffeeParser.ExprContext):
        return self._handle("visitExpr", ctx, super().visitExpr)

    def visitAssign_op(self, ctx: CoffeeParser.Assign_opContext):
        return self._handle("visitAssign_op", ctx, super().visitAssign_op)

    def visitLiteral(self, ctx: CoffeeParser.LiteralContext):
        return self._handle("visitLiteral", ctx, super().visitLiteral)

    def visitBool_lit(self, ctx: CoffeeParser.Bool_litContext):
        return self._handle("visitBool_lit", ctx, super().visitBool_lit)

    def visitLocation(self, ctx: CoffeeParser.LocationContext):
        return self._handle("visitLocation", ctx, super().visitLocation)

    def visitLimit(self, ctx: CoffeeParser.LimitContext):
        return self._handle("visitLimit", ctx, super().visitLimit)

    def visitLow(self, ctx: CoffeeParser.LowContext):
        return self._handle("visitLow", ctx, super().visitLow)

    def visitHigh(self, ctx: CoffeeParser.HighContext):
        return self._handle("visitHigh", ctx, super().visitHigh)

    def visitStep(self, ctx: CoffeeParser.StepContext):
        return self._handle("visitStep", ctx, super().visitStep)
