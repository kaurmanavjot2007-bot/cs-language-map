"""Step 2: what shows up when someone clicks a language.

Each language gets four "concept bubbles" (short, easy-words explanations)
and the same tiny task in code: print the numbers 0 to 4.
"""

# Soft pink / lavender / peach / mint / sky / coral palette
FAMILY_COLORS = {
    "Fortran": "#ffb38a",    # peach
    "Lisp": "#c3a6ff",       # lavender
    "ALGOL": "#ff8fc7",      # pink
    "Smalltalk": "#7fe0c8",  # mint
    "ML": "#8cc9ff",         # sky blue
    "Scripting": "#ff9aa8",  # coral rose
}

CONCEPTS = {
    "fortran": [
        ("Memory", "Arrays of numbers sit in fixed blocks of memory, which makes number crunching very fast."),
        ("Types", "Every variable has a set type, like integer or real (a decimal number)."),
        ("Style", "Procedural: you write step-by-step instructions and group them into subroutines."),
        ("Big idea", "Let scientists write math-like code instead of machine code."),
    ],
    "lisp": [
        ("Memory", "Memory is cleaned up for you automatically. Lisp was one of the first languages to do this (garbage collection)."),
        ("Types", "Types are checked while the program runs, not before (dynamic typing)."),
        ("Style", "Functional: functions can be passed around like any other value, and code is written as lists."),
        ("Big idea", "Code is data, so programs can write and change other programs."),
    ],
    "algol": [
        ("Memory", "Variables live inside a block and disappear when the block ends."),
        ("Types", "Variables have types like integer, real, and boolean."),
        ("Style", "Structured: begin...end blocks, loops, and if/else instead of jumping around."),
        ("Big idea", "Blocks and scope. Nearly every later language copied this."),
    ],
    "c": [
        ("Memory", "You ask for memory and give it back yourself, using pointers."),
        ("Types", "Types are checked before the program runs, but you can cast your way around them."),
        ("Style", "Procedural: small, simple, and close to the hardware."),
        ("Big idea", "Fast enough to write operating systems, portable enough to run almost anywhere."),
    ],
    "smalltalk": [
        ("Memory", "Everything is an object, and unused objects are cleaned up automatically."),
        ("Types", "Dynamic: an object decides at runtime how to respond to a message."),
        ("Style", "Pure object-oriented: all you do is send messages to objects."),
        ("Big idea", "A program is a bunch of objects talking to each other."),
    ],
    "cpp": [
        ("Memory", "Manual like C, but tools like destructors and smart pointers help clean up for you."),
        ("Types", "Static types with classes and templates (code that works with many types)."),
        ("Style", "Multi-paradigm: procedural, object-oriented, and generic code all in one language."),
        ("Big idea", "C's speed, plus classes to organize big programs."),
    ],
    "haskell": [
        ("Memory", "Memory is cleaned up automatically, and data is immutable by default (it does not change)."),
        ("Types", "Static and strong, and the compiler can often figure out types for you (type inference)."),
        ("Style", "Purely functional: functions have no hidden side effects, and values are computed only when needed (lazy)."),
        ("Big idea", "Write programs like math, so they are easier to reason about."),
    ],
    "java": [
        ("Memory", "A garbage collector frees memory for you automatically."),
        ("Types", "Static types, and all code lives inside classes."),
        ("Style", "Object-oriented, with C++-style syntax."),
        ("Big idea", "Compile once to bytecode, then run it on any machine with a Java Virtual Machine."),
    ],
    "rust": [
        ("Memory", "Ownership rules free memory safely at compile time, with no garbage collector."),
        ("Types", "Static and strong, with type inference."),
        ("Style", "Multi-paradigm: systems-level control with some functional ideas."),
        ("Big idea", "As fast as C++, but the compiler blocks whole kinds of memory bugs."),
    ],
    "python": [
        ("Memory", "Automatic: Python counts references to objects and cleans up the ones nobody uses."),
        ("Types", "Dynamic: types are checked while running (optional type hints exist)."),
        ("Style", "Multi-paradigm, with indentation that forces readable code."),
        ("Big idea", "Code should be easy to read and quick to write."),
    ],
}

# The same task in every language: print the numbers 0 to 4.
CODE = {
    "fortran": ("Fortran", "do i = 0, 4\n  print *, i\nend do"),
    "lisp": ("Common Lisp", "(dotimes (i 5)\n  (print i))"),
    "algol": ("ALGOL 68", "FOR i FROM 0 TO 4 DO\n  print((i, newline))\nOD"),
    "c": ("C", "for (int i = 0; i < 5; i++) {\n    printf(\"%d\\n\", i);\n}"),
    "smalltalk": ("Smalltalk", "0 to: 4 do: [:i |\n    Transcript showCr: i printString]"),
    "cpp": ("C++", "for (int i = 0; i < 5; i++) {\n    std::cout << i << \"\\n\";\n}"),
    "haskell": ("Haskell", "mapM_ print [0..4]"),
    "java": ("Java", "for (int i = 0; i < 5; i++) {\n    System.out.println(i);\n}"),
    "rust": ("Rust", "for i in 0..5 {\n    println!(\"{}\", i);\n}"),
    "python": ("Python", "for i in range(5):\n    print(i)"),
}
