from typing import Optional, List
from fastapi import FastAPI, Query, Path
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

@app.get("/products/")
async def read_items(q: Optional[str] = Query(None, min_length=3, max_length=50)):
    results = {"products": [{"item_id": "Foo"}, {"item_id": "Bar"} ]}
    if q:
        results.update({"q": q})
    return results

@app.get("/list_default/")
async def read_items(q: List = Query(["foo", "bar"])):
    query_items = {"q": q}
    return query_items

# http://127.0.0.1:8000/items/2?item-query=include%20me
@app.get("/items/{item_id}")
async def get_items(item_id: int = Path(..., title="The ID of the item to get"),
    q: Optional[str] = Query(None, alias='item-query')):
    # "..." = Ellipsis, special single value.
    results = {'item_id': item_id}
    if q:
        results.update({'q': q})
    return results
