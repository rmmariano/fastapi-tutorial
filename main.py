# pylint: disable=invalid-name
"""main"""
from enum import Enum
from typing import Annotated, Any

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root() -> dict[str, str]:
    """root function"""
    return {"message": "Hello World"}


@app.get("/items/1/{item_id}")
async def read_item1(item_id: str) -> dict[str, str]:
    """read_item1 function"""
    return {"item_id": item_id}  # item_id: str


@app.get("/items/2/{item_id}")
async def read_item2(item_id: int) -> dict[str, int]:
    """read_item2 function"""
    return {"item_id": item_id}  # item_id: int


class ModelName(str, Enum):
    """ModelName enum class"""

    ALEXNET = "ALEXNET"
    RESNET = "RESNET"
    LENET = "LENET"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName) -> dict[str, str]:
    """get_model function"""
    if model_name is ModelName.ALEXNET:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "LENET":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str) -> dict[str, str]:
    """read_file function"""
    return {"file_path": file_path}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item3(skip: int = 0, limit: int = 10) -> list[dict[str, str]]:
    """read_item3 function"""
    # http://127.0.0.1:8000/items/?skip=0&limit=10
    return fake_items_db[skip : skip + limit]


@app.get("/items/{item_id}")
async def read_item4(item_id: str, q: str | None = None) -> dict[str, str]:
    """read_item4 function"""
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@app.get("/items/{item_id}")
async def read_item5(
    item_id: str, q: str | None = None, short: bool = False
) -> dict[str, str]:
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


class Item(BaseModel):
    """Item model"""

    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items/")
async def create_item1(item: Item) -> Item:
    """create_item1 function"""
    # item.price + item.name
    return item


@app.post("/items/")
async def create_item2(item: Item) -> dict[str, Any]:
    """create_item2 function"""
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
async def create_item3(
    item_id: int, item: Item, q: str | None = None
) -> dict[str, Any]:
    """create_item2 function"""
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


@app.get("/items/")
async def read_items1(
    q: Annotated[
        str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")
    ] = None
) -> dict[str, Any]:
    """read_items1 function"""
    results: dict[str, Any] = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/")
async def read_items2(q: Annotated[list[str] | None, Query()] = None) -> dict[str, Any]:
    """read_items2 function"""
    # http://localhost:8000/items/?q=foo&q=bar
    query_items = {"q": q}
    return query_items


@app.get("/items/")
async def read_items3(
    q: Annotated[
        str | None,
        Query(
            alias="item-query",
            title="Query string",
            description=(
                "Query string for the items to search"
                "in the database that have a good match"
            ),
            min_length=3,
            max_length=50,
            pattern="^fixedquery$",
            deprecated=True,
        ),
    ] = None
) -> dict[str, Any]:
    """read_items3 function"""
    results: dict[str, Any] = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
