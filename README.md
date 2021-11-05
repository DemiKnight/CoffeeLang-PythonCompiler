Coffee Lang
---

- test/
    - Unit tests for `semantics.py`
- CoffeeLang/
  - Result of `antlr -Dlanguage=Python3 -visitor ./Coffee.g4` 

To test, inside `CoffeeLang` directory, run `grun Coffee program ../test.coffee -gui`

# Tests
- Run `pytest` 

## Semantic Rules 
1. Variables must be declared before use 
2. Variable declarations must have unique identifiers in a scope 
3. Method declarations (including imported methods) must have unique identifiers in a scope 
4. Method calls must refer to a declared method with an identical signature (return type, and number and type of parameters) 
5. Method calls referring to imported methods must produce a warning to check the argument and return types match that of the imported method 
6. Void methods cannot return an expression 
7. Non-void methods must return an expression 
8. The main method does not require a return statement, but if it has one, it must be of type int 
9. Branch statements (if-else) containing return statements do not qualify a method as having a return statement and a warning must be issued unless they appear in both the main branch and the else branch
10. Loops containing return statements do not qualify a method as having a return statement and a warning must be issued 
11. The expression in a branch statement must have type bool 
12. The expression in a while loop must have type bool 
13. The low and high expressions in a limit must have type int 
14. Arrays must be declared with size greater than 0 
15. The id in a for-loop must reference a declared array variable 
16. Arrays cannot be assigned during declaration 
17. Char expressions must be coerced to int 
18. The expression in an assignment must have type bool, int or float 
19. Locations of the from `<id> [ <expr> ]` must refer to a declared array variable 
20. In a location, array indices must have type 'int' 
21. The expression in unary minus operation must have type int or float 
22. The expression in logical not operation must have type bool 
23. The expression(s) in an arithmetic operation must have type int or float 
24. The expression(s) in a logical operation must have type bool 
25. The singular expression in a block (expr) provides a valid return value for a method without requiring the return keyword 
26. Methods returning void cannot be used in an expression 
27. Break and continue statements must be contained within the body of a loop.

#Coursework - Semantic 
Semantic Coursework Tasks 1 & 2
## Task 1 Method Invocation

Create a test source file with the following content:
```c
import printf, printf; 
void foo(int x, int y) { 
  return 0; 
} 
int a = food(1, -2.0, 5);
```
Use the supplied Coffee compiler to discover the semantic errors.
i) Identify all semantic errors (hint: rules 4, 6, 7, 26) in the above code and write code in your
CoffeeTreeVisitor class to detect the errors.

## Task 2 Arithmetic and Logic
Create a test source file with the following content:
```c
if (true && !1) { 
  return true; 
}
```
- Identify all semantic errors (hint: rules 8, 9, 11, 22) in the above code and write code in your
CoffeeTreeVisitor class to detect the errors.

# Coursework - CodeGen
CodeGen Coursework Tasks 1 & 2
## Task 1 Expressions
i) Arithmetic: Create a test source file with the following contents:
```c
int a, b;
a = 2 + 3 * 4; 
b = 5 - a % 10;
return -(a + b);
```
Write a solution which generates the correct assembly code and program output for the above Coffee code.

# Task 3 Loops
i) Limit / Step: Create a test source file with the following contents:
```c
int a = 0;
for (i in [1:10:2]) {
  a = a + i;
}
return a;
```
Write a solution which generates the correct assembly code and program output for the above Coffee
code.
Tip: in addition to visitFor for the loop, you will have to write visitAssign for the assignment of a + i;