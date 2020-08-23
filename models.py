from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model


class Item(Model):
    date = fields.CharField(max_length=10)
    cargo_type = fields.CharField(max_length=255)
    rate = fields.FloatField(default=0.0)

    class Meta:
        table = 'Item_DB'


Item_Pydantic = pydantic_model_creator(Item, name="Item")
