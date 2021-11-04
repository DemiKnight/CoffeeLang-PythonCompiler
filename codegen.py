from CoffeeLang.CoffeeUtil import SymbolTable, Method
from CoffeeLang.CoffeeVisitor import CoffeeVisitor


class CoffeeTreeVisitor(CoffeeVisitor):
    def __init__(self):
        self.stbl = SymbolTable()
        self.data = '.data\n'
        self.body = '.text\n.global main\n'

    def visitProgram(self, ctx):
        line = ctx.start.line

        method = Method('main', 'int', line)

        self.stbl.pushFrame(method)

        self.stbl.pushMethod(method)

        method.body += method.id + ':\n'
        method.body += 'push %rbp\n'
        method.body += 'movq %rsp, %rbp\n'

        self.visitChildren(ctx)

        if method.has_return == False:
            method.body += 'pop %rbp\n'
            method.body += 'ret\n'

        self.data += method.data
        self.body += method.body

        self.stbl.popFrame()