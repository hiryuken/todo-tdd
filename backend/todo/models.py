from dataclasses import dataclass, field
from typing import List, Optional
import uuid


@dataclass
class TodoItem:
    title: str
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    done: bool = False

    def complete(self):
        self.done = True

    def uncomplete(self):
        self.done = False

    def to_dict(self) -> dict:
        return {"id": self.id, "title": self.title, "done": self.done}


class TodoList:
    def __init__(self):
        self._items: List[TodoItem] = []

    # ── query ──────────────────────────────────────────────────────────────

    def all(self) -> List[TodoItem]:
        return list(self._items)

    def get(self, item_id: str) -> Optional[TodoItem]:
        return next((i for i in self._items if i.id == item_id), None)

    @property
    def count(self) -> int:
        return len(self._items)

    @property
    def pending_count(self) -> int:
        return sum(1 for i in self._items if not i.done)

    # ── commands ───────────────────────────────────────────────────────────

    def add(self, title: str) -> TodoItem:
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        item = TodoItem(title=title.strip())
        self._items.append(item)
        return item

    def complete(self, item_id: str) -> TodoItem:
        item = self.get(item_id)
        if item is None:
            raise KeyError(f"Item '{item_id}' not found")
        item.complete()
        return item

    def delete(self, item_id: str) -> None:
        item = self.get(item_id)
        if item is None:
            raise KeyError(f"Item '{item_id}' not found")
        self._items.remove(item)

    def clear_completed(self) -> int:
        before = self.count
        self._items = [i for i in self._items if not i.done]
        return before - self.count
