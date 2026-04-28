/**
 * todo-client.js
 * Wrapper fetch per l'API Flask.
 *
 * Modalità sviluppo locale:  DEFAULT_BASE = "http://localhost:5000"
 * Modalità Docker:           DEFAULT_BASE = "/api"  (nginx fa da proxy)
 *
 * In Docker non servono CORS header perché frontend e backend
 * comunicano sulla rete interna — il browser vede solo nginx su :3000.
 */

// Rileva automaticamente se siamo in Docker (nginx proxy) o in sviluppo locale.
// In Docker window.location.port è "3000" e il backend non è raggiungibile
// direttamente: usiamo il proxy nginx su /api.
// In sviluppo locale il backend è su http://localhost:5000.
const DEFAULT_BASE = (
  typeof window !== "undefined" && window.API_BASE
) ? window.API_BASE
  : "http://localhost:5000";

export class TodoClient {
  constructor(baseUrl = DEFAULT_BASE) {
    this.baseUrl = baseUrl;
  }

  async _req(method, path, body = null) {
    const opts = { method, headers: { "Content-Type": "application/json" } };
    if (body) opts.body = JSON.stringify(body);
    const resp = await fetch(`${this.baseUrl}${path}`, opts);
    const data = await resp.json();
    if (!resp.ok) throw Object.assign(new Error(data.error || "API error"), { status: resp.status });
    return data;
  }

  getAll()         { return this._req("GET",    "/todos"); }
  create(title)    { return this._req("POST",   "/todos", { title }); }
  complete(id)     { return this._req("PATCH",  `/todos/${id}/complete`); }
  delete(id)       { return this._req("DELETE", `/todos/${id}`); }
  clearCompleted() { return this._req("DELETE", "/todos/completed"); }
}
