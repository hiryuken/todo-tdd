"""
Integration Test — Flask API                  ⏱ 10 minuti
================================================
Questi test verificano routing HTTP, serializzazione JSON
e stato condiviso tra chiamate successive.

Esegui: pytest tests/integration/ -v
"""
import pytest
from todo.app import app, _todo


@pytest.fixture(autouse=True)
def reset_todo():
    """Ricomincia con lista vuota prima di ogni test."""
    _todo._items.clear()
    yield
    _todo._items.clear()


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# ── Health ───────────────────────────────────────────────────────────────────

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


# ── GET /todos ────────────────────────────────────────────────────────────────

class TestGetTodos:

    def test_empty_list_returns_200(self, client):
        r = client.get("/todos")
        assert r.status_code == 200

    def test_empty_list_structure(self, client):
        data = client.get("/todos").get_json()
        assert data["items"] == []
        assert data["count"] == 0
        assert data["pending"] == 0

    def test_returns_added_items(self, client):
        client.post("/todos", json={"title": "Primo"})
        data = client.get("/todos").get_json()
        assert data["count"] == 1
        assert data["items"][0]["title"] == "Primo"


# ── POST /todos ───────────────────────────────────────────────────────────────

class TestCreateTodo:

    def test_create_returns_201(self, client):
        r = client.post("/todos", json={"title": "Task"})
        assert r.status_code == 201

    def test_create_returns_item(self, client):
        data = client.post("/todos", json={"title": "Task"}).get_json()
        assert data["title"] == "Task"
        assert data["done"] is False
        assert "id" in data

    def test_create_empty_title_returns_400(self, client):
        r = client.post("/todos", json={"title": ""})
        assert r.status_code == 400

    def test_create_missing_title_returns_400(self, client):
        r = client.post("/todos", json={})
        assert r.status_code == 400


# ── PATCH /todos/<id>/complete ────────────────────────────────────────────────

class TestCompleteTodo:

    def test_complete_returns_200(self, client):
        item = client.post("/todos", json={"title": "Task"}).get_json()
        r = client.patch(f"/todos/{item['id']}/complete")
        assert r.status_code == 200

    def test_complete_sets_done_true(self, client):
        item = client.post("/todos", json={"title": "Task"}).get_json()
        updated = client.patch(f"/todos/{item['id']}/complete").get_json()
        assert updated["done"] is True

    def test_complete_unknown_id_returns_404(self, client):
        r = client.patch("/todos/id-inesistente/complete")
        assert r.status_code == 404

    def test_complete_updates_pending_count(self, client):
        """Test multi-step: crea → completa → verifica contatori."""
        client.post("/todos", json={"title": "A"})
        item = client.post("/todos", json={"title": "B"}).get_json()
        client.patch(f"/todos/{item['id']}/complete")
        data = client.get("/todos").get_json()
        assert data["pending"] == 1
        assert data["count"] == 2


# ── DELETE /todos/<id> ────────────────────────────────────────────────────────

class TestDeleteTodo:

    def test_delete_returns_200(self, client):
        item = client.post("/todos", json={"title": "Task"}).get_json()
        r = client.delete(f"/todos/{item['id']}")
        assert r.status_code == 200

    def test_delete_removes_item(self, client):
        item = client.post("/todos", json={"title": "Task"}).get_json()
        client.delete(f"/todos/{item['id']}")
        assert client.get("/todos").get_json()["count"] == 0

    def test_delete_unknown_id_returns_404(self, client):
        r = client.delete("/todos/id-inesistente")
        assert r.status_code == 404


# ── DELETE /todos/completed ───────────────────────────────────────────────────

class TestClearCompleted:

    def test_clear_completed_returns_removed_count(self, client):
        a = client.post("/todos", json={"title": "A"}).get_json()
        client.post("/todos", json={"title": "B"})
        client.patch(f"/todos/{a['id']}/complete")
        data = client.delete("/todos/completed").get_json()
        assert data["removed"] == 1

    def test_clear_completed_leaves_pending(self, client):
        a = client.post("/todos", json={"title": "A"}).get_json()
        client.post("/todos", json={"title": "B"})
        client.patch(f"/todos/{a['id']}/complete")
        client.delete("/todos/completed")
        assert client.get("/todos").get_json()["count"] == 1
