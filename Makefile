# Proti IQ Development & Operations Automation

.PHONY: setup pipeline test run-api run-ui docker-up audit

setup:
	pip install -r requirements.txt

pipeline:
	python -m pipeline.cli run-all

test:
	pytest tests/ -v

audit:
	ruff check .
	python -m pip_audit

run-api:
	uvicorn api.main:app --reload --port 8000

run-ui:
	streamlit run ui/Home.py --server.port 8501

docker-up:
	docker compose up --build
