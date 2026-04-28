/**
 * todo-logic.js
 * Logica di presentazione pura — nessun DOM, nessun fetch.
 * Testabile con Vitest senza mock.
 */

/**
 * Formatta il contatore nella toolbar.
 * @param {number} pending
 * @returns {string}
 */
export function formatPendingLabel(pending) {
  if (pending === 0) return "Tutto fatto! 🎉";
  if (pending === 1) return "1 attività rimasta";
  return `${pending} attività rimaste`;
}

/**
 * Filtra i todo in base al filtro attivo.
 * @param {Array}  items
 * @param {"all"|"active"|"completed"} filter
 * @returns {Array}
 */
export function filterTodos(items, filter) {
  if (filter === "active")    return items.filter(i => !i.done);
  if (filter === "completed") return items.filter(i =>  i.done);
  return items;
}

/**
 * Valida il titolo di un nuovo todo.
 * @param {string} title
 * @returns {{ valid: boolean, error?: string }}
 */
export function validateTitle(title) {
  if (!title || title.trim().length === 0)
    return { valid: false, error: "Il titolo non può essere vuoto." };
  if (title.trim().length > 100)
    return { valid: false, error: "Il titolo non può superare i 100 caratteri." };
  return { valid: true };
}

/**
 * Ordina i todo: prima i pending, poi i completati.
 * @param {Array} items
 * @returns {Array}
 */
export function sortTodos(items) {
  return [...items].sort((a, b) => Number(a.done) - Number(b.done));
}
