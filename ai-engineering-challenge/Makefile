.PHONY: run-api run-notebook install run-ui install-ui build-ui

run-api:
	.venv/bin/uvicorn api.index:app --reload

run-notebook:
	.venv/bin/jupyter notebook

install:
	uv sync

run-ui:
	cd frontend && npm run dev

install-ui:
	cd frontend && npm install

build-ui:
	cd frontend && npm run build
