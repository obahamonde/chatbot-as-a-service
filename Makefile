dev:
	sh ./scripts/run.sh

build:
	docker build -t app . 

run:
	docker run -v $(PWD):/app -d -p 8080:8080 app

.PHONY: run build