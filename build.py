"""Build the static site. Run python3 build.py; publish the docs folder."""
import json
from pathlib import Path
from languages import LANGUAGES, validate
from lessons import LESSONS

FAMILIES_SHOWN = ['ALGOL']
SLOT = 300
PX_PER_YEAR = 10
TOP_PAD = 80
SIDE_PAD = 75
BOTTOM_PAD = 90


def layout(languages):
    children = {}
    for lang in languages:
        children.setdefault(lang['parent'], []).append(lang)
    for kids in children.values():
        kids.sort(key=lambda l: (l['year'], l['id']))
    pos, depths = {}, {}
    def place(node, depth, x0):
        depths[node] = depth
        kids = children.get(node, [])
        if not kids:
            pos[node] = x0 + .5
            return 1
        cursor = x0
        for kid in kids:
            cursor += place(kid['id'], depth + 1, cursor)
        pos[node] = (pos[kids[0]['id']] + pos[kids[-1]['id']]) / 2
        return cursor - x0
    cursor = 0
    for root in children.get(None, []):
        cursor += place(root['id'], 0, cursor)
    first, last = min(l['year'] for l in languages), max(l['year'] for l in languages)
    nodes = [dict(id=l['id'], name=l['name'], year=l['year'], parent=l['parent'],
                  depth=depths[l['id']], x=round(SIDE_PAD + pos[l['id']] * SLOT),
                  y=TOP_PAD + (l['year'] - first) * PX_PER_YEAR)
             for l in sorted(languages, key=lambda l: l['year'])]
    # Offset a sole child so nearby years do not overlap their language orbs.
    for n in nodes:
        if n['parent'] and len(children[n['parent']]) == 1:
            n['x'] -= 110
    roots = [n for n in nodes if n['parent'] is None]
    return dict(width=cursor*SLOT+SIDE_PAD*2,
                height=TOP_PAD+(last-first)*PX_PER_YEAR+BOTTOM_PAD, nodes=nodes,
                years=[dict(year=y,y=TOP_PAD+(y-first)*PX_PER_YEAR) for y in sorted({n['year'] for n in nodes})],
                stem=dict(x=roots[0]['x'],y1=0,y2=roots[0]['y']),
                langs=[dict(id=n['id'],name=n['name']) for n in nodes])


def main():
    root = Path(__file__).resolve().parent
    shown = [l for l in LANGUAGES if l['family'] in FAMILIES_SHOWN]
    if not shown:
        raise SystemExit('No languages selected')
    problems = validate(shown)
    if problems:
        raise SystemExit('; '.join(problems))
    for lang in shown:
        if not all(k in LESSONS.get(lang['id'], {}) for k in ('types','cond','loop','fn')):
            raise SystemExit('Missing lessons for ' + lang['id'])
    data = layout(shown)
    data['lessons'] = {l['id']: LESSONS[l['id']] for l in shown}
    template = (root/'template.html').read_text(encoding='utf-8')
    if template.count('__DATA__') != 1:
        raise SystemExit('Expected one __DATA__ placeholder')
    payload = json.dumps(data,ensure_ascii=False).replace('</','<\\/')
    (root/'docs').mkdir(exist_ok=True)
    (root/'docs/index.html').write_text(template.replace('__DATA__',payload),encoding='utf-8')
    print(f"Built docs/index.html with {len(shown)} languages")

if __name__ == '__main__':
    main()
