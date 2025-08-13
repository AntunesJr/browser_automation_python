# Development commands
.PHONY: setup
setup:
	@./scripts/dev_setup.sh

.PHONY: test
test:
	@./scripts/run_tests.sh

# Docker commands
.PHONY: docker-build
docker-build:
	@docker build -t browser-automation-python .

.PHONY: docker-run
docker-run:
	@docker run --rm browser-automation-python

.PHONY: docker-test
docker-test:
	@docker run --rm browser-automation-python check_cred