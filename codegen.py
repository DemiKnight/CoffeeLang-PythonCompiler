# See repo at https://github.com/DemiKnight/CoffeeLang-PythonCompiler
import antlr4 as antlr

from CoffeeLang.CoffeeLexer import CoffeeLexer
from CoffeeLang.CoffeeParser import CoffeeParser
from CoffeeLang.CoffeeUtil import SymbolTable, Method
from CoffeeLang.CoffeeVisitor import CoffeeVisitor


from SemanticsUtils import Assembler, Segment, FunctionOutput, Instr

# Attempt: Task 1 & Task 2
class CoffeeTreeVisitor(CoffeeVisitor):
    def __init__(self):
        self.stbl = SymbolTable()
        self.gen = Assembler()

        self.gen.header.append(Segment("data"))
        self.gen.header.append(Segment("text"))
        self.gen.header.append(Segment("global _main"))

        self.data = '.data\n'
        self.body = '.text\n.global _main\n'

    def visitProgram(self, ctx):
        line = ctx.start.line

        method = Method('main', 'int', line)

        self.stbl.pushFrame(method)
        self.stbl.pushMethod(method)

        self.gen.body.append(FunctionOutput("main"))
        self.gen.body.append(Instr("push", immidate="%rbp"))
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

    def visitMethod_decl(self, ctx: CoffeeParser.Method_declContext):
        method_id = ctx.ID()
        method_line = ctx.start.line
        method_type = ctx.return_type().getText()

        method = Method(method_id, method_type, method_line)
        self.stbl.pushMethod(method)
        self.stbl.pushFrame(method)

        self.body += f'{method_id}:\n'



        return super().visitMethod_decl(ctx)


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

#assembly output code
code = visitor.data + visitor.body
print(code)
print('-'*12)
output = visitor.gen.generate()
print(output)

#save the assembly file
fileout = open('a.s', 'w')
fileout.write(code)
fileout.close()

#assemble and link
# import os
# os.system("gcc a.s -lm ; ./a.out ; echo $?")
