from .todos import router as todos_router
from .auth import router as auth_router
from .users import router as user_router
from .admin import router as admin_router

routers = [todos_router, auth_router, user_router, admin_router]