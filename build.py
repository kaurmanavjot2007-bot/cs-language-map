"""Build the static site: reads the data, computes the tree layout, and
writes docs/index.html (the folder GitHub Pages serves).

Run:  python build.py
To add another family later, add its name to FAMILIES_SHOWN and give each
of its languages an entry in lessons.py.
"""
import json
import os

from languages import LANGUAGES, validate
from lessons import LESSONS

FAMILIES_SHOWN = ["ALGOL"]

SLOT = 240        # horizontal space per leaf
PX_PER_YEAR = 20  # the timeline: vertical space per year
TOP_PAD = 190     # room above the oldest language for the trunk stem
SIDE_PAD = 130
BOTTOM_PAD = 170


def layout(languages):
    children = {}
    for lang in languages:
        children.setdefault(lang["parent"], []).append(lang)
    for kids in children.values():
        kids.sort(key=lambda l: l["year"])

    pos = {}
    depth_of = {}

    def place(node_id, depth, x0):
        depth_of[node_id] = depth
        kids = children.get(node_id, [])
        if not kids:
            pos[node_id] = x0 + 0.5
            return 1
        cursor = x0
        for kid in kids:
            cursor += place(kid["id"], depth + 1, cursor)
        pos[node_id] = (pos[kids[0]["id"]] + pos[kids[-1]["id"]]) / 2
        return cursor - x0

    cursor = 0
    for root in children.get(None, []):
        cursor += place(root["id"], 0, cursor)

    first = min(l["year"] for l in languages)
    last = max(l["year"] for l in languages)
    width = round(cursor * SLOT + SIDE_PAD * 2)
    height = round(TOP_PAD + (last - first) * PX_PER_YEAR + BOTTOM_PAD)

    nodes = []
    for lang in sorted(languages, key=lambda l: l["year"]):
        nodes.append({
            "id": lang["id"], "name": lang["name"], "year": lang["year"],
            "parent": lang["parent"], "depth": depth_of[lang["id"]],
            "x": round(SIDE_PAD + pos[lang["id"]] * SLOT),
            "y": round(TOP_PAD + (lang["year"] - first) * PX_PER_YEAR),
        })

    years = sorted({n["year"] for n in nodes})
    root = next(n for n in nodes if n["parent"] is None)
    return {
        "width": width, "height": height, "nodes": nodes,
        "years": [{"year": y, "y": TOP_PAD + (y - first) * PX_PER_YEAR} for y in years],
        "stem": {"x": root["x"], "y1": 0, "y2": root["y"]},
        "langs": [{"id": n["id"], "name": n["name"]} for n in nodes],
    }


def main():
    shown = [l for l in LANGUAGES if l["family"] in FAMILIES_SHOWN]
    problems = validate(shown)
    if problems:
        raise SystemExit("Fix the data first: " + "; ".join(problems))
    for lang in shown:
        lesson = LESSONS.get(lang["id"])
        if not lesson or not all(k in lesson for k in ("types", "cond", "loop", "fn")):
            raise SystemExit(f"Missing lessons for {lang['id']} in lessons.py")

    data = layout(shown)
    data["lessons"] = {l["id"]: LESSONS[l["id"]] for l in shown}

    with open("template.html", encoding="utf-8") as f:
        html = f.read()
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = html.replace("__DATA__", payload)

    os.makedirs("docs", exist_ok=True)
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Built docs/index.html with {len(data['nodes'])} languages")


if __name__ == "__main__":
    main()
