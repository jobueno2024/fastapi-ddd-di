from pydantic import BaseModel
from typing import Optional
import uuid

class Todo(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    completed: bool = False

    @staticmethod
    def create(title: str, description: Optional[str] = None) -> 'Todo':
        return Todo(id=str(uuid.uuid4()), title=title, description=description, completed=False)

    def mark_as_completed(self) -> None:
        self.completed = True