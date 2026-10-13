"""Build the static site: reads the data, computes the tree layout, and
writes docs/index.html (the folder GitHub Pages can serve).

Run:  python build.py
"""
import json
import os

from concepts import CODE, CONCEPTS, FAMILY_COLORS
from languages import LANGUAGES, validate

SLOT = 150    # horizontal space per leaf node
ROW = 135     # vertical space per tree level
TOP = 135     # y of the first level
LEFT = 40
GAP = 0.3     # gap between family regions, in slots


def layout(languages):
    by_id = {lang["id"]: lang for lang in languages}
    children = {}
    for lang in languages:
        children.setdefault(lang["parent"], []).append(lang)
    for kids in children.values():
        kids.sort(key=lambda l: l["year"])

    pos = {}  # id -> (x in slots, depth)

    def place(node_id, depth, x0):
        kids = children.get(node_id, [])
        if not kids:
            pos[node_id] = (x0 + 0.5, depth)
            return 1
        cursor = x0
        for kid in kids:
            cursor += place(kid["id"], depth + 1, cursor)
        pos[node_id] = ((pos[kids[0]["id"]][0] + pos[kids[-1]["id"]][0]) / 2, depth)
        return cursor - x0

    # Families ordered by the year of their oldest language
    first_year = {}
    for lang in languages:
        first_year[lang["family"]] = min(first_year.get(lang["family"], 9999), lang["year"])
    families = sorted(first_year, key=lambda f: first_year[f])

    cursor = 0.0
    regions = []
    for fam in families:
        start = cursor
        roots = [l for l in children.get(None, []) if l["family"] == fam]
        for root in roots:
            cursor += place(root["id"], 0, cursor)
        regions.append({"family": fam, "start": start, "end": cursor})
        cursor += GAP

    max_depth = max(d for _, d in pos.values())
    width = LEFT * 2 + (cursor - GAP) * SLOT
    height = TOP + max_depth * ROW + 110

    nodes = []
    for lang in languages:
        sx, depth = pos[lang["id"]]
        label, code = CODE[lang["id"]]
        nodes.append({
            **lang,
            "x": round(LEFT + sx * SLOT),
            "y": TOP + depth * ROW,
            "color": FAMILY_COLORS[lang["family"]],
            "concepts": [{"label": a, "text": b} for a, b in CONCEPTS[lang["id"]]],
            "codeLang": label,
            "code": code,
        })

    region_out = [{
        "family": r["family"],
        "color": FAMILY_COLORS[r["family"]],
        "x": round(LEFT + r["start"] * SLOT - 10),
        "w": round((r["end"] - r["start"]) * SLOT + 20),
    } for r in regions]

    return {"width": round(width), "height": round(height), "nodes": nodes, "regions": region_out}


def main():
    problems = validate(LANGUAGES)
    if problems:
        raise SystemExit("Fix the data first: " + "; ".join(problems))
    missing = [l["id"] for l in LANGUAGES if l["id"] not in CONCEPTS or l["id"] not in CODE]
    if missing:
        raise SystemExit("Missing concepts/code for: " + ", ".join(missing))

    data = layout(LANGUAGES)
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
