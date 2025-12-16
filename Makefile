.PHONY: help install test test-unit test-eval lint format clean docker-build docker-run k8s-deploy k8s-undeploy terraform-init terraform-plan terraform-apply terraform-destroy minikube-start minikube-stop service-run service-test

# Default target
help:
	@echo "Available commands:"
	@echo "  make install          - Install dependencies"
	@echo "  make test             - Run all tests"
	@echo "  make test-unit        - Run unit tests only"
	@echo "  make test-eval        - Run evaluation tests (golden datasets)"
	@echo "  make lint             - Run linter (ruff)"
	@echo "  make format           - Format code (ruff)"
	@echo "  make clean            - Clean build artifacts"
	@echo ""
	@echo "Docker commands:"
	@echo "  make docker-build     - Build Docker image"
	@echo "  make docker-run       - Run Docker container"
	@echo ""
	@echo "Kubernetes commands:"
	@echo "  make k8s-deploy       - Deploy to Kubernetes"
	@echo "  make k8s-undeploy     - Remove from Kubernetes"
	@echo "  make minikube-start   - Start Minikube cluster"
	@echo "  make minikube-stop    - Stop Minikube cluster"
	@echo ""
	@echo "Terraform commands:"
	@echo "  make terraform-init   - Initialize Terraform"
	@echo "  make terraform-plan   - Plan Terraform changes"
	@echo "  make terraform-apply  - Apply Terraform changes"
	@echo "  make terraform-destroy - Destroy Terraform resources"
	@echo ""
	@echo "Service commands:"
	@echo "  make service-run      - Run service locally (simple backend)"
	@echo "  make service-run-hf   - Run service with HuggingFace backend"
	@echo "  make service-test     - Test service endpoints"

# Installation
install:
	pip install --upgrade pip
	pip install -e ".[dev]"
	pip install -r service/requirements.txt

# Testing
test: test-unit test-eval

test-unit:
	pytest ai_lib/tests -v
	pytest service/app/tests -v

test-eval:
	export AI_LIB_SUMMARISATION_BACKEND=simple && pytest eval -v

# Code quality
lint:
	ruff check .

format:
	ruff format .

lint-fix:
	ruff check --fix .

clean:
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -r {} + 2>/dev/null || true
	rm -rf .dist build

# Docker
docker-build:
	docker build -f service/DockerFile -t ai-summarise-service:latest .

docker-run:
	docker run -p 8000:8000 \
		-e AI_LIB_SUMMARISATION_BACKEND=simple \
		ai-summarise-service:latest

# Kubernetes
k8s-deploy:
	@echo "Building image in Minikube..."
	eval $$(minikube docker-env) && docker build -f service/DockerFile -t ai-summarise-service:latest .
	@echo "Deploying to Kubernetes..."
	kubectl apply -f service/k8s/deployment.yml
	kubectl apply -f service/k8s/service.yml
	@echo "Deployment complete. Use 'kubectl get pods -n ai-platform' to check status."

k8s-undeploy:
	kubectl delete -f service/k8s/deployment.yml
	kubectl delete -f service/k8s/service.yml

minikube-start:
	minikube start

minikube-stop:
	minikube stop

# Terraform
terraform-init:
	cd terraform && terraform init

terraform-plan:
	cd terraform && terraform plan

terraform-apply:
	cd terraform && terraform apply

terraform-destroy:
	cd terraform && terraform destroy

# Service
service-run:
	@echo "Starting service with backend: $${AI_LIB_SUMMARISATION_BACKEND:-simple}"
	@echo "To use HuggingFace backend, run: AI_LIB_SUMMARISATION_BACKEND=hf make service-run"
	uvicorn service.app.main:app --reload --host 0.0.0.0 --port 8000

service-run-hf:
	@echo "Starting service with HuggingFace backend..."
	AI_LIB_SUMMARISATION_BACKEND=hf uvicorn service.app.main:app --reload --host 0.0.0.0 --port 8000

service-test:
	@echo "Testing health endpoint..."
	curl http://localhost:8000/health
	@echo "\n\nTesting summarise endpoint..."
	curl -X POST http://localhost:8000/summarise \
		-H "Content-Type: application/json" \
		-d '{"text": "Bella is a 3-year-old indoor cat. She visits the vet once a year and is generally healthy."}'
