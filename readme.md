## Установка и запуск

### Через docker-compose
Создайте в корне приложения файл .env и определите в нем все переменные, указанные в [.env.example](./.env.example).


Соберите и запустите приложение с помощью
```sh
$ docker-compose build
$ docker-compose up


$ docker-compose up -d
$ docker-compose down


```

Перейти на
```sh
http://localhost:8000
```






### Локально

Установите и активируйте виртуальное окружение с помощью команд:
```sh
$ python3.11 -m venv venv
$ source venv/bin/activate
```


Установите зависимости:
```sh
$ pip install -r requirements.txt
```



Прогоните миграции с помощью команды:
```sh
$ alembic upgrade head
```


Запустите приложение с помощью [uvicorn](https://www.uvicorn.org/):
```sh
$ uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```




Запустите worker на загрузку картинок
```sh
$ celery -A app.config.task_worker:celery_app worker --loglevel=INFO
```