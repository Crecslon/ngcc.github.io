# ngcc.dev static site. GitHub Pages serves docs/ from the main branch.
#
#   make build   render content/*.md -> docs/
#   make serve   preview at http://localhost:8000
#   make sync    pull cleared documents from an ngcc1 checkout (see tools/sync.py)
#   make clean   remove generated output (keeps docs/CNAME and docs/.nojekyll)

NGCC1 ?= ../ngcc1
PORT  ?= 8000

.PHONY: build serve sync clean
build:
	python3 tools/build.py
serve: build
	python3 -m http.server -d docs $(PORT)
sync:
	python3 tools/sync.py $(NGCC1)
clean:
	python3 tools/build.py --clean
