/**
 * config.js — Configurazione runtime dell'API base URL.
 *
 * Sviluppo locale:  API_BASE = "http://l127.0.0.1:5000"
 * Docker:           API_BASE = "/api"  (nginx proxy → backend:5000)
 *
 * In Docker, nginx sostituisce questo file con una versione generata
 * da docker-compose tramite environment variable.
 */
window.API_BASE = "http://127.0.0.1:5000";
