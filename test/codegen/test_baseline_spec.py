import textwrap

from codegen import CoffeeTreeVisitorGen
from test.VisitorSpec import createTree


def test_default_output():
    target = CoffeeTreeVisitorGen()
    test_prog = createTree("""""")

    target.visit(test_prog)
    expected_value = textwrap.dedent(".data\n"
                                     ".text\n"
                                     ".global main\n"
                                     "main:\n"
                                     "push %rbp\n"
                                     "movq %rsp, %rbp\n"
                                     "pop %rbp\n"
                                     "ret\n")


    assert target.data + target.body == expected_value
