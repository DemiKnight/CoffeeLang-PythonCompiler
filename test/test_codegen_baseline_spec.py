import os

import pytest

from codegen import CoffeeTreeVisitorGen
from test.VisitorSpec import createTree

outputFile = "/Users/alexknight/projects/personal/pyAntlr/test/a"
compilerCmd = f"gcc-11 {outputFile}.s -lm; {outputFile}.out; echo $?"


# compilerCmd = f"gcc-11 {outputFile} -lm; echo $?"


def executeTestCode(assembly: str) -> str:
    print(assembly.format())
    fileout = open(f"{outputFile}.s", "w")
    fileout.write(assembly)
    fileout.close()
    returnValue = os.popen(compilerCmd).read().strip()
    print(f"return Code: {returnValue}")
    # breakpoint()
    return returnValue


def test_default_output():
    target = CoffeeTreeVisitorGen()
    test_prog = createTree("""
    int inc(int a) {
      return a + 1;
    }
    return inc(2);
    """)

    target.visit(test_prog)
    expected_value = (
        ".text\n"
        ".globl _main\n"
        "_main:\n"
        "push %rbp\n"
        "movq %rsp, %rbp\n"
        "pop %rbp\n"
        "ret\n")

    # assert target.data + target.body == expected_value
    assert executeTestCode(target.data + target.body) == "3"


def test_expr_add():
    target = CoffeeTreeVisitorGen()
    test_prog = createTree("""
    return 2 + 3; 
    """)
    target.visit(test_prog)

    assert executeTestCode(target.data + target.body) == "5"


def test_expr_mul():
    target = CoffeeTreeVisitorGen()
    test_prog = createTree("""
    return 2 * 6; 
    """)
    target.visit(test_prog)

    assert executeTestCode(target.data + target.body) == "12"


def test_expr_basic():
    target = CoffeeTreeVisitorGen()
    test_prog = createTree("""
    return 2 + 3 * 4; 
    """)
    target.visit(test_prog)

    assert executeTestCode(target.data + target.body) == "14"


def test_expr_2_basic():
    target = CoffeeTreeVisitorGen()
    test_prog = createTree("""
    return 20 - 11; 
    """)
    target.visit(test_prog)

    assert executeTestCode(target.data + target.body) == "9"


def test_expr_mod():
    target = CoffeeTreeVisitorGen()
    test_prog = createTree("""
    return 20 % 6; 
    """)
    target.visit(test_prog)

    assert executeTestCode(target.data + target.body) == "2"


def test_expr_div_basic():
    target = CoffeeTreeVisitorGen()
    test_prog = createTree("""
    return 12 / 4; 
    """)
    target.visit(test_prog)

    assert executeTestCode(target.data + target.body) == "3"


def test_expr_basic_assign():
    target = CoffeeTreeVisitorGen()
    test_prog = createTree("""
    int a;
    a = 2 + 3 * 4;
    return a; 
    """)
    target.visit(test_prog)

    assert executeTestCode(target.data + target.body) == "14"


def test_expr_basic_assign2():
    target = CoffeeTreeVisitorGen()
    test_prog = createTree("""
    int a;
    a = 2;
    return a; 
    """)
    target.visit(test_prog)

    assert executeTestCode(target.data + target.body) == "2"


def test_task1_reduced():
    target = CoffeeTreeVisitorGen()
    test_prog = createTree("""
    int a, b;
    a = 2 + 3 * 4; 
    b = 5 - a % 10;
    return (a + b);
    """)

    target.visit(test_prog)

    assert executeTestCode(target.data + target.body) == "15"


@pytest.mark.skip
def test_invert_number():
    target = CoffeeTreeVisitorGen()
    test_prog = createTree("""
    int a;
    a = 10;
    return -(a + a);
    """)

    target.visit(test_prog)

    assert executeTestCode(target.data + target.body) == "236"


@pytest.mark.skip
def test_task1():
    target = CoffeeTreeVisitorGen()
    test_prog = createTree("""
    int a, b;
    a = 2 + 3 * 4; 
    b = 5 - a % 10;
    return -(a + b);
    """)

    target.visit(test_prog)

    assert executeTestCode(target.data + target.body) == "241"
    runOutput = "Return Code 241"  # Is -15 but 256-15 == 241


@pytest.mark.skip
def test_task2_methods_empty():
    target = CoffeeTreeVisitorGen()
    test_prog = createTree("""
    int sum(int a, int b, int c, int d, int e, int f, int g) {
        return 0;
    }
    return sum(1, 2, 3, 4, 5, 6, 7);    
    """)

    target.visit(test_prog)
    assert executeTestCode(target.data + target.body) == "0"


@pytest.mark.skip
def test_task2_methods():
    target = CoffeeTreeVisitorGen()
    test_prog = createTree("""
    int sum(int a, int b, int c, int d, int e, int f, int g) {
        return a + b + c + d + e + f + g;
    }
    return sum(1, 2, 3, 4, 5, 6, 7);    
    """)

    target.visit(test_prog)
    assert executeTestCode(target.data + target.body) == "28"

@pytest.mark.skip
def test_for_loop():
    target = CoffeeTreeVisitorGen()
    test_prog = createTree("""
    int a = 0;
    for (i in [0:10:2]) { 
        a = a + i;
    }
    return a;""")
    target.visit(test_prog)
    assert executeTestCode(target.data + target.body) == "28"
