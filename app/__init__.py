from dotenv import load_dotenv
from fastapi import FastAPI
from app.extensions import engine, Base
from app.models import *

load_dotenv()

def create_app():
    app = FastAPI()

    from app.routes import register_routes
    register_routes(app)

    Base.metadata.create_all(bind=engine)

    return app