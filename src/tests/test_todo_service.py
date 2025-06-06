import pytest
from typing import Optional, List
from injector import Injector, Module, provides, singleton

from src.domain.models import Todo
from src.domain.repositories import TodoRepository
from src.application.todo_service import TodoService

# モック用のTodoRepository実装
class MockTodoRepository(TodoRepository):
    def __init__(self):
        self._todos: List[Todo] = []

    def save(self, todo: Todo) -> None:
        # 既存のものを更新、または新規追加
        found = False
        for i, existing_todo in enumerate(self._todos):
            if existing_todo.id == todo.id:
                self._todos[i] = todo
                found = True
                break
        if not found:
            self._todos.append(todo)

    def find_by_id(self, todo_id: str) -> Optional[Todo]:
        for todo in self._todos:
            if todo.id == todo_id:
                return todo
        return None

    def find_all(self) -> List[Todo]:
        return list(self._todos)

    def delete_by_id(self, todo_id: str) -> None:
        self._todos = [todo for todo in self._todos if todo.id != todo_id]

# テスト用のDIモジュール
class TestModule(Module):
    @singleton
    @provides(TodoRepository)
    def provide_mock_todo_repository(self) -> TodoRepository:
        return MockTodoRepository()

    @provides(TodoService)
    def provide_todo_service(self, todo_repository: TodoRepository) -> TodoService:
        return TodoService(todo_repository)

@pytest.fixture
def todo_service() -> TodoService:
    injector = Injector([TestModule()])
    return injector.get(TodoService)

def test_create_todo(todo_service: TodoService):
    title = "Test Todo"
    description = "This is a test todo."
    todo = todo_service.create_todo(title, description)

    assert todo.title == title
    assert todo.description == description
    assert not todo.completed
    assert todo_service.get_todo(todo.id) == todo

def test_get_todo_by_id(todo_service: TodoService):
    todo = todo_service.create_todo("Another Todo", None)
    retrieved_todo = todo_service.get_todo(todo.id)
    assert retrieved_todo == todo

    non_existent_todo = todo_service.get_todo("non-existent-id")
    assert non_existent_todo is None

def test_get_all_todos(todo_service: TodoService):
    todo1 = todo_service.create_todo("Todo 1", None)
    todo2 = todo_service.create_todo("Todo 2", None)

    all_todos = todo_service.get_all_todos()
    assert len(all_todos) == 2
    assert todo1 in all_todos
    assert todo2 in all_todos

def test_complete_todo(todo_service: TodoService):
    todo = todo_service.create_todo("Complete Me", None)
    completed_todo = todo_service.complete_todo(todo.id)

    assert completed_todo is not None
    assert completed_todo.completed
    assert todo_service.get_todo(todo.id).completed

    non_existent_completed_todo = todo_service.complete_todo("non-existent-id")
    assert non_existent_completed_todo is None

def test_delete_todo(todo_service: TodoService):
    todo = todo_service.create_todo("Delete Me", None)
    deleted = todo_service.delete_todo(todo.id)
    assert deleted
    assert todo_service.get_todo(todo.id) is None

    not_deleted = todo_service.delete_todo("non-existent-id")
    assert not not_deleted