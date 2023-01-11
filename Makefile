docker-build:
	docker build -t postgres-data-volume .

docker-run:
	docker run -p 5432:5432 -v $(shell pwd)/data:/var/lib/postgresql/data \
		-e POSTGRES_USER=kvmp -e POSTGRES_PASSWORD=password -d postgres-data-volume

dbmate:
	docker run --rm -v $(shell pwd)/db:/db ghcr.io/amacneil/dbmate:1 ${cmd}