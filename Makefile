.PHONY:	dev/install
dev/install:
	poetry install
	rm .venv/bin/black
	ln -s pyink .venv/bin/black


.PHONY:	fmt
fmt:
	pyink .
	isort .


.PHONY:	lint
lint:
	ruff check .


.PHONY: typecheck
typecheck:
	pyright .
