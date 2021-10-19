
run_celery_worker:
	celery -A core.celery_app worker --loglevel=DEBUG -Q payments

run_celery_scheduler:
	celery -A core.celery_app beat