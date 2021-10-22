
build_billing_dev:
	docker compose -f docker-compose.dev.yaml up --build -d

sub_pay_db_dev:
	docker compose -f docker-compose.dev.yaml up payment_api subscription_api postgres --build -d

db_dev:
	docker compose -f docker-compose.dev.yaml up postgres --build -d

rabbit_dev:
	docker compose -f docker-compose.dev.yaml up rabbit --build -d

db_payment_scheduler_dev:
	docker compose -f docker-compose.dev.yaml up postgres payment_scheduler payment_worker rabbit --build -d

restart_payments_worker:
	docker compose -f docker-compose.dev.yaml restart payment_worker
