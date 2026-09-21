#!/usr/bin/env python3
"""Pull the published documents from an ngcc1 checkout into content/.

    python3 tools/sync.py [path/to/ngcc1]     (default: ../ngcc1)

Only the files listed in TOP, PER_CANDIDATE and DATA are written; hand-written
pages (content/index.md, content/candidates/index.md, ...) are never touched.
Relative Markdown links are rewritten so that they resolve inside the site:
links to other synced documents become site-relative, links to a candidate's
specification PDF go to its NICCS page, and links to anything else that is
not published (Makefiles, source files, libraries) are reduced to plain text.
"""
import csv
import posixpath
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
SRC = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT.parent / "ngcc1").resolve()

# Nothing is listed here until it has been cleared for publication.
# ngcc1-relative source -> content-relative destination, e.g. "RESULTS.md": "results.md"
TOP = {}
# per-candidate file -> destination inside content/candidates/<id>/, e.g. "pseudocode.md": "pseudocode.md"
PER_CANDIDATE = {}
# data files copied verbatim into content/data/, e.g. "sign.csv"
DATA = []

CAND_RE = re.compile(r"^(sign|kem|kex|hash)-\d\d$")
LINK_RE = re.compile(r"(?<!!)\[((?:[^\[\]]|\[[^\]]*\])*)\]\(([^)\s]+)(\s+\"[^\"]*\")?\)")


def die(msg):
    sys.exit(f"sync: {msg}")


def main():
    if not (SRC / "RESULTS.md").is_file():
        die(f"{SRC} does not look like an ngcc1 checkout (no RESULTS.md)")

    candidates = sorted(
        d.name for d in SRC.iterdir()
        if d.is_dir() and CAND_RE.match(d.name)
        and any((d / f).is_file() for f in PER_CANDIDATE)
    )

    # Complete map of ngcc1-relative path -> content-relative path.
    site_of = dict(TOP)
    for cid in candidates:
        for src, dst in PER_CANDIDATE.items():
            if (SRC / cid / src).is_file():
                site_of[f"{cid}/{src}"] = f"candidates/{cid}/{dst}"

    # NICCS candidate pages, used as the target for specification links.
    page_url = {}
    dl = SRC / "downloads.csv"
    if dl.is_file():
        with open(dl, encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter=";"):
                page_url[row["ID"]] = row.get("PageURL", "")

    def rewrite(text, src_rel, dst_rel):
        src_dir = posixpath.dirname(src_rel)
        dst_dir = posixpath.dirname(dst_rel)

        def repl(m):
            label, target, title = m.group(1), m.group(2), m.group(3) or ""
            if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
                return m.group(0)
            path, _, frag = target.partition("#")
            frag = f"#{frag}" if frag else ""
            # resolve relative to the file's directory, then to the ngcc1 root
            # (some reviews link as if they lived at the root)
            for cand in (posixpath.normpath(posixpath.join(src_dir, path)),
                         posixpath.normpath(path)):
                if cand in site_of:
                    rel = posixpath.relpath(site_of[cand], dst_dir or ".")
                    return f"[{label}]({rel}{frag}{title})"
            m_id = re.search(r"((?:sign|kem|kex|hash)-\d\d)", path)
            if path.lower().endswith(".pdf") and m_id and page_url.get(m_id.group(1)):
                return f"[{label}]({page_url[m_id.group(1)]})"
            return label

        return LINK_RE.sub(repl, text)

    def copy_md(src_rel, dst_rel):
        text = (SRC / src_rel).read_text(encoding="utf-8")
        text = rewrite(text, src_rel, dst_rel)
        out = CONTENT / dst_rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(f"<!-- synced from ngcc1/{src_rel} -->\n{text}", encoding="utf-8")

    n = 0
    for src_rel, dst_rel in TOP.items():
        if (SRC / src_rel).is_file():
            copy_md(src_rel, dst_rel); n += 1
        else:
            print(f"sync: missing {src_rel}", file=sys.stderr)
    for cid in candidates:
        for src, dst in PER_CANDIDATE.items():
            if (SRC / cid / src).is_file():
                copy_md(f"{cid}/{src}", f"candidates/{cid}/{dst}"); n += 1
            elif (CONTENT / "candidates" / cid / dst).is_file():
                (CONTENT / "candidates" / cid / dst).unlink()
                print(f"sync: removed stale candidates/{cid}/{dst}")

    # drop candidate directories that no longer exist upstream
    cdir = CONTENT / "candidates"
    cdir.mkdir(parents=True, exist_ok=True)
    for d in cdir.iterdir():
        if d.is_dir() and CAND_RE.match(d.name) and d.name not in candidates:
            shutil.rmtree(d)
            print(f"sync: removed stale {d.relative_to(ROOT)}")

    (CONTENT / "data").mkdir(parents=True, exist_ok=True)
    for name in DATA:
        if (SRC / name).is_file():
            shutil.copyfile(SRC / name, CONTENT / "data" / name); n += 1

    print(f"sync: {n} files from {SRC} -> {CONTENT.relative_to(ROOT)} ({len(candidates)} candidates)")


if __name__ == "__main__":
    main()
