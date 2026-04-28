"""
Unit Test — TodoList                          ⏱ 15 minuti
================================================
Ciclo per ogni gruppo di test:
  🔴 RED    → esegui: pytest tests/unit/test_models.py -v  (deve fallire)
  🟢 GREEN  → scrivi il minimo codice in todo/models.py
  🔵 REFACTOR → migliora senza rompere i test

Esegui tutti: pytest tests/unit/ -v
"""
import pytest
from todo.models import TodoList, TodoItem


# ─────────────────────────────────────────────────────────────────────────────
# ROUND 1 — Creazione item  (~3 min)
# ─────────────────────────────────────────────────────────────────────────────

class TestTodoItemCreation:

    def test_item_has_title(self):
        item = TodoItem(title="Comprare il latte")
        assert item.title == "Comprare il latte"

    def test_item_starts_not_done(self):
        item = TodoItem(title="Qualcosa")
        assert item.done is False

    def test_item_has_unique_id(self):
        a = TodoItem(title="A")
        b = TodoItem(title="B")
        assert a.id != b.id

    def test_item_complete_sets_done(self):
        item = TodoItem(title="Task")
        item.complete()
        assert item.done is True

    def test_item_uncomplete_unsets_done(self):
        item = TodoItem(title="Task")
        item.complete()
        item.uncomplete()
        assert item.done is False

    def test_item_to_dict_has_all_keys(self):
        item = TodoItem(title="Task")
        d = item.to_dict()
        assert "id" in d
        assert "title" in d
        assert "done" in d


# ─────────────────────────────────────────────────────────────────────────────
# ROUND 2 — Aggiunta item alla lista  (~4 min)
# ─────────────────────────────────────────────────────────────────────────────

class TestTodoListAdd:

    def test_new_list_is_empty(self):
        todo = TodoList()
        assert todo.count == 0

    def test_add_returns_item(self):
        todo = TodoList()
        item = todo.add("Fare la spesa")
        assert isinstance(item, TodoItem)

    def test_add_increases_count(self):
        todo = TodoList()
        todo.add("Uno")
        todo.add("Due")
        assert todo.count == 2

    def test_add_empty_title_raises(self):
        todo = TodoList()
        with pytest.raises(ValueError):
            todo.add("")

    def test_add_whitespace_only_raises(self):
        todo = TodoList()
        with pytest.raises(ValueError):
            todo.add("   ")

    def test_add_strips_whitespace(self):
        todo = TodoList()
        item = todo.add("  Titolo con spazi  ")
        assert item.title == "Titolo con spazi"

    def test_all_returns_all_items(self):
        todo = TodoList()
        todo.add("A")
        todo.add("B")
        assert len(todo.all()) == 2


# ─────────────────────────────────────────────────────────────────────────────
# ROUND 3 — Completamento e conteggio  (~4 min)
# ─────────────────────────────────────────────────────────────────────────────

class TestTodoListComplete:

    def test_complete_marks_item_done(self):
        todo = TodoList()
        item = todo.add("Task")
        todo.complete(item.id)
        assert todo.get(item.id).done is True

    def test_complete_returns_updated_item(self):
        todo = TodoList()
        item = todo.add("Task")
        updated = todo.complete(item.id)
        assert updated.done is True

    def test_complete_unknown_id_raises(self):
        todo = TodoList()
        with pytest.raises(KeyError):
            todo.complete("id-che-non-esiste")

    def test_pending_count_decreases_on_complete(self):
        todo = TodoList()
        todo.add("A")
        todo.add("B")
        item = todo.add("C")
        todo.complete(item.id)
        assert todo.pending_count == 2

    def test_pending_count_equals_count_on_new_list(self):
        todo = TodoList()
        todo.add("A")
        todo.add("B")
        assert todo.pending_count == todo.count


# ─────────────────────────────────────────────────────────────────────────────
# ROUND 4 — Eliminazione e pulizia  (~4 min)
# ─────────────────────────────────────────────────────────────────────────────

class TestTodoListDelete:

    def test_delete_removes_item(self):
        todo = TodoList()
        item = todo.add("Da eliminare")
        todo.delete(item.id)
        assert todo.count == 0

    def test_delete_unknown_id_raises(self):
        todo = TodoList()
        with pytest.raises(KeyError):
            todo.delete("id-che-non-esiste")

    def test_delete_only_removes_target(self):
        todo = TodoList()
        a = todo.add("A")
        b = todo.add("B")
        todo.delete(a.id)
        assert todo.get(b.id) is not None

    def test_clear_completed_removes_done_items(self):
        todo = TodoList()
        a = todo.add("A")
        todo.add("B")
        todo.complete(a.id)
        todo.clear_completed()
        assert todo.count == 1

    def test_clear_completed_returns_count_removed(self):
        todo = TodoList()
        a = todo.add("A")
        b = todo.add("B")
        todo.add("C")
        todo.complete(a.id)
        todo.complete(b.id)
        removed = todo.clear_completed()
        assert removed == 2

    def test_clear_completed_keeps_pending(self):
        todo = TodoList()
        item = todo.add("Pending")
        todo.add("Done")
        todo.complete(todo.all()[1].id)
        todo.clear_completed()
        assert todo.get(item.id) is not None
