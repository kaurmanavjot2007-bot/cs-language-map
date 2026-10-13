"""Lesson content: the same four ideas (types, if/else, loops, functions)
written in each language's own syntax.

Placeholders the page fills in while you play:
  {N} loop count, {M} = N-1, {a} {b} function inputs, {v} the age value.
"""


def _loop(header, body, *rest):
    return {"lines": [header, body, *rest], "header": 0, "body": 1}


def _clike_loop(print_stmt):
    return {"lines": ["for (int i = 0; i < {N}; i++) {", "  " + print_stmt, "}"],
            "header": 0, "body": 1}


def _clike_fn(sig, call):
    return {"lines": [sig, "  return a + b;", "}", call], "call": 3}


def _clike_cond(adult, minor):
    return {"lines": ["int age = {v};", "if (age >= 18) {", "  " + adult, "} else {", "  " + minor, "}"],
            "then": 2, "else": 4}


def _clike_types(t_int, t_float, t_char, t_bool):
    return [
        (f"{t_int} n = 42;", t_int),
        (f"{t_float} x = 3.14;", t_float),
        (f"{t_char} c = 'A';", t_char),
        (f"{t_bool} ok = true;", t_bool),
    ]


LESSONS = {
    "algol": {
        "loop": _loop("FOR i FROM 0 TO {M} DO", "  print((i, newline))", "OD"),
        "fn": {"lines": ["PROC add = (INT a, b) INT: a + b;", "print((add({a}, {b}), newline))"], "call": 1},
        "cond": {"lines": ["INT age = {v};", "IF age >= 18", "THEN print((\"Adult\", newline))",
                           "ELSE print((\"Minor\", newline))", "FI"], "then": 2, "else": 3},
        "types": [("INT n = 42;", "INT"), ("REAL x = 3.14;", "REAL"),
                  ("CHAR c = \"A\";", "CHAR"), ("BOOL ok = TRUE;", "BOOL")],
    },
    "pascal": {
        "loop": _loop("for i := 0 to {M} do", "  writeln(i);"),
        "fn": {"lines": ["function add(a, b: integer): integer;", "begin", "  add := a + b;", "end;",
                         "writeln(add({a}, {b}));"], "call": 4},
        "cond": {"lines": ["age := {v};", "if age >= 18 then", "  writeln('Adult')", "else",
                           "  writeln('Minor');"], "then": 2, "else": 4},
        "types": [("var n: integer = 42;", "integer"), ("var x: real = 3.14;", "real"),
                  ("var c: char = 'A';", "char"), ("var ok: boolean = true;", "boolean")],
    },
    "c": {
        "loop": _clike_loop("printf(\"%d\\n\", i);"),
        "fn": _clike_fn("int add(int a, int b) {", "printf(\"%d\", add({a}, {b}));"),
        "cond": _clike_cond("puts(\"Adult\");", "puts(\"Minor\");"),
        "types": _clike_types("int", "double", "char", "bool"),
    },
    "cpp": {
        "loop": _clike_loop("std::cout << i << \"\\n\";"),
        "fn": _clike_fn("int add(int a, int b) {", "std::cout << add({a}, {b});"),
        "cond": _clike_cond("std::cout << \"Adult\";", "std::cout << \"Minor\";"),
        "types": _clike_types("int", "double", "char", "bool"),
    },
    "java": {
        "loop": _clike_loop("System.out.println(i);"),
        "fn": _clike_fn("static int add(int a, int b) {", "System.out.println(add({a}, {b}));"),
        "cond": _clike_cond("System.out.println(\"Adult\");", "System.out.println(\"Minor\");"),
        "types": _clike_types("int", "double", "char", "boolean"),
    },
    "csharp": {
        "loop": _clike_loop("Console.WriteLine(i);"),
        "fn": _clike_fn("static int add(int a, int b) {", "Console.WriteLine(add({a}, {b}));"),
        "cond": _clike_cond("Console.WriteLine(\"Adult\");", "Console.WriteLine(\"Minor\");"),
        "types": _clike_types("int", "double", "char", "bool"),
    },
    "rust": {
        "loop": {"lines": ["for i in 0..{N} {", "    println!(\"{}\", i);", "}"], "header": 0, "body": 1},
        "fn": {"lines": ["fn add(a: i32, b: i32) -> i32 {", "    a + b", "}",
                         "println!(\"{}\", add({a}, {b}));"], "call": 3},
        "cond": {"lines": ["let age = {v};", "if age >= 18 {", "    println!(\"Adult\");", "} else {",
                           "    println!(\"Minor\");", "}"], "then": 2, "else": 4},
        "types": [("let n: i32 = 42;", "i32"), ("let x: f64 = 3.14;", "f64"),
                  ("let c: char = 'A';", "char"), ("let ok: bool = true;", "bool")],
    },
    "go": {
        "loop": {"lines": ["for i := 0; i < {N}; i++ {", "  fmt.Println(i)", "}"], "header": 0, "body": 1},
        "fn": {"lines": ["func add(a int, b int) int {", "  return a + b", "}",
                         "fmt.Println(add({a}, {b}))"], "call": 3},
        "cond": {"lines": ["age := {v}", "if age >= 18 {", "  fmt.Println(\"Adult\")", "} else {",
                           "  fmt.Println(\"Minor\")", "}"], "then": 2, "else": 4},
        "types": [("var n int = 42", "int"), ("var x float64 = 3.14", "float64"),
                  ("var c rune = 'A'", "rune"), ("var ok bool = true", "bool")],
    },
}
