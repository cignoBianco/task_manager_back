from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger
import app.models_imports

from app.auth.router import router as router_auth
from app.engeneering_roles.router import router as engineering_roles_router
from app.workspaces.router import router as workspaces_router
from app.projects.router import router as projects_router
from app.tasks.router import router as tasks_router
from app.members.router import router as members_router
from app.meetings.router import router as meetings_router
from app.task_comments.router import router as comments_router

from app.dependencies.auth_dep import get_current_user


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
    """Управление жизненным циклом приложения."""
    logger.info("Инициализация приложения...")
    yield
    logger.info("Завершение работы приложения...")


def create_app() -> FastAPI:
    """
   Создание и конфигурация FastAPI приложения.

   Returns:
       Сконфигурированное приложение FastAPI
   """
    app = FastAPI(
        title="FastAPI",
        description=(
            "hello"
        ),
        version="1.0.0",
        lifespan=lifespan,
        root_path="/api"
    )

    # Настройка CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000","http://127.0.0.1:3000",],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # Монтирование статических файлов
    app.mount(
        '/static',
        StaticFiles(directory='app/static'),
        name='static'
    )

    # Регистрация роутеров
    register_routers(app)

    return app


def register_routers(app: FastAPI) -> None:
    """Регистрация роутеров приложения."""
    # Корневой роутер
    root_router = APIRouter()

    @root_router.get("/", tags=["root"])
    def home_page():
        return {
            "message": "Hello World"
        }

    # Подключение роутеров
    app.include_router(root_router, tags=["root"])
    app.include_router(router_auth, prefix='/auth', tags=['Auth'])
    app.include_router(
        engineering_roles_router,
        prefix='/engineering_roles',
        tags=['Engineering Roles'],
        dependencies=[Depends(get_current_user)] # Глобальная проверка для этого роутера
    )
    app.include_router(
        workspaces_router,
        prefix="/workspaces",
        tags=["Workspaces"],
        dependencies=[Depends(get_current_user)]
    )
    app.include_router(
        projects_router,
        prefix="/projects",
        tags=["Projects"],
        dependencies=[Depends(get_current_user)]
    )
    app.include_router(
        tasks_router,
        prefix="/tasks",
        tags=["Tasks"],
        dependencies=[Depends(get_current_user)]
    )
    app.include_router(
        members_router,
        prefix="/members",
        tags=["Members"],
        dependencies=[Depends(get_current_user)]
    )
    app.include_router(
        meetings_router,
        prefix="/meetings",
        tags=["Meetings"],
        dependencies=[Depends(get_current_user)]
    )
    app.include_router(
        comments_router,
        prefix="/comments",
        tags=["Comments"],
        dependencies=[Depends(get_current_user)]
    )

# Создание экземпляра приложения
app = create_app()
