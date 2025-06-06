from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from injector import Injector

from src.application.todo_service import TodoService
from src.domain.models import Todo

# リクエストボディのスキーマ
class TodoCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None

class TodoResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    completed: bool

# todo_routerのFactory関数
def create_todo_router(injector: Injector) -> APIRouter:
    router = APIRouter(prefix="/todos", tags=["todos"])

    # 依存性注入のためのヘルパー関数
    def get_todo_service() -> TodoService:
        return injector.get(TodoService)

    @router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
    def create_todo(
        request: TodoCreateRequest,
        todo_service: TodoService = Depends(get_todo_service)
    ) -> Todo:
        todo = todo_service.create_todo(request.title, request.description)
        return TodoResponse.model_validate(todo.model_dump())

    @router.get("/", response_model=List[TodoResponse])
    def get_all_todos(
        todo_service: TodoService = Depends(get_todo_service)
    ) -> List[Todo]:
        todos = todo_service.get_all_todos()
        return [TodoResponse.model_validate(todo.model_dump()) for todo in todos]

    @router.get("/{todo_id}", response_model=TodoResponse)
    def get_todo_by_id(
        todo_id: str,
        todo_service: TodoService = Depends(get_todo_service)
    ) -> Todo:
        todo = todo_service.get_todo(todo_id)
        if not todo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        return TodoResponse.model_validate(todo.model_dump())

    @router.put("/{todo_id}/complete", response_model=TodoResponse)
    def complete_todo(
        todo_id: str,
        todo_service: TodoService = Depends(get_todo_service)
    ) -> Todo:
        todo = todo_service.complete_todo(todo_id)
        if not todo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        return TodoResponse.model_validate(todo.model_dump())

    @router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_todo(
        todo_id: str,
        todo_service: TodoService = Depends(get_todo_service)
    ) -> None:
        if not todo_service.delete_todo(todo_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        return

    return router