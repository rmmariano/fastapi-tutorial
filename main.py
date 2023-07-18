"""main"""
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
