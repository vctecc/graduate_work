# Проектная работа: диплом
## Запуск инфраструктуры для разработки
```shell
docker compose -f docker-compose.dev.yaml --env-file dev.env up --build
```

## Локальный запуск user subscription api
После поднятия инфраструктуры, нужно задать путь к приложению
и выполнить миграции.

Можно воспользоваться скриптом:
```shell
cd ./user_subscription_api
./prestart.sh
```
Либо выполнить руками:
```shell
cd ./user_subscription_api
export PATHONPATH=$(readlink -f ./)
alembic upgrade head
```
