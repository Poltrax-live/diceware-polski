"""Embed both word lists into web/template.html -> docs/index.html (single self-contained file)."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def words(name):
    with open(os.path.join(ROOT, "lists", name), encoding="utf-8") as f:
        return [line.rstrip("\n").split("\t")[1] for line in f if line.strip()]

lists = {"plain": words("diceware-pl.txt"), "ogonki": words("diceware-pl-ogonki.txt")}
assert all(len(v) == 7776 for v in lists.values())
with open(os.path.join(ROOT, "web", "template.html"), encoding="utf-8") as f:
    html = f.read()
assert "/*LISTS*/null" in html
html = html.replace("/*LISTS*/null", json.dumps(lists, ensure_ascii=False, separators=(",", ":")))
os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)
with open(os.path.join(ROOT, "docs", "index.html"), "w", encoding="utf-8", newline="\n") as f:
    f.write(html)
print("docs/index.html:", len(html.encode()), "bytes")

import html as htmlmod, itertools
with open(os.path.join(ROOT, "web", "lista-template.html"), encoding="utf-8") as f:
    tpl = f.read()
rolls = ["".join(p) for p in itertools.product("123456", repeat=5)]
for key, out, title in (("plain", "lista.html", "bez polskich znaków"), ("ogonki", "lista-ogonki.html", "z polskimi znakami")):
    groups = []
    for prefix in ["".join(p) for p in itertools.product("123456", repeat=3)]:
        rows = [f'<span class="n">{r}</span> {htmlmod.escape(w)}<br>' for r, w in zip(rolls, lists[key]) if r.startswith(prefix)]
        groups.append(f'<div class="group"><b>{prefix}..</b>' + "".join(rows) + "</div>")
    page = tpl.replace("__TITLE__", title).replace("__BODY__", "\n".join(groups))
    with open(os.path.join(ROOT, "docs", out), "w", encoding="utf-8", newline="\n") as f:
        f.write(page)
    print(f"docs/{out}:", len(page.encode()), "bytes")
