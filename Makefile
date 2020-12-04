DOCKER_IMAGE = eu.gcr.io/ingka-dt-slack-dev/rrm

.PHONY: build
build:
	@echo "Docker Build..."
	docker build -t $(DOCKER_IMAGE) .
	