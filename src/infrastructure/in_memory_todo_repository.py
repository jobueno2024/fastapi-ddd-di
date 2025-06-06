from typing import List, Dict, Optional

from src.domain.models import Todo
from src.domain.repositories import TodoRepository

class InMemoryTodoRepository(TodoRepository):
    def __init__(self) -> None:
        self._todos: Dict[str, Todo] = {}

    def save(self, todo: Todo) -> None:
        self._todos[todo.id] = todo

    def find_by_id(self, todo_id: str) -> Optional[Todo]:
        return self._todos.get(todo_id)

    def find_all(self) -> List[Todo]:
        return list(self._todos.values())

    def delete_by_id(self, todo_id: str) -> None:
        if todo_id in self._todos:
            del self._todos[todo_id]