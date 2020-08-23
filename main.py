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


@app.post("/items/")
async def create_item(cargo_type: str = 'None', base_sum: int = 0):
    """
    Заполняем базу данных из считанных данных, если в ней нет таких данных

    Считаем страховку
    Выдаем ответ
    """
    for date in data:
        if data[date]:
            for rez in data[date]:
                cargo = rez['cargo_type']
                rate = rez['rate']
                await Item.get_or_create(date=date, cargo_type=cargo)
                await Item.filter(date=date, cargo_type=cargo).update(rate=rate)
                print(111111111)


    print(await Item.all())
    item = await Item.filter(cargo_type=cargo_type, date=d.today()).first()
    rate_today = item.rate
    insurance = base_sum * rate_today

    return {"Cargo_type": cargo_type,
            "Base_sum": base_sum,
            "Insurance": insurance}


# Соединяем с базой данных
register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True,
)
