# ngcc.dev static site. GitHub Pages serves docs/ from the main branch.
#
#   make build   render content/*.md -> docs/
#   make serve   preview at http://localhost:8000
#   make check   verify the rendered site (links, anchors, tag balance)
#   make sync    pull cleared documents from an ngcc1 checkout (see tools/sync.py)
#   make clean   remove generated output (keeps docs/CNAME and docs/.nojekyll)

NGCC1 ?= ../ngcc1
PORT  ?= 8000

.PHONY: build check serve sync clean
build:
	python3 tools/build.py
check: build
	python3 tools/check.py

serve: build
	python3 -m http.server -d docs $(PORT)
sync:
	python3 tools/sync.py $(NGCC1)
clean:
	python3 tools/build.py --clean
