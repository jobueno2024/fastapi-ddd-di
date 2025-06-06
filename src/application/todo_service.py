from typing import List, Optional
from injector import inject

from src.domain.models import Todo
from src.domain.repositories import TodoRepository

class TodoService:
    @inject
    def __init__(self, todo_repository: TodoRepository) -> None:
        self.todo_repository = todo_repository

    def create_todo(self, title: str, description: Optional[str]) -> Todo:
        todo = Todo.create(title=title, description=description)
        self.todo_repository.save(todo)
        return todo

    def get_todo(self, todo_id: str) -> Optional[Todo]:
        return self.todo_repository.find_by_id(todo_id)

    def get_all_todos(self) -> List[Todo]:
        return self.todo_repository.find_all()

    def complete_todo(self, todo_id: str) -> Optional[Todo]:
        todo = self.todo_repository.find_by_id(todo_id)
        if todo:
            todo.mark_as_completed()
            self.todo_repository.save(todo)
        return todo

    def delete_todo(self, todo_id: str) -> bool:
        existing_todo = self.todo_repository.find_by_id(todo_id)
        if existing_todo:
            self.todo_repository.delete_by_id(todo_id)
            return True
        return False