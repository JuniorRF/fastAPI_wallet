# fastAPI_wallet
## Тестовое задание OOO "ИТК"

### Установка зависимостей
```pip -r reqiurements.txt```


### запуск
```uvicorn backend.main:app```   с ключём `--reload` вразработке

### [localhost](http://127.0.0.1:8000/docs#/)

### Миграции alembic
```alembic revision --autogenerate -m "комментарий для удобства"```
```alembic haed``` 