from typing import Optional
from fastapi import FastAPI
from .models import ModelName

app = FastAPI()

@app.get("/")
async def root():
    return {"Message": "Hello World from FastAPI!"}

@app.get("/elements/{element_id}")
def read_item(element_id: int, q: Optional[str] = None):
    return {"element_id": element_id, "q": q}

@app.get("/products/{product_id}")
async def read_product(product_id: int, q: Optional[str] = None, short: bool = False):
    product = {"product_id": product_id}
    if q:
        product.update({"q": q})
    if not short:
        product.update({"description":
        "This is an amazing product that has a long description!"}
        )
    return product

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: Optional[int] = None
): # item_id required, needy required, skip has default, limit is optional
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/") # defaults for skip and limit, can enter in query and will ovveride.
# e.g. http://127.0.0.1:8000/items/?skip=20
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}