#!/usr/bin/env python3
"""Render content/ into docs/, the folder GitHub Pages serves.

    python3 tools/build.py          build the site
    python3 tools/build.py --clean  remove generated output only

Every content/**/*.md becomes docs/**/*.html. A page's title is its first H1
(or one derived from its path). Placeholders of the form <!-- table:NAME -->
are expanded before Markdown conversion, where NAME is one of
summary | sign | kem | kex | hash | all. All links are relative, so the site
works at any base URL.
"""
import csv
import datetime
import html
import posixpath
import re
import shutil
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
CONTENT, DOCS, ASSETS = ROOT / "content", ROOT / "docs", ROOT / "assets"
KEEP = {"CNAME", ".nojekyll"}          # never removed from docs/
SITE = "ngcc.dev"
REPO = "https://github.com/ngcc-dev/ngcc.github.io"
CATS = [("sign", "Signatures"), ("kem", "KEMs"), ("kex", "Key exchange"), ("hash", "Hash functions")]

NAV = [("Home", "index.html"), ("Candidates", "candidates/index.html"),
       ("KAT results", "results.html"), ("Security survey", "security-survey.html"),
       ("Attack matrix", "attack-matrix.html"), ("Audit", "audit.html")]

STATUS_CLASS = {
    "PASS": "ok", "FINDING": "bad", "MISMATCH": "bad", "CRYPTOFAIL": "bad", "OVERFLOW": "bad",
    "CRASH": "bad", "TIMEOUT": "warn", "ERROR": "warn", "NOKAT": "warn", "SKIP": "muted",
    "confirmed": "bad", "probable": "warn", "not_found": "ok", "ruled_out_by_design": "ok",
    "not_tested": "muted", "not_applicable": "muted", "inconclusive": "warn",
}

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{head_title}</title>
<link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body>
<header class="site-header">
<a class="brand" href="{prefix}index.html">{site}</a>
<nav>{nav}</nav>
</header>
<main>
{body}
</main>
<footer class="site-footer">
<p>Built {date} · <a href="{repo}">source</a></p>
</footer>
</body>
</html>
"""


def read_csv(name, delim=";"):
    p = CONTENT / "data" / name
    if not p.is_file():
        return []
    with open(p, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=delim))


def load_candidates():
    """id -> {cat, no, algorithm, submitters, page, zip, forum, kat_pass, kat_total, statuses}"""
    cands = {}
    for cat, _ in CATS:
        for row in read_csv(f"{cat}.csv"):
            cid = f"{cat}-{int(row['No']):02d}"
            cands[cid] = {"id": cid, "cat": cat, "no": int(row["No"]), "algorithm": row["Algorithm"],
                          "submitters": row.get("Submitters", ""), "page": "", "zip": "", "forum": "",
                          "kat_pass": 0, "kat_total": 0, "statuses": []}
    for row in read_csv("downloads.csv"):
        c = cands.setdefault(row["ID"], {"id": row["ID"], "cat": row["Category"], "no": int(row["No"]),
                                         "algorithm": row["Algorithm"], "submitters": "", "kat_pass": 0,
                                         "kat_total": 0, "statuses": []})
        c.update(page=row.get("PageURL", ""), zip=row.get("DownloadURL", ""), forum=row.get("ForumThread", ""))
    # per-instance statuses from the KAT results table
    res = CONTENT / "results.md"
    if res.is_file():
        cur = None
        for line in res.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\|\s*((?:sign|kem|kex|hash)-\d\d)?\s*\|[^|]*\|[^|]*\|[^|]*\|\s*(\S+)", line)
            if not m:
                continue
            cur = m.group(1) or cur
            if cur in cands:
                st = m.group(2)
                cands[cur]["statuses"].append(st)
                cands[cur]["kat_total"] += 1
                cands[cur]["kat_pass"] += st == "PASS"
    return cands


def candidate_pages(cid):
    d = CONTENT / "candidates" / cid
    out = []
    for name, label in (("index.md", "findings"), ("report.md", "report"), ("pseudocode.md", "pseudocode")):
        if (d / name).is_file():
            out.append((label, f"candidates/{cid}/{name[:-3]}.html"))
    return out


def kat_cell(c):
    if not c["kat_total"]:
        return "<td class=\"st muted\">—</td>"
    cls = "ok" if c["kat_pass"] == c["kat_total"] else ("bad" if c["kat_pass"] == 0 else "warn")
    return f"<td class=\"st {cls}\">{c['kat_pass']}/{c['kat_total']} PASS</td>"


def table_html(cands, cat, prefix):
    rows = sorted((c for c in cands.values() if c["cat"] == cat), key=lambda c: c["no"])
    h = ["<div class=\"table-wrap\"><table class=\"cands\">",
         "<thead><tr><th>id</th><th>algorithm</th><th>submitters</th><th>KAT</th><th>pages</th><th>NICCS</th></tr></thead><tbody>"]
    for c in rows:
        pages = " · ".join(f"<a href=\"{prefix}{href}\">{lab}</a>" for lab, href in candidate_pages(c["id"]))
        ext = " · ".join(f"<a href=\"{html.escape(c[k])}\">{lab}</a>" for k, lab in (("page", "page"), ("zip", "zip"), ("forum", "forum")) if c.get(k))
        h.append(f"<tr><td><code>{c['id']}</code></td><td>{html.escape(c['algorithm'])}</td>"
                 f"<td class=\"submitters\">{html.escape(c['submitters'])}</td>{kat_cell(c)}"
                 f"<td class=\"links\">{pages or '—'}</td><td class=\"links\">{ext or '—'}</td></tr>")
    h.append("</tbody></table></div>")
    return "\n".join(h)


def summary_html(cands, prefix):
    h = ["<table class=\"summary\"><thead><tr><th>category</th><th>candidates</th><th>instances</th><th>PASS</th><th>not PASS</th></tr></thead><tbody>"]
    tot = [0, 0, 0]
    for cat, label in CATS:
        cs = [c for c in cands.values() if c["cat"] == cat]
        n, p = sum(c["kat_total"] for c in cs), sum(c["kat_pass"] for c in cs)
        tot[0] += len(cs); tot[1] += n; tot[2] += p
        h.append(f"<tr><td><a href=\"{prefix}candidates/index.html#{cat}\">{label}</a></td><td>{len(cs)}</td><td>{n}</td><td>{p}</td><td>{n - p}</td></tr>")
    h.append(f"<tr class=\"total\"><td>total</td><td>{tot[0]}</td><td>{tot[1]}</td><td>{tot[2]}</td><td>{tot[1] - tot[2]}</td></tr>")
    h.append("</tbody></table>")
    return "\n".join(h)


def expand_placeholders(text, cands, prefix):
    def repl(m):
        name = m.group(1)
        if name == "summary":
            return summary_html(cands, prefix)
        if name == "all":
            return "\n".join(f"<h2 id=\"{cat}\">{label}</h2>\n{table_html(cands, cat, prefix)}" for cat, label in CATS)
        if name in dict(CATS):
            return table_html(cands, name, prefix)
        return m.group(0)
    return re.sub(r"<!--\s*table:(\w+)\s*-->", repl, text)


def status_classes(body):
    def repl(m):
        attrs, code_open, token, code_close = m.group(1), m.group(2) or "", m.group(3), m.group(4) or ""
        cls = STATUS_CLASS[token]
        attrs = re.sub(r'\sclass="([^"]*)"', lambda c: f' class="{c.group(1)} st {cls}"', attrs) if 'class="' in attrs else f'{attrs} class="st {cls}"'
        return f"<td{attrs}>{code_open}{token}{code_close}"
    tokens = "|".join(re.escape(t) for t in STATUS_CLASS)
    return re.sub(rf"<td([^>]*)>(<code>)?({tokens})(</code>)?(?=[\s<]|$)", repl, body)


def md_links_to_html(body):
    def repl(m):
        href = m.group(1)
        if re.match(r"^[a-z][a-z0-9+.-]*:", href) or href.startswith("#"):
            return m.group(0)
        path, _, frag = href.partition("#")
        if path.endswith(".md"):
            path = path[:-3] + ".html"
        return f'href="{path}{"#" + frag if frag else ""}"'
    return re.sub(r'href="([^"]*)"', repl, body)


def page_title(text, rel):
    m = re.search(r"^#\s+(.+?)\s*$", text, re.M)
    if m:
        return re.sub(r"[*`_]", "", m.group(1))
    parts = rel.with_suffix("").parts
    if len(parts) >= 3 and parts[0] == "candidates":
        return f"{parts[1]} {parts[2]}"
    return rel.stem.replace("-", " ")


def render(rel, cands):
    text = (CONTENT / rel).read_text(encoding="utf-8")
    depth = len(rel.parts) - 1
    prefix = "../" * depth
    title = page_title(text, rel)
    text = expand_placeholders(text, cands, prefix)
    # candidate pages without an H1 get one, plus a breadcrumb back to the index
    if rel.parts[0] == "candidates" and len(rel.parts) == 3:
        cid = rel.parts[1]
        c = cands.get(cid, {})
        crumb = f"<p class=\"crumb\"><a href=\"{prefix}candidates/index.html#{c.get('cat', '')}\">Candidates</a> › <code>{cid}</code>"
        crumb += "".join(f" · <a href=\"{prefix}{href}\">{lab}</a>" for lab, href in candidate_pages(cid) if href != f"candidates/{cid}/{rel.stem}.html")
        crumb += "</p>\n"
        if not re.search(r"^#\s", text, re.M):
            title = f"{cid} {c.get('algorithm', '')} — {rel.stem}".strip()
            text = f"# {title}\n\n{text}"
        text = crumb + text
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "toc", "sane_lists"],
                             extension_configs={"toc": {"permalink": False}})
    body = md_links_to_html(status_classes(body))
    body = re.sub(r"<table>", '<div class="table-wrap"><table>', body).replace("</table>", "</table></div>")
    nav = "".join(f'<a href="{prefix}{href}">{lab}</a>' for lab, href in NAV
                  if (CONTENT / href).with_suffix(".md").is_file())
    out = DOCS / rel.with_suffix(".html")
    out.parent.mkdir(parents=True, exist_ok=True)
    head_title = SITE if title == SITE else f"{title} · {SITE}"
    out.write_text(TEMPLATE.format(head_title=html.escape(head_title), site=SITE, prefix=prefix, nav=nav, body=body,
                                   date=datetime.date.today().isoformat(), repo=REPO), encoding="utf-8")


def clean():
    for p in DOCS.iterdir():
        if p.name in KEEP:
            continue
        shutil.rmtree(p) if p.is_dir() else p.unlink()


def main():
    DOCS.mkdir(exist_ok=True)
    clean()
    if "--clean" in sys.argv:
        return
    if ASSETS.is_dir():
        shutil.copytree(ASSETS, DOCS / "assets")
    if (CONTENT / "data").is_dir():
        shutil.copytree(CONTENT / "data", DOCS / "data")
    cands = load_candidates()
    pages = sorted(p.relative_to(CONTENT) for p in CONTENT.rglob("*.md"))
    for rel in pages:
        render(rel, cands)
    print(f"build: {len(pages)} pages, {len(cands)} candidates -> {DOCS.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
