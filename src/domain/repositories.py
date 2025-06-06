from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models import Todo

class TodoRepository(ABC):
    @abstractmethod
    def save(self, todo: Todo) -> None:
        pass

    @abstractmethod
    def find_by_id(self, todo_id: str) -> Optional[Todo]:
        pass

    @abstractmethod
    def find_all(self) -> List[Todo]:
        pass

    @abstractmethod
    def delete_by_id(self, todo_id: str) -> None:
        pass