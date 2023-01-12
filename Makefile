docker-build:
	docker build -t postgres-data-volume .

docker-run:
	docker run -p 5432:5432 -v $(shell pwd)/data:/var/lib/postgresql/data \
		-e POSTGRES_USER=kvmp -e POSTGRES_PASSWORD=password -d postgres-data-volume

dbmate:
	docker run --rm -v $(shell pwd)/db:/db ghcr.io/amacneil/dbmate:1 ${cmd}

run:
	export FLASK_RUN_HOST=0.0.0.0 && \
	export FLASK_RUN_PORT=3000 && \
	poetry run flask --debug --app kvmp.control_panel run

dbmate-new:
	dbmate new ${file}

dbmate-up:
	dbmate -e DATABASE_URL up

dbmate-down:
	dbmate -e DATABASE_URL down

dbmate-test-up:
	dbmate -e DBMATE_TEST_DATABASE_URL up

dbmate-test-down:
	dbmate -e DBMATE_TEST_DATABASE_URL down

test-s:
	poetry run pytest -s

test:
	poetry run pytest