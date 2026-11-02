SHA := $(shell git rev-parse --verify -q HEAD || echo dev)
WORKERS := $(patsubst docker/worker/%/Dockerfile,%,$(wildcard docker/worker/*/Dockerfile))

.PHONY: build build-worker build-airflow

build: build-worker build-airflow

build-worker:
	@for w in $(WORKERS); do \
	  docker build -f docker/worker/$$w/Dockerfile -t airflow-template/worker-$$w:$(SHA) -t airflow-template/worker-$$w:dev . || exit 1; \
	done

build-airflow:
	docker compose -f compose.dev.yaml build
