
build_billing_dev:
	docker compose -f docker-compose.dev.yaml up --build -d

sub_pay_db_dev:
	docker compose -f docker-compose.dev.yaml up payment_api subscription_api postgres --build -d

sub_db_dev:
	docker compose -f docker-compose.dev.yaml up subscription_api postgres --build -d

db_dev:
	docker compose -f docker-compose.dev.yaml up postgres --build -d
