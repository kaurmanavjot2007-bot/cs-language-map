"""A simplified teaching lineage; review ancestry with the professor."""
LANGUAGES = [{'id': 'algol',
  'name': 'ALGOL',
  'year': 1958,
  'family': 'ALGOL',
  'parent': None},
 {'id': 'pascal',
  'name': 'Pascal',
  'year': 1970,
  'family': 'ALGOL',
  'parent': 'algol'},
 {'id': 'c', 'name': 'C', 'year': 1972, 'family': 'ALGOL', 'parent': 'algol'},
 {'id': 'cpp', 'name': 'C++', 'year': 1985, 'family': 'ALGOL', 'parent': 'c'},
 {'id': 'java',
  'name': 'Java',
  'year': 1995,
  'family': 'ALGOL',
  'parent': 'cpp'},
 {'id': 'csharp',
  'name': 'C#',
  'year': 2000,
  'family': 'ALGOL',
  'parent': 'java'},
 {'id': 'go', 'name': 'Go', 'year': 2009, 'family': 'ALGOL', 'parent': 'c'},
 {'id': 'rust',
  'name': 'Rust',
  'year': 2015,
  'family': 'ALGOL',
  'parent': 'cpp'}]
LANGUAGES.extend([{'family': 'Fortran',
  'id': 'fortran',
  'name': 'Fortran',
  'parent': None,
  'year': 1957},
 {'family': 'Lisp', 'id': 'lisp', 'name': 'Lisp', 'parent': None, 'year': 1958},
 {'family': 'Smalltalk',
  'id': 'smalltalk',
  'name': 'Smalltalk',
  'parent': None,
  'year': 1972},
 {'family': 'ML',
  'id': 'haskell',
  'name': 'Haskell',
  'parent': None,
  'year': 1990},
 {'family': 'Scripting',
  'id': 'python',
  'name': 'Python',
  'parent': None,
  'year': 1991}])


def validate(languages):
    problems = []
    ids = [l['id'] for l in languages]
    if len(ids) != len(set(ids)):
        problems.append('duplicate language IDs')
    lookup = {l['id']: l for l in languages}
    for lang in languages:
        seen = set()
        current = lang
        while current:
            if current['id'] in seen:
                problems.append(lang['id'] + ': cycle in lineage')
                break
            seen.add(current['id'])
            parent = current['parent']
            if parent is not None and parent not in lookup:
                problems.append(current['id'] + ': unknown parent ' + parent)
                break
            current = lookup.get(parent)
    return problems
