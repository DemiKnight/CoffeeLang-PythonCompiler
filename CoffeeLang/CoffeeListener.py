# Generated from ./Coffee.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CoffeeParser import CoffeeParser
else:
    from CoffeeParser import CoffeeParser

# This class defines a complete listener for a parse tree produced by CoffeeParser.
class CoffeeListener(ParseTreeListener):

    # Enter a parse tree produced by CoffeeParser#program.
    def enterProgram(self, ctx:CoffeeParser.ProgramContext):
        pass

    # Exit a parse tree produced by CoffeeParser#program.
    def exitProgram(self, ctx:CoffeeParser.ProgramContext):
        pass


    # Enter a parse tree produced by CoffeeParser#import_stmt.
    def enterImport_stmt(self, ctx:CoffeeParser.Import_stmtContext):
        pass

    # Exit a parse tree produced by CoffeeParser#import_stmt.
    def exitImport_stmt(self, ctx:CoffeeParser.Import_stmtContext):
        pass


    # Enter a parse tree produced by CoffeeParser#global_decl.
    def enterGlobal_decl(self, ctx:CoffeeParser.Global_declContext):
        pass

    # Exit a parse tree produced by CoffeeParser#global_decl.
    def exitGlobal_decl(self, ctx:CoffeeParser.Global_declContext):
        pass


    # Enter a parse tree produced by CoffeeParser#var_decl.
    def enterVar_decl(self, ctx:CoffeeParser.Var_declContext):
        pass

    # Exit a parse tree produced by CoffeeParser#var_decl.
    def exitVar_decl(self, ctx:CoffeeParser.Var_declContext):
        pass


    # Enter a parse tree produced by CoffeeParser#var_assign.
    def enterVar_assign(self, ctx:CoffeeParser.Var_assignContext):
        pass

    # Exit a parse tree produced by CoffeeParser#var_assign.
    def exitVar_assign(self, ctx:CoffeeParser.Var_assignContext):
        pass


    # Enter a parse tree produced by CoffeeParser#var.
    def enterVar(self, ctx:CoffeeParser.VarContext):
        pass

    # Exit a parse tree produced by CoffeeParser#var.
    def exitVar(self, ctx:CoffeeParser.VarContext):
        pass


    # Enter a parse tree produced by CoffeeParser#data_type.
    def enterData_type(self, ctx:CoffeeParser.Data_typeContext):
        pass

    # Exit a parse tree produced by CoffeeParser#data_type.
    def exitData_type(self, ctx:CoffeeParser.Data_typeContext):
        pass


    # Enter a parse tree produced by CoffeeParser#method_decl.
    def enterMethod_decl(self, ctx:CoffeeParser.Method_declContext):
        pass

    # Exit a parse tree produced by CoffeeParser#method_decl.
    def exitMethod_decl(self, ctx:CoffeeParser.Method_declContext):
        pass


    # Enter a parse tree produced by CoffeeParser#return_type.
    def enterReturn_type(self, ctx:CoffeeParser.Return_typeContext):
        pass

    # Exit a parse tree produced by CoffeeParser#return_type.
    def exitReturn_type(self, ctx:CoffeeParser.Return_typeContext):
        pass


    # Enter a parse tree produced by CoffeeParser#param.
    def enterParam(self, ctx:CoffeeParser.ParamContext):
        pass

    # Exit a parse tree produced by CoffeeParser#param.
    def exitParam(self, ctx:CoffeeParser.ParamContext):
        pass


    # Enter a parse tree produced by CoffeeParser#block.
    def enterBlock(self, ctx:CoffeeParser.BlockContext):
        pass

    # Exit a parse tree produced by CoffeeParser#block.
    def exitBlock(self, ctx:CoffeeParser.BlockContext):
        pass


    # Enter a parse tree produced by CoffeeParser#eval.
    def enterEval(self, ctx:CoffeeParser.EvalContext):
        pass

    # Exit a parse tree produced by CoffeeParser#eval.
    def exitEval(self, ctx:CoffeeParser.EvalContext):
        pass


    # Enter a parse tree produced by CoffeeParser#assign.
    def enterAssign(self, ctx:CoffeeParser.AssignContext):
        pass

    # Exit a parse tree produced by CoffeeParser#assign.
    def exitAssign(self, ctx:CoffeeParser.AssignContext):
        pass


    # Enter a parse tree produced by CoffeeParser#if.
    def enterIf(self, ctx:CoffeeParser.IfContext):
        pass

    # Exit a parse tree produced by CoffeeParser#if.
    def exitIf(self, ctx:CoffeeParser.IfContext):
        pass


    # Enter a parse tree produced by CoffeeParser#for.
    def enterFor(self, ctx:CoffeeParser.ForContext):
        pass

    # Exit a parse tree produced by CoffeeParser#for.
    def exitFor(self, ctx:CoffeeParser.ForContext):
        pass


    # Enter a parse tree produced by CoffeeParser#while.
    def enterWhile(self, ctx:CoffeeParser.WhileContext):
        pass

    # Exit a parse tree produced by CoffeeParser#while.
    def exitWhile(self, ctx:CoffeeParser.WhileContext):
        pass


    # Enter a parse tree produced by CoffeeParser#return.
    def enterReturn(self, ctx:CoffeeParser.ReturnContext):
        pass

    # Exit a parse tree produced by CoffeeParser#return.
    def exitReturn(self, ctx:CoffeeParser.ReturnContext):
        pass


    # Enter a parse tree produced by CoffeeParser#break.
    def enterBreak(self, ctx:CoffeeParser.BreakContext):
        pass

    # Exit a parse tree produced by CoffeeParser#break.
    def exitBreak(self, ctx:CoffeeParser.BreakContext):
        pass


    # Enter a parse tree produced by CoffeeParser#continue.
    def enterContinue(self, ctx:CoffeeParser.ContinueContext):
        pass

    # Exit a parse tree produced by CoffeeParser#continue.
    def exitContinue(self, ctx:CoffeeParser.ContinueContext):
        pass


    # Enter a parse tree produced by CoffeeParser#pass.
    def enterPass(self, ctx:CoffeeParser.PassContext):
        pass

    # Exit a parse tree produced by CoffeeParser#pass.
    def exitPass(self, ctx:CoffeeParser.PassContext):
        pass


    # Enter a parse tree produced by CoffeeParser#loop_var.
    def enterLoop_var(self, ctx:CoffeeParser.Loop_varContext):
        pass

    # Exit a parse tree produced by CoffeeParser#loop_var.
    def exitLoop_var(self, ctx:CoffeeParser.Loop_varContext):
        pass


    # Enter a parse tree produced by CoffeeParser#method_call.
    def enterMethod_call(self, ctx:CoffeeParser.Method_callContext):
        pass

    # Exit a parse tree produced by CoffeeParser#method_call.
    def exitMethod_call(self, ctx:CoffeeParser.Method_callContext):
        pass


    # Enter a parse tree produced by CoffeeParser#expr.
    def enterExpr(self, ctx:CoffeeParser.ExprContext):
        pass

    # Exit a parse tree produced by CoffeeParser#expr.
    def exitExpr(self, ctx:CoffeeParser.ExprContext):
        pass


    # Enter a parse tree produced by CoffeeParser#assign_op.
    def enterAssign_op(self, ctx:CoffeeParser.Assign_opContext):
        pass

    # Exit a parse tree produced by CoffeeParser#assign_op.
    def exitAssign_op(self, ctx:CoffeeParser.Assign_opContext):
        pass


    # Enter a parse tree produced by CoffeeParser#literal.
    def enterLiteral(self, ctx:CoffeeParser.LiteralContext):
        pass

    # Exit a parse tree produced by CoffeeParser#literal.
    def exitLiteral(self, ctx:CoffeeParser.LiteralContext):
        pass


    # Enter a parse tree produced by CoffeeParser#bool_lit.
    def enterBool_lit(self, ctx:CoffeeParser.Bool_litContext):
        pass

    # Exit a parse tree produced by CoffeeParser#bool_lit.
    def exitBool_lit(self, ctx:CoffeeParser.Bool_litContext):
        pass


    # Enter a parse tree produced by CoffeeParser#location.
    def enterLocation(self, ctx:CoffeeParser.LocationContext):
        pass

    # Exit a parse tree produced by CoffeeParser#location.
    def exitLocation(self, ctx:CoffeeParser.LocationContext):
        pass


    # Enter a parse tree produced by CoffeeParser#limit.
    def enterLimit(self, ctx:CoffeeParser.LimitContext):
        pass

    # Exit a parse tree produced by CoffeeParser#limit.
    def exitLimit(self, ctx:CoffeeParser.LimitContext):
        pass


    # Enter a parse tree produced by CoffeeParser#low.
    def enterLow(self, ctx:CoffeeParser.LowContext):
        pass

    # Exit a parse tree produced by CoffeeParser#low.
    def exitLow(self, ctx:CoffeeParser.LowContext):
        pass


    # Enter a parse tree produced by CoffeeParser#high.
    def enterHigh(self, ctx:CoffeeParser.HighContext):
        pass

    # Exit a parse tree produced by CoffeeParser#high.
    def exitHigh(self, ctx:CoffeeParser.HighContext):
        pass


    # Enter a parse tree produced by CoffeeParser#step.
    def enterStep(self, ctx:CoffeeParser.StepContext):
        pass

    # Exit a parse tree produced by CoffeeParser#step.
    def exitStep(self, ctx:CoffeeParser.StepContext):
        pass



del CoffeeParser