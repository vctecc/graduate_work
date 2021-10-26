build:
	docker compose -f docker-compose.dev.yaml up --build -d

dev:
	docker compose -f docker-compose.dev.yaml up postgres rabbit redis --build -d

init_db:
	docker exec -it payment_api bash -c 'cd src/db/; alembic upgrade head'
	docker exec -it subscription_api bash -c 'alembic upgrade head'
	docker exec -it subscription_api bash -c 'python init_test_data.py'

all:
	make build
	make init_db

stop:
	docker compose -f docker-compose.dev.yaml stop

clean:
	make stop
	docker compose -f docker-compose.dev.yaml rm --force

test:
	make test_build
	make init_db
	make test_run
	make test_clear

test_build:
	docker compose -f docker-compose.test.yaml up --build -d

test_run:
	docker exec -it payment_api bash -c 'cd tests/functional; pytest'
	docker exec -it subscription_api bash -c 'cd tests/functional; pytest'

test_clear:
	docker compose -f docker-compose.test.yaml stop
	docker compose -f docker-compose.test.yaml rm --force
	docker volume rm redis_data_test
	docker volume rm postgresdata_test
