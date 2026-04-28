from flask import Flask, jsonify, request
from .models import TodoList

app = Flask(__name__)


# ── CORS ──────────────────────────────────────────────────────────────────────
# Gestione manuale CORS: funziona su qualsiasi versione di Flask,
# senza dipendenze esterne, e copre TUTTI i casi:
#   - preflight OPTIONS su path statici e dinamici
#   - risposte normali 2xx
#   - risposte di errore 4xx/5xx (after_request viene chiamato anche su errori)

def _cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PATCH, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@app.after_request
def add_cors(response):
    return _cors(response)


# Flask non chiama after_request per le risposte generate da handle_exception,
# quindi registriamo anche un error handler globale che aggiunge CORS.
@app.errorhandler(Exception)
def handle_exception(e):
    from werkzeug.exceptions import HTTPException
    if isinstance(e, HTTPException):
        response = e.get_response()
        response.data = __import__('json').dumps({"error": e.description})
        response.content_type = "application/json"
        return _cors(response)
    # Errore interno non previsto
    response = jsonify({"error": "Internal server error"})
    response.status_code = 500
    return _cors(response)


# Risponde alle preflight OPTIONS su qualsiasi path
@app.route("/", defaults={"path": ""}, methods=["OPTIONS"])
@app.route("/<path:path>",             methods=["OPTIONS"])
def preflight(path):
    from flask import make_response
    return _cors(make_response("", 204))


# ── Store in-memory ────────────────────────────────────────────────────────────
_todo = TodoList()


# ── Health ─────────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return jsonify({"status": "ok"})


# ── GET /todos ─────────────────────────────────────────────────────────────────

@app.get("/todos")
def get_todos():
    return jsonify({
        "items":   [i.to_dict() for i in _todo.all()],
        "count":   _todo.count,
        "pending": _todo.pending_count,
    })


# ── POST /todos ────────────────────────────────────────────────────────────────

@app.post("/todos")
def create_todo():
    data = request.get_json(silent=True) or {}
    title = data.get("title", "")
    try:
        item = _todo.add(title)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(item.to_dict()), 201


# ── IMPORTANTE: route specifica PRIMA della route con parametro ───────────────
# Flask valuta le route nell'ordine di registrazione.
# /todos/completed deve stare sopra /todos/<item_id>,
# altrimenti "completed" viene interpretato come item_id.

@app.delete("/todos/completed")
def clear_completed():
    removed = _todo.clear_completed()
    return jsonify({"removed": removed})


@app.patch("/todos/<item_id>/complete")
def complete_todo(item_id: str):
    try:
        item = _todo.complete(item_id)
    except KeyError:
        return jsonify({"error": "Not found"}), 404
    return jsonify(item.to_dict())


@app.delete("/todos/<item_id>")
def delete_todo(item_id: str):
    try:
        _todo.delete(item_id)
    except KeyError:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"deleted": item_id})
