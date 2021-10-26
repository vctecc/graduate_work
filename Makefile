
build_billing_dev:
	docker compose -f docker-compose.dev.yaml up --build -d

db_dev:
	docker compose -f docker-compose.dev.yaml up postgres rabbit redis --build -d

init_db:
	docker exec -it payment_api bash -c 'cd src/db/; alembic upgrade head'
	docker exec -it subscription_api bash -c 'cd src/db/; alembic upgrade head'
	docker exec -it subscription_api bash -c 'python init_test_data.py'

test: $(CLEAR)
	make test_build
	make init_db
	make test_run

	if $(CLEAR)
		make test_clear
	endif

test_build:
	docker compose -f docker-compose.test.yaml up --build -d

test_run:
	docker exec -it payment_api bash -c 'cd tests/functional/; pytest'
	docker exec -it payment_api bash -c 'cd tests/integration/; pytest'
	docker exec -it subscription_api bash -c 'cd tests/functional/; pytest'
	docker exec -it subscription_api bash -c 'cd tests/integration/; pytest'

test_clear:
	docker compose -f docker-compose.test.yaml stop
	docker compose -f docker-compose.test.yaml rm --force
	docker volume rm redis_data_test
	docker volume rm postgresdata_test

