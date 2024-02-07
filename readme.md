# Установка и запуск
Создайте в корне приложения файл **.env** и определите в нём все переменные, указанные в [.env.example](./.env.example).
___
- заменить **_email_to_** на **_email_to_mock_** в файле [email_and_resize_image_tasks.py](./app/tasks/email_and_resize_image_tasks.py)
Изменял, чтобы самому себе отправить на email информацию о регистрации в приложении
___

___
#### Добавить и настроить sentry
- создать и определить [SENTRY_URL](https://sentry.io/issues/?project=4506698945200128) в **_.env_**
___

___

#### Проверить настройки [Prometheus](http://localhost:9090/targets) в разделе STATUS - TARGETS
- Убедиться, что Prometheus видит наше приложение должно быть **up**
___
___

#### В настройках [Grafana](http://localhost:3000/datasources) добавить prometheus (add data source/Prometheus)

- указать : "URL" = "http://prometheus:9090"  .
**prometheus** это _localhost_  из [docker-compose.yaml](./docker-compose.yaml)


- заменить **_uid_** в [grafana-dashboard.json](./grafana-dashboard.json) на свой созданный выше
выгрузить конфиг [grafana-dashboard.json](./grafana-dashboard.json) или свой конфиг в дашборд
___

## Запуск через docker-compose

#### Собрать и запустить/остановить приложение с помощью
```sh
$ make up_re
$ make up

$ make down
```
или
```sh
$ docker-compose build
$ docker-compose up


$ docker-compose up -d
$ docker-compose down

```


#### Перейти на [http://localhost:8000](http://localhost:8000)
```sh
http://localhost:8000
```


## Локально

#### Установить и активировать виртуальное окружение с помощью команд:
```sh
$ python3.11 -m venv venv
$ source venv/bin/activate
```

#### Установить зависимости:
```sh
$ pip install -r requirements.txt
```


#### Прогнать миграции с помощью с помощью [alembic](https://alembic.sqlalchemy.org/en/latest/):
```sh
$ alembic upgrade head
```


#### Запустить приложение с помощью [uvicorn](https://www.uvicorn.org/):
```sh
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Запустить worker для celery
```sh
celery -A app.config.task_worker:celery_app worker --loglevel=INFO
```


#### Запуск Flower:
посмотреть таски на [Flower](http://localhost:5555)
```sh
celery -A app.config.task_worker:celery_app flower
```
