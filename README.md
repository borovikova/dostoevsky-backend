### Как пользоваться

Запустить сервер в докере:

`docker-compose build`

`docker-compose up`

Создать суперпользователя

`docker-compose run app sh -c "python manage.py createsuperuser`

Заполнить базу данных (несколько минут):

`docker-compose run app sh -c "python manage.py fill_db"`

Получить токен для доступа к api:

отправить на `http://localhost:8000/token/` `POST`-запрос вида 

```
{
    "username": "user", "password": "password"
}
```

Все данные за все года отдаются по `GET`-запросу на `/api/data/`. Например, `http://localhost:8000/api/data/`
Пример ответа:

```
[
    {
        "id": 1,
        "clause": "185.4",
        "part": "185.4ч.1",
        "name": "Воспрепятствование осуществлению или незаконное ограничение прав владельцев ценных бумаг",
        "year": 2016,
        "category": "экономической направленности",
        "parameters": {
            "addFine": 0,
            "addFine5": 0,
            "acquittal": 0,
            "addFine1M": 0,
            "addFine5_25": 0,
            "addRestrain": 0,
            "primaryFine": 0,
            ...
        }
    }
]
```


TODO:

- README
- swagger
- linters
- env variables
- reduce docker image
