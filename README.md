Coffee Lang
---

- test/
    - Unit tests for `semantics.py`
- CoffeeLang/
  - Result of `antlr -Dlanguage=Python3 -visitor ./Coffee.g4` 

To test, inside `CoffeeLang` directory, run `grun Coffee program ../test.coffee -gui`

## Tests
`test/`
  - `test_variable_spec` - rules 1 & 2 
  - `test_method_spec` - rules 3, 4, 5, 6, 7 & 8
  - `test_control_spec` - rules 9, 10, 11, 12, 15 27,
  - `test_expressions_spec` - 13, 17, 18, 21, 22, 23, 24, 25, 26
  - `test_arrays_spec` - 14, 16, 19, 20,