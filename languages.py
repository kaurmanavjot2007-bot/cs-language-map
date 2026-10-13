"""Step 1: the data model for the CS language map.

Each language is one node. `parent` is the PRIMARY lineage (one parent only),
which is what makes the tree. Other influences come later as separate links.
"""

LANGUAGES = [
    {"id": "fortran", "name": "Fortran", "year": 1957, "family": "Fortran", "parent": None,
     "tagline": "First widely used high-level language, built for scientific computing."},
    {"id": "lisp", "name": "Lisp", "year": 1958, "family": "Lisp", "parent": None,
     "tagline": "Code as data; the root of the functional tradition."},
    {"id": "algol", "name": "ALGOL", "year": 1958, "family": "ALGOL", "parent": None,
     "tagline": "Introduced block structure; its syntax shaped most later languages."},
    {"id": "c", "name": "C", "year": 1972, "family": "ALGOL", "parent": "algol",
     "tagline": "Small, fast, close to the hardware."},
    {"id": "smalltalk", "name": "Smalltalk", "year": 1972, "family": "Smalltalk", "parent": None,
     "tagline": "Everything is an object; popularized object-oriented thinking."},
    {"id": "cpp", "name": "C++", "year": 1985, "family": "ALGOL", "parent": "c",
     "tagline": "C plus classes and abstractions, without giving up speed."},
    {"id": "haskell", "name": "Haskell", "year": 1990, "family": "ML", "parent": None,
     "tagline": "Purely functional with a strong static type system."},
    {"id": "java", "name": "Java", "year": 1995, "family": "ALGOL", "parent": "cpp",
     "tagline": "Write once, run anywhere; C++-style syntax with managed memory."},
    {"id": "rust", "name": "Rust", "year": 2015, "family": "ALGOL", "parent": "cpp",
     "tagline": "Systems programming with memory safety enforced at compile time."},
    # Python has mixed ancestry (ABC, plus ALGOL-family and Lisp ideas), so for now it is
    # a root of its own "Scripting" family. Open question for the professor.
    {"id": "python", "name": "Python", "year": 1991, "family": "Scripting", "parent": None,
     "tagline": "Readable, general-purpose, and beginner-friendly."},
]


def validate(languages):
    """Return a list of problems; an empty list means the data is consistent."""
    ids = {lang["id"] for lang in languages}
    problems = []
    for lang in languages:
        if lang["parent"] is not None and lang["parent"] not in ids:
            problems.append(f"{lang['id']}: unknown parent '{lang['parent']}'")
    return problems


def print_tree(languages):
    children = {}
    for lang in languages:
        children.setdefault(lang["parent"], []).append(lang)

    def walk(parent_id, depth):
        for lang in sorted(children.get(parent_id, []), key=lambda l: l["year"]):
            print("  " * depth + f"{lang['name']} ({lang['year']})")
            walk(lang["id"], depth + 1)

    walk(None, 0)


if __name__ == "__main__":
    issues = validate(LANGUAGES)
    print("Problems:", issues if issues else "none")
    print_tree(LANGUAGES)
