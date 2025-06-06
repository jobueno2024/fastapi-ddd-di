from injector import Module, singleton, provides, Injector

from src.domain.repositories import TodoRepository
from src.infrastructure.in_memory_todo_repository import InMemoryTodoRepository
from src.application.todo_service import TodoService

class InfrastructureModule(Module):
    @singleton
    @provides(TodoRepository)
    def provide_todo_repository(self) -> TodoRepository:
        return InMemoryTodoRepository()

    # TodoServiceはTodoRepositoryに依存しており、injectorが解決します
    @provides(TodoService)
    def provide_todo_service(self, todo_repository: TodoRepository) -> TodoService:
        return TodoService(todo_repository)