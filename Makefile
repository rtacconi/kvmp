export DATABASE_URL=postgresql://kvmp:password@127.0.0.1:5432/kvmp?sslmode=disable
export TEST_DATABASE_URL=postgresql://kvmp:password@127.0.0.1:5432/kvmp_test?sslmode=disable
export DBMATE_DATABASE_URL=postgresql://kvmp:password@127.0.0.1:5432/kvmp?sslmode=disable
export DBMATE_TEST_DATABASE_URL=postgresql://kvmp:password@127.0.0.1:5432/kvmp_test?sslmode=disable
export CELERY_BROKER_URL=redis://localhost:6379/0
export CELERY_RESULT_BACKEND=redis://localhost:6379/0

build:
	docker build -t postgres-data-volume .

docker-run:
	docker run -p 5432:5432 -v $(shell pwd)/data:/var/lib/postgresql/data \
		-e POSTGRES_USER=kvmp -e POSTGRES_PASSWORD=password -d postgres:15.1
	docker run -p 6379:6379 -d redis redis-server --save 60 1 --loglevel warning

stop:
	docker stop $(shell docker ps -qa)

list:
	@docker ps
 
clean:
	docker rm $(shell docker ps -qa)
	docker rmi -f $(shell docker images -q)

dbmate:
	docker run --rm -v $(shell pwd)/db:/db ghcr.io/amacneil/dbmate:1 ${cmd}

c:
	poetry run celery --app kvmp.celery worker --loglevel=info

shell:
	export DATABASE_URL
	export TEST_DATABASE_URL
	export DBMATE_DATABASE_URL
	export DBMATE_TEST_DATABASE_URL
	export CELERY_BROKER_URL
	export CELERY_RESULT_BACKEND
	export FLASK_RUN_HOST=0.0.0.0 && \
	export FLASK_RUN_PORT=3000 && \
	poetry run flask --app kvmp.control_panel shell	

run: stop docker-run
	export DATABASE_URL
	export TEST_DATABASE_URL
	export DBMATE_DATABASE_URL
	export DBMATE_TEST_DATABASE_URL
	export CELERY_BROKER_URL
	export CELERY_RESULT_BACKEND
	sleep 1
	dbmate -e DBMATE_DATABASE_URL up
	export FLASK_RUN_HOST=0.0.0.0 && \
	export FLASK_RUN_PORT=3000 && \
	poetry run flask --debug --app kvmp.control_panel run

dbmate-new:
	dbmate new ${file}

dbmate-up:
	dbmate -e DBMATE_DATABASE_URL up

dbmate-down:
	dbmate -e DBMATE_DATABASE_URL down

dbmate-test-up:
	dbmate -e DBMATE_TEST_DATABASE_URL up

dbmate-test-down:
	dbmate -e DBMATE_TEST_DATABASE_URL down

test-s:
	poetry run pytest -s

test:
	poetry run pytest

celery:
	celery -A kvmp.celery worker --loglevel=info


.PHONY: psql
psql:
	docker exec -it $(shell docker ps | grep postgres | awk '{print $$1}') psql -U kvmp -d kvmp