# Биллинг

## Запуск инфраструктуры для разработки
```shell
make build_billing_dev
```

## Инициаилазция баз
```shell
docker exec -it postgres sh
cd docker-entrypoint-initdb.d/
sh init_multitype_db.sh
```

## Локальный запуск user subscription api
После поднятия инфраструктуры, нужно задать путь к приложению
и выполнить миграции.

Можно воспользоваться скриптом:
```shell
cd ./subscription_api
./prestart.sh
```
Либо выполнить руками:
```shell
cd ./subscription_api
export PYTHONPATH=$(readlink -f ./)
alembic upgrade head
```
