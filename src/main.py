from fastapi import FastAPI
from injector import Injector

from src.infrastructure.di import InfrastructureModule
from src.presentation.todo_router import create_todo_router

def create_app() -> FastAPI:
    app = FastAPI(title="DDD FastAPI Todo App")

    # DIコンテナの初期化
    # ここでアプリケーション全体の依存性を解決するモジュールをロードします
    injector = Injector([InfrastructureModule()])

    # presentation層のルーターを登録
    # ルーターの作成時にinjectorを渡すことで、依存性を注入できるようにします
    app.include_router(create_todo_router(injector))

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)