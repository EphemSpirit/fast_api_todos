from dotenv import load_dotenv
from fastapi import FastAPI
from app.extensions import engine, Base
from app.models import *
from app.routers import routers

load_dotenv()

def create_app():
    app = FastAPI()

    @app.get("/healthy")
    def health_check():
        return {"status": "healthy"}

    for router in routers:
        app.include_router(router)

    Base.metadata.create_all(bind=engine)

    return app