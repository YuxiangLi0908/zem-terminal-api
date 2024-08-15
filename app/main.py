from typing import Union
import pandas as pd

from sqlalchemy import text
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.test_db_conn import conn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(GZipMiddleware)

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/dbtest")
async def read_db():
    # cursor = conn.cursor()
    # return {"tables": text(cursor.execute("SELECT * FROM information_schema.tables"))}
    # df = pd.read_sql('SELECT * FROM information_schema.tables', con=conn)
    df = pd.read_sql("SELECT * FROM public.warehouse_vessel WHERE vessel_eta > '2024-08-01'", con=conn)
    return {"tables": df.to_dict()}