## Установка и запуск
```sh
 #заменить email_to!!!!!! на email_to_mock!. в файле
  email_and_resize_image_tasks.py
 заменял чтобы самому себе отправить для теста
```
### Через docker-compose
Создайте в корне приложения файл .env и определите в нём все переменные, указанные в [.env.example](./.env.example).


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
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```




Запустите worker
```sh
celery -A app.config.task_worker:celery_app worker --loglevel=INFO
```


запуск Flower
посмотреть таски на порту "http://localhost:5555"
```sh
celery -A app.config.task_worker:celery_app flower
```

добавить в sentry project
```
https://sentry.io/issues/?project=4506698945200128
```

проверить настройки prometheus в разделе STATUS - TARGETS
проверить что видит наше приложение должно быть(up)
```
http://localhost:9090/targets
```

в grafana добавить prometheus (add data source/Prometheus)


```
в настрйоках подключения "URL" указать "http://prometheus:9090"  -> localhost(prometheus) из docker-compose
http://localhost:3000/datasources
```