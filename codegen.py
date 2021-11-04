from CoffeeLang.CoffeeParser import CoffeeParser
from CoffeeLang.CoffeeUtil import SymbolTable, Method, Var
from CoffeeLang.CoffeeVisitor import CoffeeVisitor


# Tasks
# Task 1 - Expressions
# Task 2 - Methods
# Changes
# main -> _main
# global -> globl
class CoffeeTreeVisitorGen(CoffeeVisitor):
    body: str
    data: str

    def __init__(self):
        self.stbl = SymbolTable()
        self.data = '.data\n'
        self.body = '.text\n.globl _main\n'

    def visitProgram(self, ctx):
        line = ctx.start.line

        method = Method('_main', 'int', line)

        self.stbl.pushFrame(method)
        self.stbl.pushMethod(method)

        method.body += method.id + ':\n'
        method.body += 'push %rbp\n'
        method.body += 'movq %rsp, %rbp\n'
        method.body += 'movl $3, %eax\n'  # Todo remove when sorting return
        method.body += 'popq %rbp\n'

        self.visitChildren(ctx)

        if not method.has_return:
            method.body += 'pop %rbp\n'
            method.body += 'ret\n'

        self.data += method.data
        self.body += method.body

        self.stbl.popFrame()

    def visitMethod_call(self, ctx: CoffeeParser.Method_callContext):
        return super().visitMethod_call(ctx)

    def visitMethod_decl(self, ctx: CoffeeParser.Method_declContext):
        line_number = ctx.start.line
        method_id = ctx.ID().getText()
        method_type = ctx.return_type().getText()

        method_def = Method(method_id, method_type, line_number)

        self.stbl.pushMethod(method_def)
        self.stbl.pushFrame(method_def)

        method_def.body += (f"{method_id}:\n"
                            "push %rbp\n"
                            "movq %rsp, %rbp\n")

        for index in range(len(ctx.param())):
            param_id = ctx.param(index).ID().getText()
            param_type = ctx.param(index).data_type().getText()
            param_size = 8
            param_is_array = False

            param = Var(param_id, param_type, param_size, Var.LOCAL, param_is_array, line_number)
            method_def.pushParam(param_type)
            self.stbl.pushVar(param)

            if index < len(self.stbl.param_reg):
                method_def.body += f"movq {self.stbl.param_reg[index]}, {str(param.addr)}(%rbp)\n"
            else:
                print("TODO")

            # breakpoint()

        if ctx.block() is not None:
            self.visit(ctx.block())
        else:  # Must be an expression
            self.visit(ctx.expr())

        if not method_def.has_return:
            method_def.body += 'pop %rbp\n'
            method_def.body += 'ret\n'

        self.body += method_def.body
        self.data += method_def.data

        self.stbl.popFrame()

    def visitLiteral(self, ctx:CoffeeParser.LiteralContext):
        if ctx.INT_LIT() is not None:
            methodCTx: Method = self.stbl.getMethodContext()
            methodCTx.body += f"movq ${ctx.INT_LIT()}, %rax\n"
            breakpoint()

            return ctx.INT_LIT()

    def visitLocation(self, ctx: CoffeeParser.LocationContext):
        methodCtx: Method = self.stbl.getMethodContext()
        location_id = ctx.ID().getText()

        var: Var = self.stbl.find(location_id)

        if(var.scope == Var.GLOBAL):
            pass
        else:  # Only other scope is Local...
            methodCtx.body += f"movq {var.addr}(%rbp), %rax\n"

        return super().visitLocation(ctx)

    def visitExpr(self, ctx:CoffeeParser.ExprContext):
        if ctx.literal() is not None:
            return self.visit(ctx.literal())
        elif ctx.location() is not None:
            return self.visit(ctx.location())
        else:
            return self.visitChildren(ctx)

    def visitBlock(self, ctx:CoffeeParser.BlockContext):
        if ctx.LCURLY() is not None:
            method_ctx = self.stbl.getMethodContext()
            method_ctx.body += "# lol\n"

        self.visitChildren(ctx)
