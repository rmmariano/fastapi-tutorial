"""main"""
from enum import Enum

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    """root function"""
    return {"message": "Hello World"}


@app.get("/items/1/{item_id}")
async def read_item1(item_id):
    """read_item1 function"""
    return {"item_id": item_id}  # item_id: str


@app.get("/items/2/{item_id}")
async def read_item2(item_id: int):
    """read_item2 function"""
    return {"item_id": item_id}  # item_id: int


class ModelName(str, Enum):
    """ModelName enum class"""

    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    """get_model function"""
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    """read_file function"""
    return {"file_path": file_path}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item3(skip: int = 0, limit: int = 10):
    """read_item3 function"""
    # http://127.0.0.1:8000/items/?skip=0&limit=10
    return fake_items_db[skip : skip + limit]


@app.get("/items/{item_id}")
async def read_item4(item_id: str, q: str | None = None):
    """read_item4 function"""
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@app.get("/items/{item_id}")
async def read_item5(item_id: str, q: str | None = None, short: bool = False):
    """read_item5 function"""
    # http://127.0.0.1:8000/items/foo?short=1
    # http://127.0.0.1:8000/items/foo?short=True
    # http://127.0.0.1:8000/items/foo?short=true
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
