.PHONY: run
run:
	uvicorn app.main:app --host 0.0.0.0 --port 8062

.PHONY: grpc_server
grpc_server:
	python grpc_server.py

.PHONY: test
test:
	pytest --cov=app tests/

.PHONY: lint
lint:
	flake8 app/

.PHONY: build
build:
	docker build -t label-service .

.PHONY: deploy
deploy:
	kubectl apply -f k8s/
