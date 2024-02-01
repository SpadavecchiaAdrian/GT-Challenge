.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


clean-pyc:
	echo "Clean pycache"
	find ./backend/ -name '__pycache__' -exec rm -rf {} +
	find ./backend/ -name '*.pyc' -exec rm -f {} +
	find ./backend/ -name '*.pyo' -exec rm -f {} +
	find ./backend/ -name '*~' -exec rm -f {} +

local-run: clean-pyc ## Run FastAPI locally
	echo "launch uvicorn"
	cd backend; uvicorn app.main:app --reload

local-test: clean-pyc ## run test locally
	# clean
	find ./backend/ -name '.pytest_cache' -exec rm -rf {} +
	pytest ./backend/


docker-build: clean-pyc ## build the docker image
	cd backend; poetry export -f requirements.txt --output requirements.txt --without-hashes
	docker build -t fastapi_htmx:0.1.0 .

docker-push: ## push to repository
	docker tag fastapi_htmx:0.1.0 aspadavecchia/fastapi_htmx:0.1.0
	docker push aspadavecchia/fastapi_htmx:0.1.0

docker-run: ## run the container
	docker run -p 8000:80 fastapi_htmx

