from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import api_router, html_router
from .sql import prime_database
from .sql.models import Base
from .sql.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(api_router)
app.include_router(html_router)

prime_database()
