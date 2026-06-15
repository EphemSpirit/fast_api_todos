from .todos import router as todos_router
from .auth import router as auth_router

routers = [todos_router, auth_router]