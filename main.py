import json

from datetime import date as d
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from models import Item


# Запускаем
app = FastAPI(title="Tortoise ORM FastAPI example")

# Считываем данные из файла data.json
with open('data.json', 'r', encoding='utf-8') as fh:  # открываем файл на чтение
    data = json.load(fh)  # загружаем из файла данные в словарь


@app.post("/")
async def create_item(cargo_type: str = 'None', declared_value: int = 0):
    """
    Заполняем базу данных из считанных данных, если в ней нет таких данных
    Обновляем все значения
    Считаем страховку
    Выдаем ответ
    ВАЖНО - Актуальный тариф на день запроса.
    """
    for date in data:
        if data[date]:
            # if cargo_type in data:
                for rez in data[date]:
                    cargo = rez['cargo_type']
                    rate = rez['rate']
                    await Item.get_or_create(date=date, cargo_type=cargo)
                    await Item.filter(date=date, cargo_type=cargo).update(rate=rate)
            # else:
            #     return {"mes":"Мы не обрабатывает такой груз"}
        else:
            return{"mes": " Мы пока не подобрали тариф на эту дату"}


    item = await Item.filter(cargo_type=cargo_type, date=d.today()).first()

    if item is None:
        return {"mes":"Неверный тип груза"}

    rate_today = item.rate
    insurance = declared_value * rate_today

    return {"Cargo_type": cargo_type,
            "Declared value": declared_value,
            "Insurance": insurance}

@app.get("/")
async def create_item():
    return {"mes": "Сервер запущен и работает"}


# Соединяем с базой данных
register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True,
)
