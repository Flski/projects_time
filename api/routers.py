from fastapi import APIRouter
from api.login import router as login_router
from api.profile import router as profile_router
from api.project import router as project_router
from api.task import router as task_router

routers = APIRouter()
routers.include_router(login_router)
routers.include_router(profile_router)
routers.include_router(project_router)
routers.include_router(task_router)
