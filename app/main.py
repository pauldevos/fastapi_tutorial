from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from .models import Item

app = FastAPI()

@app.get("/")
async def root():
    return {"Message": "Hello World from FastAPI!"}

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict