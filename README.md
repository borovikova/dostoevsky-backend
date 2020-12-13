### Как пользоваться

Запустить сервер в докере, провести миграции, собрать статику, создать суперюзера и заполнить базу:

```
docker-compose up -d --build
docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py collectstatic --no-input --clear
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py fill_db
```

Получить токен для доступа к api:

отправить на `http://localhost:8000/token/` `POST`-запрос вида 

```
{
    "username": "user", "password": "password"
}
```

Все данные за все года отдаются по `GET`-запросу на `/api/data/`. Например, `http://localhost:8000/api/data/`

Токен должен быть в headers запроса: `Authorization: Token <token>`

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

Описание работы api также доступно по `/swagger/`
