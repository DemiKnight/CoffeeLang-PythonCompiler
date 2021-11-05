from CoffeeLang.CoffeeParser import CoffeeParser
from CoffeeLang.CoffeeUtil import SymbolTable, Method, Var
from CoffeeLang.CoffeeVisitor import CoffeeVisitor


# Tasks
# Task 1 - Expressions
#   - Issue with negation
# Task 3 - Loops
#   - Causes an infinite loop
# Changes
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

        self.visitChildren(ctx)

        if not method.has_return:
            method.body += 'pop %rbp\n'
            method.body += 'ret\n'

        self.data += method.data
        self.body += method.body

        self.stbl.popFrame()

    def visitMethod_call(self, ctx: CoffeeParser.Method_callContext):
        method_ctx: Method = self.stbl.getMethodContext()

        for index in range(len(ctx.expr())):
            self.visit(ctx.expr(index))  # Value stored in %rax

            # Prevent out of bound index
            if index < len(self.stbl.param_reg):
                method_ctx.body += f"movq %rax, {self.stbl.param_reg[index]}\n"

        method_ctx.body += f"addq ${self.stbl.getStackPtr()}, %rsp\n"
        method_ctx.body += f"call {ctx.ID().getText()}\n"
        method_ctx.body += f"subq ${self.stbl.getStackPtr()}, %rsp\n"

    def visitMethod_decl(self, ctx: CoffeeParser.Method_declContext):
        line_number = ctx.start.line
        method_id = ctx.ID().getText()
        method_type = ctx.return_type().getText()

        # Prep start of function
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

            # Add parameters to Symbol Table
            param = Var(param_id, param_type, param_size, Var.LOCAL, param_is_array, line_number)
            method_def.pushParam(param_type)
            self.stbl.pushVar(param)

            # Prevent out of bound index & gather parameters from registries
            if index < len(self.stbl.param_reg):
                method_def.body += f"movq {self.stbl.param_reg[index]}, {str(param.addr)}(%rbp)\n"

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

    def visitReturn(self, ctx: CoffeeParser.ReturnContext):
        self.visit(ctx.expr())

    def visitLiteral(self, ctx: CoffeeParser.LiteralContext):
        if ctx.INT_LIT() is not None:
            methodCTx: Method = self.stbl.getMethodContext()
            methodCTx.body += f"movq ${ctx.INT_LIT()}, %rax\n"

    def visitLocation(self, ctx: CoffeeParser.LocationContext):
        methodCtx: Method = self.stbl.getMethodContext()
        location_id = ctx.ID().getText()

        var: Var = self.stbl.find(location_id)

        # Get value from location and store it within %rax
        if var.scope == Var.GLOBAL:
            methodCtx.body += f"movq {var.id}(%rip), %rax\n"
            pass
        else:  # Only other scope is Local...
            methodCtx.body += f"movq {var.addr}(%rbp), %rax\n"

    def visitAssign(self, ctx: CoffeeParser.AssignContext):
        self.visit(ctx.expr())  # Value stored in %rax

        methodCtx: Method = self.stbl.getMethodContext()
        location_id = ctx.location().ID().getText()

        var: Var = self.stbl.find(location_id)

        # Assign value stored in %rax to local or global variable
        if var.scope == Var.GLOBAL:
            methodCtx.body += f"movq %rax, {var.id}(%rip)\n"
        else:  # Only other scope is Local...
            methodCtx.body += f"movq %rax, {var.addr}(%rbp)\n"

    def visitExpr(self, ctx: CoffeeParser.ExprContext):
        if ctx.literal() is not None:
            return self.visit(ctx.literal())
        elif ctx.location() is not None:
            return self.visit(ctx.location())
        elif len(ctx.expr()) == 2:
            method_ctx: Method = self.stbl.getMethodContext()

            # Store value on stack to prevent over-writing on nested expressions
            self.visit(ctx.expr(0))
            self.stbl.pushBytes(8)
            method_ctx.body += f"movq %rax, {self.stbl.getStackPtr()}(%rsp)\n"

            result2 = self.visit(ctx.expr(1))
            method_ctx.body += f"movq %rax, %r11\n"

            # Retrieve from stack.
            method_ctx.body += f"movq {self.stbl.getStackPtr()}(%rsp), %r10\n"
            self.stbl.popBytes(8)

            if ctx.ADD() is not None:
                method_ctx.body += "addq %r10, %r11\n"
                method_ctx.body += "movq %r11, %rax\n"
            elif ctx.SUB() is not None:
                method_ctx.body += "subq %r11, %r10\n"
                method_ctx.body += "movq %r10, %rax\n"

            elif ctx.DIV() is not None:
                method_ctx.body += "movq %r10, %rax\n"
                method_ctx.body += "movq $0, %rdx\n"
                method_ctx.body += "idiv %r11\n"
            elif ctx.MUL() is not None:
                method_ctx.body += "imul %r10, %r11\n"
                method_ctx.body += "movq %r11, %rax\n"
                pass
            elif ctx.MOD() is not None:
                method_ctx.body += "movq %r10, %rax\n"
                method_ctx.body += "movq $0, %rdx\n"
                method_ctx.body += "idiv %r11\n"
                method_ctx.body += "movq %rdx, %rax\n"
                pass
        elif ctx.SUB() is not None:  # Negation (e.g. -10)
            # There is an issue present the makes this return an incorrect answer.
            method_ctx: Method = self.stbl.getMethodContext()
            method_ctx.body += "neg %rax\n"
        else:
            return self.visitChildren(ctx)

    def visitBlock(self, ctx: CoffeeParser.BlockContext):
        self.visitChildren(ctx)

    def visitGlobal_decl(self, ctx: CoffeeParser.Global_declContext):
        method_ctx: Method = self.stbl.getMethodContext()
        line_number = ctx.start.line

        for index in range(len(ctx.var_decl().var_assign())):
            variable_decl: CoffeeParser.VarContext = ctx.var_decl().var_assign(index).var()
            variable_id = variable_decl.ID().getText()

            variable_type = self.visit(ctx.var_decl().var_assign(index).expr()) \
                if ctx.var_decl().var_assign(index).expr() is not None else None

            variable_is_array = variable_decl.INT_LIT() is not None
            variable_size = int(variable_decl.INT_LIT().getText()) * 8 if variable_is_array else 8

            # Push global variable to .data section & Symbol table
            variable_def = Var(variable_id, variable_type, variable_size, Var.GLOBAL, variable_is_array, line_number)
            self.stbl.pushVar(variable_def)
            method_ctx.data += f".comm {variable_id},{variable_size}\n"

    def visitFor(self, ctx: CoffeeParser.ForContext):
        method_ctx: Method = self.stbl.getMethodContext()
        start_label = self.stbl.getNextLabel()
        end_label = self.stbl.getNextLabel()

        self.stbl.pushScope()

        loop_var_id = ctx.loop_var().getText()

        loop_variable = Var(loop_var_id, "int", 8, Var.LOCAL, False, ctx.start.line)
        self.stbl.pushVar(loop_variable)

        low_variable = Var("lowVar", "int", 8, Var.LOCAL, False, ctx.start.line)
        self.stbl.pushVar(low_variable)
        self.visit(ctx.limit().low().expr())
        method_ctx.body += f"movq %rax, {str(low_variable.addr)}(%rsp)\n"

        high_variable = Var("highVar", "int", 8, Var.LOCAL, False, ctx.start.line)
        self.stbl.pushVar(high_variable)
        self.visit(ctx.limit().high().expr())
        method_ctx.body += f"movq %rax, {str(high_variable.addr)}(%rsp)\n"

        step_variable = Var("stepVar", "int", 8, Var.LOCAL, False, ctx.start.line)
        self.stbl.pushVar(step_variable)
        self.visit(ctx.limit().step().expr())
        method_ctx.body += f"movq %rax, {str(step_variable.addr)}(%rsp)\n"

        # Initialise loop variable
        method_ctx.body += f"movq {str(low_variable.addr)}(%rsp), %rax\n"
        method_ctx.body += f"movq %rax, {str(loop_variable.addr)}(%rsp)\n"

        method_ctx.body += f"{start_label}:\n"

        self.visit(ctx.block())

        # Increment loop variable by step.
        method_ctx.body += f"movq {str(loop_variable.addr)}(%rbp), %rax\n"
        method_ctx.body += f"movq {str(step_variable.addr)}(%rbp), %r11\n"
        method_ctx.body += f"addq %rax, %r11\n"
        method_ctx.body += f"movq %rax, {str(loop_variable.addr)}(%rbp)\n"

        method_ctx.body += f"movq {str(high_variable.addr)}(%rbp), %r10\n"
        # Compare loop variable to high_variable/boundary,
        # If loop variable is greater than or equal to the boundary, exit loop.
        method_ctx.body += f"cmp %r10, %rax\n"
        method_ctx.body += f"jge {end_label}\n"
        method_ctx.body += f"jmp {start_label}\n"

        method_ctx.body += f"{end_label}:\n"
        self.stbl.popScope()
