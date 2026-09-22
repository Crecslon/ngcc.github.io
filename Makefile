# ngcc.dev static site. GitHub Pages serves docs/ from the main branch.
#
#   make build   render content/*.md -> docs/
#   make serve   preview at http://localhost:8000
#   make check   verify the rendered site (links, anchors, tag balance)
#   make sync REPORT_SOURCE=/path/to/source-checkout
#   make clean   remove generated output (keeps docs/CNAME and docs/.nojekyll)

REPORT_SOURCE ?=
PORT  ?= 8000

.PHONY: build check serve sync clean
build:
	python3 tools/build.py
check: build
	python3 tools/check.py

serve: build
	python3 -m http.server -d docs $(PORT)
sync:
	@test -n "$(REPORT_SOURCE)" || { echo "set REPORT_SOURCE=/path/to/source-checkout" >&2; exit 2; }
	python3 tools/sync.py "$(REPORT_SOURCE)"
clean:
	python3 tools/build.py --clean
